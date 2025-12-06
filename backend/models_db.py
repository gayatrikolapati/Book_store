from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)


class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_path = Column(String, nullable=True)
