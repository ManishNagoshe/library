from http import cookies
from unicodedata import decimal
from app import login
from fastapi import HTTPException, status,APIRouter
from jose import JWTError, jwt
from datetime import date

from pydantic import BaseModel
from app.config import settings
from typing import List, Optional
from fastapi import FastAPI,Cookie
import psycopg2
from psycopg2.extras import RealDictCursor
from starlette.responses import Response
router=APIRouter(
    prefix="/book"
)

class Insertbook(BaseModel):
    title:str
    author:str
    price:float
@router.post("/insertbook")
def insertbook(response:Response,books:Insertbook,Manish:Optional[str]=Cookie(None)):
    role=login.getrole(Manish)
    if role!=1:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    
    if len(books.title)<2:
        return({"msg":"Name is not valid"})

    if len(books.author)<2:
        return({"msg":"Author is short in length"})
    
    if books.price<=0:
        return({"msg":"invalid price"})

    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO bookmaster (title, authors,price) VALUES (%s, %s,%s) returning accno"
        val = (books.title,books.author,books.price)
        mycursor.execute(sql,val,)
        rowid=mycursor.fetchone()
        mydb.commit()
        # print(rowid['accno'])
        mycursor.close()
        mydb.close()
        response.set_cookie(key="Manish",value=login.setcookie(login.verifyuser(Manish)), httponly=True,secure=settings.SECURITYHHTPS, samesite=settings.SAMESITE)
        return({"msg":"Book registered successfully","accno":rowid['accno']})
    except :
        return({"msg":"error occurred while registering the book please check all fields or may connection error"})

class Booksallpagination(BaseModel):
    startindex:int
    endindex:int

@router.post("/getallbooks_with_start_end_index")
def getallbooks_with_start_end_index(response:Response,books:Booksallpagination,Manish:Optional[str]=Cookie(None)):
    role=login.getrole(Manish)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")

    if(books.endindex-books.startindex>10):
        return({"msg":"Maximum 10 books can be fetched"})
    
    if(books.startindex<0):
        return({"msg":"Start index minimum value should be zero"})
    
    if(books.endindex<books.startindex):
        return({"msg":"end index should be greater than start index"})
    try:

        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        max_num=books.endindex-books.startindex
        val = (max_num,books.startindex)
        sql="SELECT accno,title,authors,price,status FROM bookmaster order by accno limit %s offset %s"
        mycursor.execute(sql, val,)
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        response.set_cookie(key="Manish",value=login.setcookie(login.verifyuser(Manish)), httponly=True,secure=settings.SECURITYHHTPS, samesite=settings.SAMESITE)
        if myresult:
            return(myresult)
        else:
            return
    except:
        return({"msg":"Connection error"})

class Searchbyany(BaseModel):
    title:Optional[str]=None
    authors:Optional[str]=None
    startindex:int
    endindex:int

@router.post("/searchbook")
def seacrhbyanybooks(response:Response,books:Searchbyany,Manish:Optional[str]=Cookie(None)):
    role=login.getrole(Manish)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")

    if(books.endindex-books.startindex>10):
        return({"msg":"Maximum 10 books can be fetched"})
    if(books.startindex<0):
        return({"msg":"Start index minimum value should be zero"})
    
    if(books.endindex<books.startindex):
        return({"msg":"end index should be greater than start index"})
    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        max_num=books.endindex-books.startindex
        val = (f"%{books.title}%",books.title,f"%{books.authors}%",books.authors,max_num,books.startindex)
        # print(val)
        sql="SELECT accno,title,authors,price,status FROM bookmaster where (lower(title) like lower(%s) OR %s IS NULL)  and (lower(authors) like lower(%s) OR %s IS NULL)  order by accno limit %s offset %s"
        mycursor.execute(sql, val,)
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        response.set_cookie(key="Manish",value=login.setcookie(login.verifyuser(Manish)), httponly=True,secure=settings.SECURITYHHTPS, samesite=settings.SAMESITE)
        if myresult:
            return(myresult)
        else:
            return
    except:
        return({"msg":"Connection error"})

class Issuebook(BaseModel):
    accno:int
    userid:int

def checkbookavailability(accno:int):
    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        
        val = (accno,)
        # print(accno)
        # print(val)
        sql="SELECT status from bookmaster where accno=%s"
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        print(myresult['status'])
        return(myresult['status'])
    except:
        return("Error")

def checkvaliduser(userid:int):
    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        
        val = (userid,)
        # print(accno)
        # print(val)
        sql="SELECT status from users where id=%s"
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        print(myresult['status'])
        return(myresult['status'])
    except:
        return("Error")

@router.post("/issuebook")
def issuebook(response:Response,books:Issuebook,Manish:Optional[str]=Cookie(None)):
    role=login.getrole(Manish)
    if role!=1:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    
    # print(checkbookavailability(books.accno))
    if checkbookavailability(books.accno)!="Available":
        return({"msg":"Book is not available"})

    if checkvaliduser(books.userid)!="Active":
        return({"msg":"User is deleted or does not exists"})

    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO usage (userid, accno,issuedate) VALUES (%s, %s,%s)"
        val = (books.userid,books.accno,date.today())
        mycursor.execute(sql,val,)

        sql = "UPDATE bookmaster SET status='Issued', issuedto=%s WHERE accno=%s"
        val = (books.userid,books.accno,)
        mycursor.execute(sql,val)

        mydb.commit()    
        mycursor.close()
        mydb.close()
        response.set_cookie(key="Manish",value=login.setcookie(login.verifyuser(Manish)), httponly=True,secure=settings.SECURITYHHTPS, samesite=settings.SAMESITE)
        return({"msg":"Book issued successfully"})
    except:
        mydb.rollback()
        return({"msg":"Connection error"})
    
class Delete_book(BaseModel):
    accno:int
@router.put("/delete_book")
def delete_book(response:Response,books:Delete_book,Manish:Optional[str]=Cookie(None)):
    role=login.getrole(Manish)
    if role!=1:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    
    # print(checkbookavailability(books.accno))
    if checkbookavailability(books.accno)=="Deleted" or checkbookavailability(books.accno)=="Error":
        return({"msg":"Book is already deleted or not available"})

    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
            
        sql = "UPDATE bookmaster SET status='Deleted' WHERE accno=%s"
        val = (books.accno,)
        mycursor.execute(sql,val)

        mydb.commit()    
        mycursor.close()
        mydb.close()
        response.set_cookie(key="Manish",value=login.setcookie(login.verifyuser(Manish)), httponly=True,secure=settings.SECURITYHHTPS, samesite=settings.SAMESITE)
        return({"msg":"Book Deleted successfully"})
    except:
        # mydb.rollback()
        return({"msg":"Connection error"})

class Update_book(BaseModel):
    accno:int
    title:str
    author:str
    price:float
@router.put("/update_book")
def delete_book(response:Response,books:Update_book,Manish:Optional[str]=Cookie(None)):
    role=login.getrole(Manish)
    if role!=1:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    
    # print(checkbookavailability(books.accno))
    if checkbookavailability(books.accno)=="Deleted" or checkbookavailability(books.accno)=="Error":
        return({"msg":"Book is already deleted or not available"})

    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
            
        sql = "UPDATE bookmaster SET title=%s, authors=%s, price=%s WHERE accno=%s"
        val = (books.title,books.author,books.price,books.accno,)
        mycursor.execute(sql,val,)

        mydb.commit()    
        mycursor.close()
        mydb.close()
        response.set_cookie(key="Manish",value=login.setcookie(login.verifyuser(Manish)), httponly=True,secure=settings.SECURITYHHTPS, samesite=settings.SAMESITE)
        return({"msg":"Book updated successfully"})
    except:
        # mydb.rollback()
        return({"msg":"Connection error"})

def returnbookavailability(accno:int):
    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        
        val = (accno,)
        # print(accno)
        # print(val)
        sql="SELECT status,issuedto from bookmaster where accno=%s"
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        # print(myresult['status'])
        return({"status":myresult['status'],"issuedto":myresult['issuedto']})
    except:
        return("Error")

class Returnbook(BaseModel):
    accno:int
@router.put("/returnbook")
def returnbook(response:Response,books:Returnbook,Manish:Optional[str]=Cookie(None)):
    role=login.getrole(Manish)
    if role!=1:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    
    try:
        bookdetail=returnbookavailability(books.accno)
        if bookdetail['status']!="Issued":
            return({"msg":"Book is not Issued"})
    except:
        return({"msg":"Please check accno"})
    
    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        sql = "UPDATE usage SET returndate=%s where userid=%s and accno=%s and returndate is NULL"
        val = (date.today(),bookdetail['issuedto'],books.accno,)
        mycursor.execute(sql,val,)

        sql = "UPDATE bookmaster SET status='Available', issuedto=%s WHERE accno=%s"
        val = (None,books.accno,)
        mycursor.execute(sql,val)

        mydb.commit()    
        mycursor.close()
        mydb.close()
        response.set_cookie(key="Manish",value=login.setcookie(login.verifyuser(Manish)), httponly=True,secure=settings.SECURITYHHTPS, samesite=settings.SAMESITE)
        return({"msg":"Book Returned successfully"})
    except:
        mydb.rollback()
        return({"msg":"Connection error"})