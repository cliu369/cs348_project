import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "library.db")

db = SQLAlchemy(app)

class Author(db.Model):
    __tablename__ = "Authors"
    author_id = db.Column(db.Integer, primary_key = True)
    # index on authors.name because of name filter 
    name = db.Column(db.String(200), nullable = False, index = True)
    books = db.relationship("Book", backref = "author", lazy = True)

class Book(db.Model):
    __tablename__ = "Books"
    book_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    # index on books.pub_year because of publication year filter
    pub_year = db.Column(db.Integer, nullable = False, index = True)
    loan_count = db.Column(db.Integer, nullable = False, default = 0)
    author_id = db.Column(db.Integer, db.ForeignKey("Authors.author_id"), nullable = False)

@app.route("/add_book", methods = ["GET", "POST"])
def add_book(): 
    if request.method == "POST":
        author_name = request.form.get("author_name")
        book_title = request.form.get("title")
        year = request.form.get("pub_year")

        db.session.begin()
        try:
            existing_author = Author.query.filter_by(name=author_name).first()
            if existing_author:
                target_author = existing_author
            else:
                target_author = Author(name = author_name)
            
            new_book = Book(title=book_title, pub_year = year, author = target_author)

            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for("home"))
        except Exception as e:
            db.session.rollback()
            return f"Error: {e}", 500
    return render_template("/add_book.html")

@app.route("/borrow/<int:id>")
def borrow_book(id): 
    db.session.begin()
    try:
        book = Book.query.get_or_404(id)
        book.loan_count += 1
        db.session.commit()
        return redirect(url_for("home"))
    except Exception as e:
        db.session.rollback()
        return f"Error: {e}", 500 

@app.route("/delete_book/<int:id>")
def delete_book(id):
    db.session.begin()
    try:
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for("home"))
    except Exception as e: 
        db.session.rollback()
        return f"Error: {e}", 500

@app.route("/")
def home(): 
    query = Book.query

    raw_year = request.args.get("year")
    raw_author = request.args.get("author")

    if raw_year:
        query = query.filter(Book.pub_year == raw_year)

    if raw_author:
        query = query.join(Author).filter(Author.name.contains(raw_author))
    
    books = query.all()
    return render_template("index.html", books=books)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)