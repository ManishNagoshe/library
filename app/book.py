from http import cookies
from unicodedata import decimal
from app import login
from fastapi import HTTPException, status,APIRouter
from jose import JWTError, jwt
from datetime import datetime, timedelta
import mysql.connector
from pydantic import BaseModel
from app.config import settings
from typing import List, Optional
from fastapi import FastAPI,Cookie

router=APIRouter(
    prefix="/book"
)

class Insertbook(BaseModel):
    title:str
    author:str
    price:float
@router.post("/insertbook")
def insertbook(books:Insertbook,Manish:Optional[str]=Cookie(None)):
    role=login.getrole(Manish)
    if role!=1:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    
    if len(books.title)<2:
        return({"msg":"Name is not valid"})

    if len(books.author)<2:
        return({"msg":"Password is length is shorter than 8"})
    
    if books.price<=0:
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
        val = (books.title,books.author,books.price)
        mycursor.execute(sql,val,)
        mydb.commit()    
        mycursor.close()
        mydb.close()
        return({"msg":"Book registered successfully"})
    except :
        mycursor.close()
        mydb.close()
        return({"msg":"error occured while registring the book please check all fields"})

class Booksallpagination(BaseModel):
    startindex:int
    endindex:int

@router.post("/getallbooks_with_start_end_index")
def getallbooks_with_start_end_index(books:Booksallpagination,Manish:Optional[str]=Cookie(None)):
    role=login.getrole(Manish)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")

    if(books.endindex-books.startindex>=10):
        return({"msg":"Maximum 10 books can be fetched"})
    
    mydb = mysql.connector.connect(
    host=settings.HOST_NAME,
    user=settings.USER_NAME,
    password=settings.USER_PASSWORD,
    database=settings.DATABASE_NAME,
    )
    mycursor = mydb.cursor(dictionary=True)
    if(books.startindex>0):
        books.startindex=books.startindex-1
    val = (books.startindex,books.endindex)
    sql="SELECT title,authors,price,status FROM bookmaster order by accno limit %s,%s"
    mycursor.execute(sql, val,)
    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    if myresult:
        return(myresult)
    else:
        return

class Seachbyany(BaseModel):
    title:Optional[str]=None
    authors:Optional[str]=None
    startindex:int
    endindex:int

@router.post("/searchbook")
def seacrhbyanybooks(books:Seachbyany,Manish:Optional[str]=Cookie(None)):
    role=login.getrole(Manish)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")

    if(books.endindex-books.startindex>=10):
        return({"msg":"Maximum 10 books can be fetched"})
    
    mydb = mysql.connector.connect(
    host=settings.HOST_NAME,
    user=settings.USER_NAME,
    password=settings.USER_PASSWORD,
    database=settings.DATABASE_NAME,
    )
    mycursor = mydb.cursor(dictionary=True)
    if(books.startindex>0):
        books.startindex=books.startindex-1
    val = (books.title,f"%{books.title}%",books.authors,f"%{books.authors}%",books.startindex,books.endindex)
    # print(val)
    sql="SELECT title,authors,price,status FROM bookmaster where (title LIKE CASE WHEN %s IS NOT NULL THEN %s ELSE '%' END) and (authors LIKE CASE WHEN %s IS NOT NULL THEN %s ELSE '%' END) order by accno limit %s,%s"
    mycursor.execute(sql, val,)
    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    if myresult:
        return(myresult)
    else:
        return