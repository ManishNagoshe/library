from passlib.context import CryptContext
from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta

from pydantic import BaseModel
from app.config import settings
import psycopg2
from psycopg2.extras import RealDictCursor 
import re
SECRET_KEY = settings.SECRETKEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
pwd_context = CryptContext(schemes=["md5_crypt"])


def encryptpassword(password):
    hashpassword = pwd_context.hash(password)
    return hashpassword


class Createuser(BaseModel):
    email:str
    name:str
    password:str
    role:int
def createuser(createuser:Createuser):
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if not re.match(pat,createuser.email):
        return({"msg":"Email not valid"})
    if len(createuser.name)<2:
        return({"msg":"Name is not valid"})

    if len(createuser.password)<8:
        return({"msg":"Password is length is shorter than 8"})
    
    
    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO users (email, name,role,password) VALUES (%s, %s,%s,%s)"
        val = (createuser.email,createuser.name,createuser.role ,encryptpassword(createuser.password))
        mycursor.execute(sql,val,)
        mydb.commit()    
        mycursor.close()
        mydb.close()
        return({"msg":"user created sucessfully"})
    except :
        return({"msg":"error occured, role is invalid or user may exist"})

class Loginuser(BaseModel):
    email:str
    password:str
def loginuser(user:Loginuser):
    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        val = (user.email,)
        mycursor.execute("SELECT email,password from users where email=%s and status='Active'", val)
        myresult = mycursor.fetchone()
        mycursor.close()
        mydb.close()
    except:
        return({"msg":"Connection error"})
    
    if myresult:
        # print(myresult['name'])
        if pwd_context.verify(user.password, myresult["password"]):
            expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            data = {"username": user.email, "exp": expire, "time": str(expire)}
            # print(data)
            encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
            return {"msg": "logged_in", "cookie": encoded_jwt}

        else:
            return {"msg": "invalid credentials"}
    else:
        return {"msg": "invalid credentials"}

    
def verifyuser(cookie: str):
    if not cookie:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    try:
        data = jwt.decode(cookie, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = data.get("username")
        print(username)
        expiredtime = data.get("time")
        validity = datetime.fromisoformat(expiredtime) - datetime.now()
        if validity.total_seconds() < 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Login Expired")

        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        val = (username,)
        mycursor.execute("SELECT email FROM users where email=%s", val)
        myresult = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        if not myresult:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    except JWTError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    return username

def setcookie(username: str):
    if not username:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"username": username, "exp": expire, "time": str(expire)}
    # print(data)
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def getrole(Manish:str):
    username = verifyuser(Manish)
    if not username:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        sql = "select role from users where email=%s"
        val = (username,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        if not myresult:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
        return myresult["role"]
    except:
        return({"msg":"Connection error"})

def getusername(Manish:str):
    username = verifyuser(Manish)
    if not username:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        sql = "select name from users where email=%s"
        val = (username,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        if not myresult:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
        return myresult["name"]
    except:
        return({"msg":"Connection error"})

def getuserid(Manish:str):
    username = verifyuser(Manish)
    if not username:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        sql = "select id from users where email=%s"
        val = (username,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        if not myresult:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
        return myresult["id"]
    except:
        return({"msg":"Connection error"})


class Changepassword(BaseModel):
    old_password:str
    new_password:str

def changepassword(changepass:Changepassword,Manish):
    email=verifyuser(Manish)
    if not email:
         raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    try:
        mydb = psycopg2.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
        cursor_factory=RealDictCursor
        )
        mycursor = mydb.cursor()
        # print("SELECT name,password FROM ioc where name=%s")
        val = (email,)
        mycursor.execute("SELECT email,password FROM users where email=%s", val)
        myresult = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        # myres=dict(zip(mycursor.column_names, mycursor.fetchall()))
        if myresult:
            # print(myresult['name'])
            if pwd_context.verify(changepass.old_password, myresult["password"]):
                mydb = psycopg2.connect(
                host=settings.HOST_NAME,
                user=settings.USER_NAME,
                password=settings.USER_PASSWORD,
                database=settings.DATABASE_NAME,
                cursor_factory=RealDictCursor
                )
                mycursor = mydb.cursor()
                # print("SELECT name,password FROM ioc where name=%s")
                val = (encryptpassword(changepass.new_password),email,)
                sql = "UPDATE users SET password=%s WHERE email=%s"
                mycursor.execute(sql, val)
                mydb.commit()
                row=mycursor.rowcount
                mycursor.close()
                mydb.close()
                if(row>0):
                    return({"msg":"password changed successfully"})

        return({"error":"Password not updated, check old password"})
    except:
        return({"msg":"Connection error"})
