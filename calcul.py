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
        self.add = info[user]["addPTO"]

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
        pto = todayM - month
    elif workYear == 1:
        if todayM < month:
            pto = 12 + todayM - month
        else:
            pto = (workYear-1)*15 + (12 - month)
    else:
        pto = (workYear-1)*15 + (12 - month)
    return str(pto)

#남은 연차(get)
def leftPTO(tPTO:str,exPTO:str,uPTO:str) -> str:
    left = float(tPTO) + float(exPTO) - float(uPTO)
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

#추가 연차(post)
def extraPTO(worker:aboutPTO,number:str) -> str:
    extra = float(worker.add)
    result = extra + (float(number)*1.5)
    with open(staffInfoPath, 'r', encoding='utf-8') as j:
        workerinfo = json.load(j)
    workerinfo[worker.user]["addPTO"] = str(result)
    with open(staffInfoPath, 'w', encoding='utf-8') as j:
        json.dump(workerinfo, j, ensure_ascii=False, indent=4)
    return str(result)

#연차 사용 취소(post)
def cancelPTO(worker:aboutPTO,number:str) -> str:
    usedPTO = float(worker.usedPTO)
    result = usedPTO - float(number)
    with open(staffInfoPath, 'r', encoding='utf-8') as j:
        workerinfo = json.load(j)
    workerinfo[worker.user]["usedPTO"] = str(result)
    with open(staffInfoPath, 'w', encoding='utf-8') as j:
        json.dump(workerinfo, j, ensure_ascii=False, indent=4)
    return str(result)