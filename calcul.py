from datetime import datetime

example = {
    21093001 : 
    {
        "name":"서동규",
        "join":"2021-09-30",
        "usedPTO":"1",
        "addPTO":"3"
    }
}

#연차 계산기
class aboutPTO:
    #데이터 정의
    def __init__(self,user):
        self.name = example[user]["name"]
        self.join = example[user]["join"]
        self.usedPTO = example[user]["usedPTO"]
        self.add = example[user]["addPTO"]

#입사 후 전체 연차
def totalPTO(join:aboutPTO,addPTO:aboutPTO) -> int:
    today = datetime.now()
    join = join.split("-")
    year = int(join[0])
    month = int(join[1])
    workYear = int(today.strftime('%Y')) - year
    if workYear == 0:
        pto = int(today.strftime('%m')) - month + int(addPTO)
    else:
        pto = (workYear-1)*15 + (12 - month) + int(addPTO)
    return pto

#사용 연차
def usedPTO(worker:aboutPTO) -> int:
    return int(worker)

#남은 연차
def leftPTO(tPTO:totalPTO,uPTO:usedPTO) -> int:
    left = tPTO - uPTO
    return left