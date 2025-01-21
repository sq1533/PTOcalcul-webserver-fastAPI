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
        results = f"근무자 : {userName}<br>남은연차 : {userleftPTO}일<br>공휴일 근무 : 총 {len(workHolyday)}일<br>사용 연차 : {userUsedPTO}일"
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
        return Response(content="공휴일 근무 일자를 선택해주세요.")
    else:
        user = calcul.aboutPTO(data["name"])
        calcul.ADDworkHolyday(worker=user,date=data["add"])
        return Response(content=f"{data["add"]} 추가 완료")

#추가 연차 제거
@app.post("/removePTO")
async def add(request:Request):
    data = await request.form()
    with open(staffInfoPath, 'r', encoding='utf-8') as j:
        workerinfo = json.load(j)
    if data["name"] not in list(workerinfo.keys()):
        return Response(content="근무자 이름이 잘못되었습니다.")
    elif data["remove"] == "":
        return Response(content="공휴일 근무 일자를 선택해주세요.")
    else:
        user = calcul.aboutPTO(data["name"])
        calcul.REMOVEworkHolyday(worker=user,date=data["remove"])
        return Response(content=f"{data["remove"]} 삭제 완료")

#공휴일 근무날짜 조회
@app.post("/lookupWorkHolyday")
async def lookHolyday(request:Request):
    data = await request.form()
    with open(staffInfoPath, 'r', encoding='utf-8') as j:
        workerinfo = json.load(j)
    if data["name"] not in list(workerinfo.keys()):
        return Response(content="근무자 이름이 잘못되었습니다.")
    else:
        html_content = "<div>"
        for item in calcul.aboutPTO(data["name"]).workHoly:
            html_content += f"{item}<br>"
        html_content += "</div>"
        return Response(content=html_content)

#신규입사자 데이터 추가
@app.post("/joinNew")
async def lookHolyday(request:Request):
    data = await request.form()
    with open(staffInfoPath, 'r', encoding='utf-8') as j:
        workerinfo = json.load(j)
    if data["name"] == "":
        return Response(content="근무자 이름 없음")
    elif data["name"] in list(workerinfo.keys()):
        return Response(content="근무자 중복")
    elif data["join"] == "":
        return Response(content="입사 날짜를 입력해주세요.")
    else:
        workerinfo[data["name"]] = {"join":data["join"],"usedPTO":"0","workHolyday":[]}
        with open(staffInfoPath, 'w', encoding='utf-8') as j:
            json.dump(workerinfo, j, ensure_ascii=False, indent=4)
        return Response(content="근무자 추가 완료")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)