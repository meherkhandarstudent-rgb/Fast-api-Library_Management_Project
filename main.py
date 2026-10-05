from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import Book
from schemas import BookCreate, BookResponse


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Library Management API")


# ==================================================
# HOME
# ==================================================

@app.get("/")
def home():
    return {
        "message": "Library Management API is running"
    }


# ==================================================
# ADD BOOK
# ==================================================

@app.post("/books", response_model=BookResponse)
def add_book(
    book: BookCreate,
    db: Session = Depends(get_db)
):

    # Check duplicate ISBN
    existing_book = db.query(Book).filter(
        Book.isbn == book.isbn
    ).first()

    if existing_book:
        raise HTTPException(
            status_code=400,
            detail="Book with this ISBN already exists"
        )

    new_book = Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        category=book.category,
        available=True
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


# ==================================================
# GET ALL BOOKS
# ==================================================

@app.get("/books", response_model=list[BookResponse])
def get_books(
    db: Session = Depends(get_db)
):

    books = db.query(Book).all()

    return books


# ==================================================
# GET SINGLE BOOK
# ==================================================

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):

    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


# ==================================================
# UPDATE BOOK
# ==================================================

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_data: BookCreate,
    db: Session = Depends(get_db)
):

    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    # Check duplicate ISBN
    existing_book = db.query(Book).filter(
        Book.isbn == book_data.isbn,
        Book.id != book_id
    ).first()

    if existing_book:
        raise HTTPException(
            status_code=400,
            detail="Another book already uses this ISBN"
        )

    book.title = book_data.title
    book.author = book_data.author
    book.isbn = book_data.isbn
    book.category = book_data.category

    db.commit()
    db.refresh(book)

    return book


# ==================================================
# DELETE BOOK
# ==================================================

@app.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):

    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    db.delete(book)
    db.commit()

    return {
        "message": "Book deleted successfully"
    }