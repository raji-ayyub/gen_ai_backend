from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pymysql.constants import CLIENT
import os

load_dotenv()


# db_url = dialect+driver://dbuser;dbpassword;dbhost;dbport;dbname

db_url = f"mysql+pymysql://{os.getenv("dbuser")}:{os.getenv("dbpassword")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/{os.getenv("dbname")}"


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


