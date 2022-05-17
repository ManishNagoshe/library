from unicodedata import decimal
from app import login
from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
import mysql.connector
from pydantic import BaseModel
from app.config import settings

class Insertbook(BaseModel):
    title:str
    author:str
    price:float

def insertbook(insertbook:Insertbook,Manish):
    role=login.getrole(Manish)
    if role!=1:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    
    if len(insertbook.title)<2:
        return({"msg":"Name is not valid"})

    if len(insertbook.author)<2:
        return({"msg":"Password is length is shorter than 8"})
    
    if insertbook.price<=0:
        return({"msg":"invalid price"})

    try:
        mydb = mysql.connector.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME
        )
        mycursor = mydb.cursor(dictionary=True)
        sql = "INSERT INTO bookmaster (title, authors,price) VALUES (%s, %s,%s)"
        val = (insertbook.title,insertbook.author,insertbook.price)
        mycursor.execute(sql,val,)
        mydb.commit()    
        mycursor.close()
        mydb.close()
        return({"msg":"Book registered successfully"})
    except :
        mycursor.close()
        mydb.close()
        return({"msg":"error occured while registring the book please check all fields"})

    
    