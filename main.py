import os
import json
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import calcul

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

#근무자 정보 path
staffInfoPath = os.path.join(os.path.dirname(__file__),"DB","staffInfo.json")

# MainPage
@app.get("/home",response_class=HTMLResponse)
async def HOME(request:Request):
    return templates.TemplateResponse(name="HCM.html",context={"request":request})

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
        userExtraPTO = calcul.aboutPTO(data["name"]).add
        userTotalPTO = calcul.totalPTO(info=user)
        userleftPTO = calcul.leftPTO(tPTO=userTotalPTO,exPTO=userExtraPTO,uPTO=userUsedPTO)
        results = f"[근무자 : {userName}] [남은연차 : {userleftPTO}]"
        return templates.TemplateResponse(request=request,name="output.html",context={"results":results,"name":userName})

#연차 사용 처리
@app.post("/usingPTO")
async def using(request:Request):
    data = await request.form()
    with open(staffInfoPath, 'r', encoding='utf-8') as j:
        workerinfo = json.load(j)
    if data["name"] not in list(workerinfo.keys()):
        return Response(content="근무자 이름이 잘못되었습니다.")
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
    else:
        user = calcul.aboutPTO(data["name"])
        results = calcul.extraPTO(worker=user,number=data["add"])
        return Response(content=results)

#연차 사용 취소
@app.post("/cancelPTO")
async def cancel(request:Request):
    data = await request.form()
    with open(staffInfoPath, 'r', encoding='utf-8') as j:
        workerinfo = json.load(j)
    if data["name"] not in list(workerinfo.keys()):
        return Response(content="근무자 이름이 잘못되었습니다.")
    else:
        user = calcul.aboutPTO(data["name"])
        results = calcul.cancelPTO(worker=user,number=data["cancel"])
        return Response(content=results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)