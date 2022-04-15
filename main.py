from crypt import methods
from enum import unique
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Books %r>' % self.title

db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    print(all_books)

    return render_template('index.html', all_books=all_books)

@app.route("/add")
def add():
    return render_template('add.html')


@app.route("/add", methods=['POST'])
def add_row():
    name = request.form['name']
    author = request.form['author']
    rating = request.form['rating']
    books = Books(title=name, author=author, rating=rating)
    db.session.add(books)
    db.session.commit()
    return home()

@app.route("/edit/<int:id>")
def edit_rating(id=id):
    book = Books.query.filter_by(id=id).first()
    return render_template("edit.html", title=book.title,rating=book.rating, id=book.id)

@app.route("/edit/<int:id>",methods=['POST'])
def change_rating(id=id):
    new_rating = request.form['rating']
    book = Books.query.get(id)
    book.rating = new_rating
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/delete/<int:id>")
def delete_book(id):
    book = Books.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)

