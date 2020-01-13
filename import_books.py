from app.models import BookTable
import os, csv

file = "books.csv"

if os.path.exists(file):

    bt = BookTable()

    csv_reader = csv.reader(open(file))

    params = []

    all = 5000
    current = 0

    for isbn, title, author, year in csv_reader:

        bt.insert_book({"isbn": isbn, "title": title, "author": author, "year": year})
        current += 1
        all -= 1
        print(current, " inserted ", all, " left")


else:
    print("no such file")
