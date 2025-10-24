from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pymysql.constants import CLIENT
import os
from dotenv import load_dotenv

load_dotenv()


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(
    db_url,
    connect_args={"client_flag": CLIENT.MULTI_STATEMENTS}
    )

session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

db = session()

# query = text("select * from user")

# users = db.execute(query).fetchall()

# print(users)


create_user =  text("""
    CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL
        );      
""")


# create_courses =  text("""
#     CREATE TABLE IF NOT EXISTS users (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             title VARCHAR(100) NOT NULL,
#             level VARCHAR(100) NOT NULL,
#             password VARCHAR(100) NOT NULL
#         );      


# """)

# create_enrollment =  text("""
#     CREATE TABLE IF NOT EXISTS users (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(100) NOT NULL,
#             email VARCHAR(100) NOT NULL,
#             password VARCHAR(100) NOT NULL
#         );      


# """)

db.execute(create_user)
# db.execute(create_courses)
# db.execute(create_enrollment)


