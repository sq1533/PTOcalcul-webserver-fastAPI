import os
import json
from datetime import datetime

#DB데이터 경로
staffInfoPath = os.path.join(os.path.dirname(__file__),"DB","staffInfo.json")

#연차 계산기
class aboutPTO:
    #데이터 정의
    def __init__(self,user):
        with open(staffInfoPath, 'r', encoding='utf-8') as f:
            info = json.load(f)
        self.user = user
        self.join = info[user]["join"]
        self.usedPTO = info[user]["usedPTO"]
        self.workHoly = info[user]["workHolyday"]

#입사 후 전체 연차(get)
def totalPTO(info:aboutPTO) -> str:
    today = datetime.now()
    todayY = float(today.strftime('%Y'))
    todayM = float(today.strftime('%m'))
    join = info.join.split("-")
    year = float(join[0])
    month = float(join[1])
    workYear = todayY - year
    if workYear == 0:
        pto = (todayM - month)
    elif workYear == 1:
        pto = 12 + (12 - month)
    elif workYear == 2:
        pto = 15 + 12 + (12 - month)
    elif  workYear == 3:
        pto = 2*15 + 12 + (12 - month)
    elif workYear == 4:
        pto = 16 + 2*15 + 12 + (12 - month)
    elif workYear == 5:
        pto = 2*16 + 2*15 + 12 + (12 - month)
    else:
        pto = (workYear-5)*17 + 2*16 + 2*15 + 12 + (12 - month)
    return str(pto)

#남은 연차(get)
def leftPTO(tPTO:str,exPTO:str,uPTO:str) -> str:
    left = float(tPTO) + (len(exPTO)*1.5) - float(uPTO)
    return str(left)

#사용 연차 누계(post)
def addUsedPTO(worker:aboutPTO,data:str) -> str:
    used = float(worker.usedPTO)
    result = used + float(data)
    with open(staffInfoPath, 'r', encoding='utf-8') as j:
        workerinfo = json.load(j)
    workerinfo[worker.user]["usedPTO"] = str(result)
    with open(staffInfoPath, 'w', encoding='utf-8') as j:
        json.dump(workerinfo, j, ensure_ascii=False, indent=4)
    return str(result)

#날짜 데이터 처리
def str_to_date(dateData):
    return datetime.strptime(dateData,"%Y-%m-%d")

#공휴일 근무 날짜 추가
def ADDworkHolyday(worker:aboutPTO,date:str) -> list:
    with open(staffInfoPath, 'r', encoding='utf-8') as j:
        workerinfo = json.load(j)
    typeSet = set(workerinfo[worker.user]["workHolyday"])
    typeSet.add(date)
    result = sorted(list(typeSet),key=str_to_date,reverse=True)
    workerinfo[worker.user]["workHolyday"] = result
    with open(staffInfoPath, 'w', encoding='utf-8') as j:
        json.dump(workerinfo, j, ensure_ascii=False, indent=4)
    return result

#공휴일 근무 날짜 추가
def REMOVEworkHolyday(worker:aboutPTO,date:str) -> list:
    with open(staffInfoPath, 'r', encoding='utf-8') as j:
        workerinfo = json.load(j)
    typeSet = set(workerinfo[worker.user]["workHolyday"])
    typeSet.discard(date)
    result = sorted(list(typeSet),key=str_to_date,reverse=True)
    workerinfo[worker.user]["workHolyday"] = result
    with open(staffInfoPath, 'w', encoding='utf-8') as j:
        json.dump(workerinfo, j, ensure_ascii=False, indent=4)
    return worker.workHoly