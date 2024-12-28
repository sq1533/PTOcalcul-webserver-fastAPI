from datetime import datetime

example ={
    "name":"서동규",
    "join":"2021-09-30",
    "usedPTO":"24"
    }

#연차 계산기
class aboutPTO:
    #데이터 정의
    def __init__(self):
        self.worker = example
    #입사 후 토탈 연차
    def PTO(self):
        join = self.worker["join"].split("-")
        year = int(join[0])
        month = int(join[1])
        day = int(join[2])
        workYear = int(datetime.now().strftime('%Y')) - year
        if workYear == 0:
            pto = int(datetime.now().strftime('%m')) - month
        else:
            pto = (workYear-1)*15 + (12 - month)
        return pto
    #남은 연차
    def leftPTO(self):
        left = self.PTO() - int(example["usedPTO"])
        return left

PTO = aboutPTO()
print(PTO.leftPTO())