import os
import pandas as pd  # Assuming you need pandas for data processing
import re  # Assuming you need re for data processing
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# MainPage
@app.get("/home", response_class=HTMLResponse)
async def HOME(request: Request):
    return templates.TemplateResponse(name="HCM.html",context={"request":request})

@app.get("/{LOOKUP}")
async def read_item(request: Request,LOOKUP:str):
    test = LOOKUP+"123"
    return {"LOOKUP":test}

class User(BaseModel):
    username: str

@app.post("/submit")
async def create_user(request: Request, user: User = Form(...)):
    return {"message": f"Hello, {user.username}!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)