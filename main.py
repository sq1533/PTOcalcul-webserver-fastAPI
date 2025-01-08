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

#데이터 폼
class userID(BaseModel):
    number:int

#mainPage
@app.get("/home",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse(name="HCM.html",context={"request":request})

#
@app.get("/home/PTO",response_class=HTMLResponse)
async def home(request:Request,user_id:userID):
    """
    user_pto = calcul.aboutPTO(user_id.number)
    html = f"<div>{calcul.usedPTO(user_pto.usedPTO)}</div>"
    """
    return HTMLResponse(content=123)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8081)