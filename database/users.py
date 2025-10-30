from database import db
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import uvicorn
import bcrypt

from middleware import create_token, verify_token





load_dotenv()

token_time = os.getenv("token_time")

app = FastAPI(title="User management App", version="1.0.0")

class Simple(BaseModel):
    name: str = Field(..., examples=["Sam Larry"])
    email: str = Field(..., examples=["sam@gmail.com"])
    password: str = Field(..., examples=["sam123"])
    usertype: str = Field(..., examples=["student"])



class Login(BaseModel):
    email: str = Field(..., examples=["sam@gmail.com"])
    password: str = Field(..., examples=["sam123"])


class courseRequest(BaseModel):
    title: str = Field(..., examples=["Algorithms"])
    level: str = Field(..., examples=["300lv"])


class enrollmentRequest(BaseModel):
    course_id: int = Field(..., examples=["232"])

# class courseID()


@app.post("/signup")
def signup(input: Simple):
    try:

        duplicate_query = text("""
            SELECT * FROM users WHERE email = :email
            
        """)

        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")


        query = text("""
            INSERT INTO users (name, email, password, usertype)
            VALUES (:name, :email, :password, :usertype)
        """)
            
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(input.password.encode('utf-8'), salt)

        try:
            db.execute(query, {"name": input.name, "email": input.email, "password":hashedPassword, "usertype": input.usertype})
            db.commit()
            return ({"message": "user created successfully"})
        except:
            db.rollback()
        finally:
            db.close()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail = str(e))
    

@app.post("/login")
def login(input: Login):
    try:
        query = text("SELECT * FROM users WHERE email = :email")
        user = db.execute(query, {"email": input.email}).fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # password is stored as bytes — ensure both are bytes before checking
        stored_password = user.password if isinstance(user.password, bytes) else user.password.encode('utf-8')


        verified_password = bcrypt.checkpw(input.password.encode('utf-8'), stored_password)


        if not verified_password:
            raise HTTPException(status_code=401, detail="Invalid password")
        
        encoded_token = create_token(details={
            "email": user.email,
            "usertype": user.usertype,
            "user_id": user.id
        }, expiry=token_time)

        return {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "usertype": user.usertype
            },
            "token": encoded_token
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    



@app.post("/courses")
def add_courses(input: courseRequest, user_data = Depends(verify_token)):
    try:
        
        print(user_data)
        if user_data["usertype"] != 'admin':
            raise HTTPException(status_code=401, detail="You are not authorized to add a course")
        

        query = text("""
            INSERT INTO courses (title, level)
            VALUES (:title, :level)
        """)

        

        db.execute(query, {"title":input.title, "level": input.level})
        db.commit()

        return {"message": f"course {input.title} created successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()




@app.post("/enrol")
def enroll_student(input: enrollmentRequest, user_data = Depends(verify_token)):
    try:
        
        print(user_data)
        # if user_data["usertype"] != 'admin':
        #     raise HTTPException(status_code=401, detail="You are not authorized to add a course")
        

        query = text("""
            INSERT INTO enrollment (user_id, course_id)
            VALUES (:user_id, :course_id)
        """)

        

        db.execute(query, {"user_id":user_data["user_id"], "course_id": input.course_id})
        db.commit()

        return {"message": f"student enrolled {user_data["user_id"]} successfully to course {input.course_id}"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()




# if __name__ == "__main__":
#     uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))