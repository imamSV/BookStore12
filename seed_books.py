import json
from bookstore import create_app, db
from bookstore.models import Book, Genre

app = create_app()

with app.app_context():
    with open("data/books_catalog.json", "r", encoding="utf-8") as f:
        books = json.load(f)

    for b in books:
        genre_name = b.get("genre")
        genre = Genre.query.filter_by(name=genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
            db.session.add(genre)

        book = Book(
            title=b.get("title"),
            author=b.get("author"),
            year=b.get("year"),
            price=b.get("price"),
            description=b.get("description"),
            cover_url=b.get("cover_url"),
            rating=b.get("rating")
        )

        book.genres.append(genre)
        db.session.add(book)

    db.session.commit()
    print("Книги успешно сохранены")