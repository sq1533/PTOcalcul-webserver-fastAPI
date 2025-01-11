import os
import pandas as pd  # Assuming you need pandas for data processing
import re  # Assuming you need re for data processing
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import calcul

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# MainPage
@app.get("/home",response_class=HTMLResponse)
async def HOME(request:Request):
    return templates.TemplateResponse(name="HCM.html",context={"request":request})

#form태그 데이터 post
@app.post("/lookup")
async def read_number(request:Request):
    data = await request.form()
    return data

#연차 사용 처리
@app.post("/usingPTO")
async def using(request:Request):
    data = await request.form()
    user = calcul.aboutPTO(data["number"])
    results = calcul.addUsedPTO(worker=user,data=data["time"])
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)