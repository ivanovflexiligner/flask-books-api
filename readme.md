CS50 web development course project 1 implementation

site about books with no design

Works with goodreads api and implements it's own api

There is a:

* User registration, login management
* search through site
* page for each book
* ability to leave comments
* API to site DB
* No ORM

*Fields in book.csv: isbn, title, author, year

SQL queries made for postgresql

Before you begin you need goodreads api keys. Find it here https://www.goodreads.com/api
You need db. I used a postgres by Heroku, it's free for personal projects. 
Copy it's uri and pass it to models.py to the create_engine function call


