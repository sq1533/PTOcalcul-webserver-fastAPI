import os
import requests
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
async def HOME(request:Request):
    return templates.TemplateResponse(name="HCM.html",context={"request":request})

@app.post("/lookup")
async def read_number(request: Request):
    data = await request.form()
    return {"message":"Hello,"+data["number"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)