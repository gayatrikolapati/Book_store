from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from models import User, Book
from models_db import UserDB, BookDB
from database import SessionLocal, engine, Base
import random
import shutil
import hashlib
import requests
import os

Base.metadata.create_all(bind=engine)

MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_SENDER = os.getenv("MAILJET_SENDER")
app = FastAPI()

# ===================== MAILJET CONFIG =====================
MAILJET_API_KEY = "c37fa7b676712cd324047b17f4fd813a"
MAILJET_SECRET_KEY = "9529fd3a213707bd2f4c61a75f77ebd2"
MAILJET_SENDER = "kolapatigayatri@gmail.com"   
# ===================== PASSWORD HASH =====================
# ===================== HASH PASSWORD =====================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@app.post("/login")
def login(email: str, password: str):

    # ADMIN LOGIN
    if email == "Gayatri" and password == "Honey@123":
        return {"login": "admin", "name": "Admin"}

    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")

    if user.password != hash_password(password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"login": "user", "name": user.name}


# -------------------- ADD BOOK --------------------
@app.post("/books")
def add_book(
    admin_username: str = Form(...),
    admin_password: str = Form(...),
    title: str = Form(...),
    author: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    image: UploadFile = File(None)
):

    if admin_username != "Gayatri" or admin_password != "Honey@123":
        raise HTTPException(status_code=401, detail="Only admin can add books")

    db = SessionLocal()
    
    exists = db.query(BookDB).filter(
        BookDB.title.ilike(title), BookDB.author.ilike(author)
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Book already exists")

    image_path = None
    if image:
        image_path = f"bookstore_images/{image.filename}"
        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

    new_book = BookDB(
        title=title, author=author, price=price,
        quantity=quantity, image_path=image_path
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {"message": "Book added", "book": new_book}


# -------------------- GET BOOKS --------------------
@app.get("/books")
def get_books():
    db = SessionLocal()
    return db.query(BookDB).all()


# -------------------- EDIT BOOK --------------------
@app.put("/books/{book_id}")
def edit_book(
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...)
):
    db = SessionLocal()
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = title
    book.author = author
    book.price = price
    book.quantity = quantity

    db.commit()
    db.refresh(book)
    return {"message": "Book updated", "book": book}


# -------------------- DELETE BOOK --------------------
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    db = SessionLocal()
    book = db.query(BookDB).filter(BookDB.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}


# -------------------- USERS LIST --------------------
@app.get("/users")
def get_users():
    db = SessionLocal()

    return db.query(UserDB).all()
