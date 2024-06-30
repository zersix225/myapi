from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    cnx = mysql.connector.connect(
        host = os.getenv("MYSQL_HOST"),
        user = os.getenv("MYSQL_username"),
        database = os.getenv("MYSQL_DATABASE")
    )
    return cnx

app = FastAPI()

class User_details(BaseModel):
    username: str
    first_name: str
    last_name: str
    gender: str 
    password: str

@app.post('/userdata')
def create_user(user_details: User_details):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = '''
    INSERT INTO user_details (username, first_name, last_name, gender, password )
    VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(query, (user_details.username, user_details.first_name, user_details.last_name
                          ,user_details.gender, user_details.password))
    cnx.commit()
    user_details_id = cursor.lastrowid
    cursor.close()
    cnx.close()
    return {"id": user_details_id}

@app.get('/userdata')
def get_user():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "SELECT * FROM user_details "
    cursor.execute(query)
    row = cursor.fetchall()
    cursor.close
    cnx.close

    user_details = []
    for row in row:
        user_details.append({
            "id": row[0],
            "username": row[1],
            "first_name": row[2],
            "last_name": row[3]
        })
    return user_details



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"seeee": item_id}

@app.get("/cal/{x}/{y}")
def read_item(x: int , y: int):
    sum = x+y
    return {"message": sum}



