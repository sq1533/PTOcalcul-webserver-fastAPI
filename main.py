import os
import pandas as pd
import re
from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import calcul

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__),"templates"))

#mainPage
@app.get("/home",response_class=HTMLResponse)
async def HOME(request:Request):
    return templates.TemplateResponse(name="HCM.html",context={"request":request})

class User(BaseModel):
    username: str
    password: str

@app.post("/submit_data")
async def create_user(user: User):
    user = user.username
    return {"message": "User created successfully!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8081)