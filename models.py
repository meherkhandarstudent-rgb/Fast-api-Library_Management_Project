from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=True)
    available = Column(Boolean, default=True)
