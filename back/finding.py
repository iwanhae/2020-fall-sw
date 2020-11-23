from db import getCol, getDB
from datetime import datetime, timedelta
import time

def fetchKeywords(since : datetime, until : datetime) -> {}:
    col = db.get_collection("ranked")
    data = {}
    length = (until - since).days + 1
    for doc in col.find({
        'status': 2,
        'date': {
            '$gte': since,
            '$lte': until
        }
    }):
        date = doc['date']
        delta = (date - since).days
        for keyword in doc['keywords']:
            key = keyword['name']
            if key not in data:
                data[key] = [0 for i in range(length)]
            data[key][delta] = keyword['rank']
        print(date)
        clear_output(wait=True)
    return data

def movingmean(d, size = 3):
    data = [0 for i in range(len(d))]
    for i in range(size):
        total = 0
        for j in range(i + 1):
            total += d[j]
        data[i] = total / (i + 1)
    for i in range(size, len(d)):
        total = 0
        for j in range(size):
            total += d[i-j]
        data[i] = total / size
    return data

def calVariance(data):
    result=[0]
    for i in range(1,len(data)):
        if data[i]==data[i-1]:
            result.append(0)
        elif data[i]>data[i-1]:
            result.append(1)
        else:
            result.append(-1)
    return result

def compData(keyResult, userResult):
    compResult=0
    for i in range(len(userResult)):
        if keyResult[i]==userResult[i]:
            compResult+=1
    return compResult

def finding_related():
    col = getCol()
    print("finding related 시작")
    while True:
        doc = col.find_one({"finished": {"$in": [None]}})
        if doc == None:
            print("[finding related] 찾은게 없어요")
            time.sleep(1)  # 작업할게 없으면 1초 뒤 다시확인
            continue
        doc["finished"] = False
        doc["status"]["total"] = 0
        doc["status"]["current"] = 0
        doc["status"]["message"] = "작업을 시작합니다."
        since = doc["meta"]["from"]
        until = doc["meta"]["to"]
        tmp = fetchKeywords(since, until)
        related_keys = []
        for key in tmp:
            mean1 = movingmean(tmp[key], 7) # db에 있는 키워드 주단위로 분석
            mean2 = movingmean(doc["data"][0]["value"], 7) # 입력한 데이터 주단위로 분석
            similarity = 1 - (compData(calVariance(mean2),calVariance(mean1)) / compData(calVariance(mean1),calVariance(mean1)))
            related_keys.append((key, similarity))
            doc["status"]["total"] = len(keywords)
            doc["status"]["current"] += 1
            if(doc["status"]["current"] % 50 == 0): #50개씩 작업되고 있다고 보여줌
                col.find_one_and_update({"_id": doc["_id"]}, {"$set": doc})
        related_keys.sort(key=lambda x:x[1]) #키워드 유사도 오름차순
        for i in range(0, 20): #키워드 20개 뽑아서 저장
            doc["related"].append({
                "keyword": related_keys[i][0],
                "similarity": related_keys[i][1],
                "data": [
                    {
                    "date": doc["data"][0]["date"],
                    "value": doc["data"][0]["value"],
                    }
                ]
            })
        col.find_one_and_update({"_id": doc["_id"]}, {"$set": doc})
