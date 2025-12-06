from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from backend.models import User, Book
from backend.models_db import UserDB, BookDB
from database import SessionLocal, engine, Base
import random
import shutil
import hashlib
import requests
import os

# -------------------- CREATE DATABASE TABLES --------------------
Base.metadata.create_all(bind=engine)

# -------------------- MAILJET ENV VARIABLES --------------------
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_SENDER = os.getenv("MAILJET_SENDER")

if not MAILJET_API_KEY or not MAILJET_SECRET_KEY or not MAILJET_SENDER:
    raise Exception("Mailjet environment variables are missing!")

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Book Store API is running!"}


# -------------------- PASSWORD HASH --------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# -------------------- SEND OTP USING MAILJET --------------------
def send_email(to_email: str, otp: int) -> bool:
    url = "https://api.mailjet.com/v3.1/send"
    data = {
        "Messages": [
            {
                "From": {"Email": MAILJET_SENDER, "Name": "Bookstore OTP"},
                "To": [{"Email": to_email}],
                "Subject": "Your OTP Code",
                "TextPart": f"Your OTP is {otp}"
            }
        ]
    }

    response = requests.post(
        url,
        auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY),
        json=data
    )

    return response.status_code == 200


otp_store = {}  # TEMP OTP MEMORY STORE


# -------------------- REQUEST OTP --------------------
@app.post("/request-otp")
def request_otp(email: str):

    otp = random.randint(1000, 9999)
    otp_store[email] = otp

    sent = send_email(email, otp)
    if not sent:
        raise HTTPException(status_code=500, detail="Failed to send OTP email")

    return {"message": "OTP sent"}


# -------------------- VERIFY OTP & REGISTER USER --------------------
@app.post("/verify-otp")
def verify_otp(user: User, otp: str):

    db = SessionLocal()

    # Check OTP exists
    if user.email not in otp_store:
        raise HTTPException(status_code=400, detail="OTP not requested")

    # Check OTP matches
    if str(otp_store[user.email]) != str(otp):
        raise HTTPException(status_code=400, detail="Incorrect OTP")

    # Remove OTP after successful verification
    del otp_store[user.email]

    # Check if user exists already
    exists = db.query(UserDB).filter(UserDB.email == user.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)

    new_user = UserDB(
        name=user.name,
        email=user.email,
        age=user.age,
        password=hashed_pw,
        is_verified=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# -------------------- LOGIN --------------------
@app.post("/login")
def login(email: str, password: str):

    # ADMIN LOGIN (CUSTOM)
    if email == "Gayatri" and password == "Honey@123":
        return {"login": "admin", "name": "Admin"}

    db = SessionLocal()
    hashed_pw = hash_password(password)

    user = db.query(UserDB).filter(UserDB.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")

    if user.password != hashed_pw:
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"login": "user", "name": user.name}


# -------------------- ADD BOOK (ADMIN ONLY) --------------------
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

    # Duplicate check
    exists = db.query(BookDB).filter(
        BookDB.title.ilike(title),
        BookDB.author.ilike(author)
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Book already exists")

    image_path = None
    if image:
        image_path = f"bookstore_images/{image.filename}"
        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

    new_book = BookDB(
        title=title,
        author=author,
        price=price,
        quantity=quantity,
        image_path=image_path
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {"message": "Book added", "book": new_book}


# -------------------- GET ALL BOOKS --------------------
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


# -------------------- GET USERS --------------------
@app.get("/users")
def get_users():
    db = SessionLocal()
    return db.query(UserDB).all()


