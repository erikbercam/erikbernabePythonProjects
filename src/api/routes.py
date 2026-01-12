from flask import jsonify, request
from src.config.db import session
from src.models.book import Book

def init_api_routes(app):

    @app.route('/api/books', methods=['GET'])
    def get_books():
        books = session.query(Book).all()
        return jsonify([{'id': b.id, 'title': b.title, 'author': b.author} for b in books])

    @app.route('/api/books', methods=['POST'])
    def post_book():
        data = request.get_json()
        new_book = Book(title=data['title'], author=data['author'], price=data.get('price'))
        session.add(new_book)
        session.commit()
        return jsonify({'message': 'Libro creado'}), 201

    @app.route('/api/books/<int:id>', methods=['PUT'])
    def put_book(id):
        data = request.get_json()
        book = session.query(Book).get(id)
        if not book: return jsonify({"error": "No encontrado"}), 404
        book.title = data.get('title', book.title)
        session.commit()
        return jsonify({'message': 'Actualizado'})

    @app.route('/api/books/<int:id>', methods=['DELETE'])
    def delete_book(id):
        book = session.query(Book).get(id)
        if not book: return jsonify({"error": "No encontrado"}), 404
        session.delete(book)
        session.commit()
        return jsonify({'message': 'Eliminado'}), 204