import os
import csv

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db.init_app(app)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["GET", "POST"])
def front():
    return render_template("front.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@app.route("/login_auth", methods=["GET", "POST"])
def login_auth():
    u = request.form.get("username")
    p = request.form.get("password")
    if User.query.filter_by(username=u).first() == None:
        return render_template("loginfailure.html")
    elif User.query.filter_by(username=u).first() != None:
        user = User.query.filter_by(username=u).first()
        if user.username == u and user.password == p:
            #session["user_id"] = user.id
            #session["user_id"]["notes"] = []
            return render_template("profile.html")       
        elif user.username == u and user.password != p:
            return render_template("loginfailure.html")

@app.route("/register_auth", methods=["GET", "POST"])
def register_auth():
    u = request.form.get("username")
    p = request.form.get("password")
    if User.query.filter_by(username=u).first() == None:
        user=User(username=u, password=p)
        db.add(user)
        db.commit()
        return render_template("profile.html")
    else:
        return render_template("registerfailure.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    #if request.method == "POST":
        #note = request.form.get("note")
        #session["notes"].append(note)
    return render_template("profile.html")

@app.route("/logout")
def logout():
    session.pop("user_id")
    return render_template("front.html")