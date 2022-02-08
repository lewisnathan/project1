from application import *

def main():
    db.create_all()
    f = open("books.csv")
    reader = csv.reader(f)
    for ISBN, title, author, year in reader:
        book = Book(ISBN=ISBN, title=title, author=author, year=year)
        db.session.add(book)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()