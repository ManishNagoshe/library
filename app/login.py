from passlib.context import CryptContext
from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
import mysql.connector
from pydantic import BaseModel
from app.config import settings
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
        mydb = mysql.connector.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME
        )
        mycursor = mydb.cursor(dictionary=True)
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
    mydb = mysql.connector.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
    )
    mycursor = mydb.cursor(dictionary=True)
    val = (user.email,)
    mycursor.execute("SELECT email,password from users where email=%s", val)
    myresult = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    
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

        mydb = mysql.connector.connect(
            host=settings.HOST_NAME,
            user=settings.USER_NAME,
            password=settings.USER_PASSWORD,
            database=settings.DATABASE_NAME,
        )
        mycursor = mydb.cursor(dictionary=True)
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
    mydb = mysql.connector.connect(
        host=settings.HOST_NAME,
        user=settings.USER_NAME,
        password=settings.USER_PASSWORD,
        database=settings.DATABASE_NAME,
    )
    mycursor = mydb.cursor(dictionary=True)
    sql = "select role from users where email=%s"
    val = (username,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    if not myresult:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"invalid user")
    return myresult["role"]
