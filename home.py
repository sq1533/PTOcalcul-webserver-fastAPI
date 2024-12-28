from datetime import datetime
#연차 계산기
def PTO(worker:dict):
    year = int(worker["Year"])
    month = int(worker["Month"])
    day = int(worker["Day"])
    usedPTO = int(worker["Used"])
    workYear = int(datetime.now().strftime('%Y')) - year
    if workYear == 0:
        pto = int(datetime.now().strftime('%m')) - month
    else:
        pto = (workYear-1)*15 + (12 - month)