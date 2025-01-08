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

class lookup(BaseModel):
    number : str

#mainPage
@app.get("/home",response_class=HTMLResponse)
async def HOME(request:Request):
    return templates.TemplateResponse(name="HCM.html",context={"request":request})

#연차 조회
@app.get("/user/")
async def LOOKUP(ID:lookup):
    return {"number": ID.number}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8081)