import os
import json
from datetime import datetime
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import calcul

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

#근무자 정보 path
staffInfoPath = os.path.join(os.path.dirname(__file__),"DB","staffInfo.json")

#MainPage
@app.get("/home",response_class=HTMLResponse)
async def HOME(request:Request):
    return templates.TemplateResponse(name="HCM.html",context={"request":request})

#당일 날짜
@app.get("/today")
async def today():
    today = datetime.now().strftime('%Y-%m')
    return Response(content=f"{today}")

#form태그 데이터 post
@app.post("/lookup")
async def read_number(request:Request):
    data = await request.form()
    with open(staffInfoPath, 'r', encoding='utf-8') as j:
        workerinfo = json.load(j)
    if data["name"] not in list(workerinfo.keys()):
        return Response(content="근무자 이름이 잘못되었습니다.")
    else:
        user = calcul.aboutPTO(data["name"])
        userName = calcul.aboutPTO(data["name"]).user
        userUsedPTO = calcul.aboutPTO(data["name"]).usedPTO
        workHolyday = calcul.aboutPTO(data["name"]).workHoly
        userTotalPTO = calcul.totalPTO(info=user)
        userleftPTO = calcul.leftPTO(tPTO=userTotalPTO,exPTO=workHolyday,uPTO=userUsedPTO)
        results = f"근무자 : {userName}<br>남은연차 : {userleftPTO}일<br>공휴일 근무 : {workHolyday}일<br>사용 연차 : {userUsedPTO}일"
        return templates.TemplateResponse(request=request,name="output.html",context={"results":results,"name":userName})

#연차 사용 처리
@app.post("/usingPTO")
async def using(request:Request):
    data = await request.form()
    with open(staffInfoPath, 'r', encoding='utf-8') as j:
        workerinfo = json.load(j)
    if data["name"] not in list(workerinfo.keys()):
        return Response(content="근무자 이름이 잘못되었습니다.")
    elif data["time"] == "":
        return Response(content="연차 사용일자를 적어주세요.")
    else:
        user = calcul.aboutPTO(data["name"])
        results = calcul.addUsedPTO(worker=user,data=data["time"])
        return Response(content=results)

#추가 연차 반영
@app.post("/addPTO")
async def add(request:Request):
    data = await request.form()
    with open(staffInfoPath, 'r', encoding='utf-8') as j:
        workerinfo = json.load(j)
    if data["name"] not in list(workerinfo.keys()):
        return Response(content="근무자 이름이 잘못되었습니다.")
    elif data["add"] == "":
        return Response(content="공휴일 근무 일자를 입력해주세요.")
    else:
        user = calcul.aboutPTO(data["name"])
        results = calcul.workHolyday(worker=user,number=data["add"])
        return Response(content=results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)