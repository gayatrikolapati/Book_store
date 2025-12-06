from pydantic import BaseModel, EmailStr, Field, validator

# ================== USER MODEL ==================
class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=30)
    email: EmailStr
    age: int = Field(..., ge=18, le=60)
    password: str = Field(..., min_length=6)

    @validator("name")
    def name_letters_only(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters")
        return v

    @validator("password")
    def strong_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must include at least 1 uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must include at least 1 digit")
        return v


# ================== BOOK MODEL ==================
class Book(BaseModel):
    id: int | None = None
    title: str = Field(..., min_length=2, max_length=50)
    author: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)

    @validator("title")
    def title_not_numeric(cls, v):
        if v.isdigit():
            raise ValueError("Book title cannot be only numbers")
        return v

    @validator("author")
    def author_no_digits(cls, v):
        if any(c.isdigit() for c in v):
            raise ValueError("Author name cannot contain numbers")
        return v
