from typing import List, Optional
from fastapi import FastAPI,Cookie
from app import login,book, report

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

@app.get("/getusername")
def getusername(Manish:Optional[str] = Cookie(None)):
    return(login.getusername(Manish))

@app.put("/logout")
def logout(response:Response):
    response.delete_cookie("Manish")
    response.set_cookie(key="Manish",value="a", httponly=True,secure=settings.SECURITYHHTPS, samesite=settings.SAMESITE)
    return({"msg":"logout successfull"})

@app.post("/changepassword")
def changepassword(user:login.Changepassword,Manish:Optional[str] = Cookie(None)):
    return(login.changepassword(user,Manish))

@app.post("/get_user_details")
def getuser_details(response:Response,user:login.User_details,Manish:Optional[str] = Cookie(None)):
    return(login.getuser_details(response,user,Manish)) 

@app.post("/get_user_details_by_id")
def getuser_details(response:Response,user:login.Individual_user,Manish:Optional[str] = Cookie(None)):
    return(login.getuser_details_by_id(response,user,Manish)) 

@app.post("/modify_user_details_by_id")
def modify_user_details(response:Response,user:login.Modify_user,Manish:Optional[str] = Cookie(None)):
    return(login.modify_user_details_by_id(response,user,Manish)) 

@app.post("/disable_account")
def modify_user_details(response:Response,Manish:Optional[str] = Cookie(None)):
    return(login.disable_account(response,Manish)) 
#login------------------------------------------------------------------

# Books-----------------------------------------------------------------
app.include_router(book.router)
# Books-----------------------------------------------------------------
#Report-----------------------------------------------------------------
app.include_router(report.router)
#Report-----------------------------------------------------------------


app = CORSMiddleware(
    app=app,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    #expose_headers= ["*"],
)