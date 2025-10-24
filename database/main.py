from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, Integer, String
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import bcrypt


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple App", version="1.0.0")


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()



@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    # Create new user
    new_user = User(name=user.name, email=user.email, password=hashed_password.decode('utf-8'))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return (db)
