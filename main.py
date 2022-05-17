from typing import List, Optional
from fastapi import FastAPI,Cookie
from app import login,book
import requests
from starlette.requests import cookie_parser
import os
from app.config import settings
from starlette.requests import cookie_parser
from starlette.responses import Response
from starlette.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware


script_dir = os.path.dirname(__file__)
staticpath = os.path.join(script_dir, "static/")

app=FastAPI()

origins=settings.ORIGINS



#sign up
@app.post("/signup")
def signup(usercreate:login.Createuser):
    return(login.createuser(usercreate))


#login------------------------------------------------------------------
@app.post("/login")
def loginpage(response:Response,userdetails:login.Loginuser): #
    
    token=login.loginuser(userdetails)
    if(token['msg']=="invalid credentials"):
        return({"msg":"invalid credentials"})
    
    response.set_cookie(key="Manish",value=token['cookie'], httponly=True,secure=settings.SECURITYHHTPS, samesite=settings.SAMESITE)
    
    return ({"msg":"login Successfull"})#,"Manish":token['cookie']})

@app.get("/getrole")
def getrole(Manish:Optional[str] = Cookie(None)):
    return(login.getrole(Manish))


@app.put("/logout")
def logout(response:Response):
    response.delete_cookie("Manish")
    response.set_cookie(key="Manish",value="a", httponly=True,secure=settings.SECURITYHHTPS, samesite=settings.SAMESITE)
    return({"msg":"logout successfull"})

@app.post("/changepassword")
def changepassword(user:login.Changepassword,Manish:Optional[str] = Cookie(None)):
    return(login.changepassword(user,Manish))
#login------------------------------------------------------------------

# Books-----------------------------------------------------------------

@app.post("/book/insertbook")
def insertbook(books:book.Insertbook,Manish:Optional[str]=Cookie(None)):
    return(book.insertbook(books,Manish))

# Books-----------------------------------------------------------------




app = CORSMiddleware(
    app=app,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    #expose_headers= ["*"],
)