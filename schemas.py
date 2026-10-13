from datetime import date

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: date


class BookList(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    author_id: int


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorList(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AuthorDetail(AuthorList):
    books: list[BookList]
    model_config = ConfigDict(from_attributes=True)


class AuthorCreate(AuthorBase):
    pass
