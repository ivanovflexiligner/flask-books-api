The application provides acces to it's own DB with books

Data output format - json

There is two methods:

GET host/books/api/1.0/books - show all books from DB
GET host/books/api/1.0/books/{isbn} - show particular book by isbn

Book fields:

* author_id: str
* id: str
* isbn: str
* title: str
* year: str

To create a database run manage.py using CLI with command "create-db"
To fill database run manage.py using CLI with command "fill-db"

*Fields in book.csv: isbn, title, author, year