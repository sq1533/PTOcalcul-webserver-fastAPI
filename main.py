import os
import pandas as pd
import re
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import calcul

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__),"templates"))

#mainPage
@app.get("/home",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse("HCM.html",{"request":request})

class lookUp(BaseModel):
    number:int

#조회
@app.post("/user{lookUp}")
async def lookUp(request:Request,response:lookUp):
    user = calcul.aboutPTO(response.number)
    html_content = f"{calcul.usedPTO(worker=user.usedPTO)}"
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8081)