from database import db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import uvicorn
import bcrypt


load_dotenv()

app = FastAPI(title="User management App", version="1.0.0")

class Simple(BaseModel):
    name: str = Field(..., examples=["Sam Larry"])
    email: str = Field(..., examples=["sam@gmail.com"])
    password: str = Field(..., examples=["sam123"])
    usertype: str = Field(..., examples=["student"])

@app.post("/signup")
def signup(input: Simple):
    try:

        duplicate_query = text("""
            SELECT * FROM users WHERE email = :email
            
        """)

        existing = db.execute(duplicate_query, {"email": input.email})
        if existing:
            print("Email already exists")


        query = text("""
            INSERT INTO users (name, email, password)
            VALUES (:name, :email, :password)
        """)
            
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(input.password.encode('utf-8'), salt)

        
        db.execute(query, {"name": input.name, "email": input.email, "password":hashedPassword, "usertype": input.usertype})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))