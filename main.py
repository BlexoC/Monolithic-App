from flask import Flask, jsonify, request
from flask import Flask, json, jsonify, request
from extensions import db
from flask_migrate import Migrate
from controllers.book_controller import BookController

app = Flask(__name__)
# Configure the database URI (replace with your actual database URI)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Book Management API!"})

@app.route('/books')
def get_books():
    books = BookController.get_all_books()
    return jsonify(books)

@app.route('/books/<int:book_id>')
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    book = BookController.get_book_by_id(book_id)
    return jsonify(book) if book else jsonify({"error": "Book not found"}), 404

@app.route('/books', methods=['POST'])
def create_book():
    new_book = {
        "id": len(books) + 1,
        "id": request.json.get("id"),
        "title": request.json.get("title"),
        "author": request.json.get("author")
    }
    books.append(new_book)
    new_book = BookController.create_book(new_book)
    return jsonify(new_book), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    book = BookController.get_book_by_id(book_id)

    # update the book if present 
    if book:
        update_book = {
            "title": request.json.get("title", book["title"]),
            "author": request.json.get("author", book["author"])
        }

        updated_book = BookController.update_book(book_id, update_book)
        return jsonify(updated_book), 200


    if not book:
        return jsonify({"error": "Book not found"}), 404

    book["title"] = request.json.get("title", book["title"])
    book["author"] = request.json.get("author", book["author"])
    return jsonify(book)

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [book for book in books if book["id"] != book_id]
    return jsonify({"message": "Book deleted successfully"}), 204
    book = BookController.get_book_by_id(book_id)

    if book: 
        BookController.delete_book(book_id)
        return jsonify({"message": "Book deleted successfully"}), 204
    else: 
        return jsonify({"error": "Book not found"}), 404

@app.route('/about')
def about():
    return jsonify({"message": "This is a simple book management API."})