from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    category: str


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    category: str
    available: bool

    class Config:
        from_attributes = True
