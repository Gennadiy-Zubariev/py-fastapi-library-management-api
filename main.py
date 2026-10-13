from collections.abc import Generator

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine

import models
import crud
import schemas


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as db:
        yield db


@app.post("/authors/", response_model=schemas.AuthorList)
def create_author(
        author_data: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    author = crud.get_author_by_name(db=db, name=author_data.name)
    if author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author already exists"
        )
    return crud.author_create(db=db, author_data=author_data)


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_author_list(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorDetail)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    return author


@app.post("/books/", response_model=schemas.BookList)
def create_book(book_data: schemas.BookCreate, db: Session = Depends(get_db)):
    if crud.get_author_by_id(db=db, author_id=book_data.author_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    return crud.book_create(db=db, book_data=book_data)


@app.get("/books/", response_model=list[schemas.BookList])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_book_list(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/books/", response_model=list[schemas.BookList])
def read_books_by_author_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_book_by_author_id(author_id=author_id, db=db)
