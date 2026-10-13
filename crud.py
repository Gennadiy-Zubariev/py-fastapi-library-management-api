from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Author, Book
import schemas


def get_author_by_name(db: Session, name: str):
    return db.scalars(select(Author).where(Author.name == name)).one_or_none()


def author_create(db: Session, author_data: schemas.AuthorCreate):
    author = Author(name=author_data.name, bio=author_data.bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_author_list(db: Session, skip: int, limit: int):
    stmt = select(Author).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def get_author_by_id(db: Session, author_id: int):
    return db.scalars(
        select(Author).where(Author.id == author_id)
    ).one_or_none()


def book_create(db: Session, book_data: schemas.BookCreate):
    book = Book(
        title=book_data.title,
        summary=book_data.summary,
        author_id=book_data.author_id,
        publication_date=book_data.publication_date,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book_list(db: Session, skip: int, limit: int):
    stmt = select(Book).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def get_book_by_author_id(db: Session, author_id: int):
    return db.scalars(select(Book).where(Book.author_id == author_id)).all()
