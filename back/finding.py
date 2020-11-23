from db import getCol, getDB
from datetime import datetime, timedelta
import time

# 1, 0, -1 로 변환된 두 데이터의 유사도를 비교하는 함수 클수록 유사도가 높음


def compData(keyResult, userResult):
    compResult = 0
    for i in range(len(userResult)):
        if keyResult[i] == userResult[i]:
            compResult += 1
    return compResult

# 특정 키워드의 랭크 리스트값을 받아서 증감수치로만 변환해주는 함수


def calVariance(data):
    result = [0]
    for i in range(1, len(data)):
        if data[i] == data[i-1]:
            result.append(0)
        elif data[i] > data[i-1]:
            result.append(1)
        else:
            result.append(-1)
    return result


def fetchKeywords(since: datetime, until: datetime) -> {}:
    db = getDB()
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
    return data


def movingmean(d, size=3):
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


def sync(doc):
    col = getCol()
    return col.find_one_and_update({"_id": doc["_id"]}, {"$set": doc})


def finding_related():
    col = getCol()
    print("finding related 시작")
    while True:
        doc = col.find_one({"finished": {"$in": [None]}})
        if doc == None:
            print("[finding related] 찾은게 없어요")
            time.sleep(1)  # 작업할게 없으면 1초 뒤 다시확인
            continue

        since = doc['meta']['from']
        until = doc['meta']['to']
        doc["finished"] = False
        doc["status"]["total"] = (until - since).days
        doc["status"]["current"] = 0
        doc["status"]["message"] = "데이터를 불러오는 중입니다."
        sync(doc)
        ########
        # Fetch data
        ########
        db = getDB()
        col_rank = db.get_collection("ranked")
        keywords = {}
        length = (until - since).days + 1
        start = time.time()
        for rank_doc in col_rank.find({
            'status': 2,
            'date': {
                '$gte': since,
                '$lte': until
            }
        }):
            date = rank_doc['date']
            delta = (date - since).days
            for keyword in rank_doc['keywords']:
                key = keyword['name']
                if key not in keywords:
                    keywords[key] = [0 for i in range(length)]
                keywords[key][delta] = keyword['rank']
            doc["status"]["current"] += 1
            if time.time() - start > 1:
                start = time.time()
                sync(doc)
        ########
        # Data Conversion
        ########
        data_req = list(map(lambda x: x['value'], doc['data']))
        ########
        # Compare data
        ########
        related_keys = []
        doc['status']['total'] = len(keywords)
        doc['status']['current'] = 0
        doc["status"]["message"] = "데이터를 비교해보는 중입니다."
        sync(doc)
        start = time.time()
        for key in keywords:
            data_cmp = movingmean(keywords[key], 7)  # db에 있는 키워드 주단위로 분석
            similarity = 1 - (compData(calVariance(data_cmp),
                                       calVariance(data_req)) / len(data_req))
            related_keys.append((key, similarity))
            doc["status"]["current"] += 1
            if time.time() - start > 1:
                start = time.time()
                sync(doc)
        ########
        # Sort data
        ########
        doc['status']['total'] = 2
        doc['status']['current'] = 0
        doc["status"]["message"] = "거의 완료되었습니다."
        doc["related"] = []
        sync(doc)
        related_keys.sort(key=lambda x: x[1])  # 키워드 유사도 오름차순
        for i in range(0, 20):  # 키워드 20개 뽑아서 저장
            tmp = []
            d = doc['meta']['from']
            for val in keywords[related_keys[i][0]]:
                tmp.append({
                    'date': d,
                    'value': val
                })
                d += timedelta(1)
            doc["related"].append({
                "keyword": related_keys[i][0],
                "similarity": related_keys[i][1],
                "data": tmp
            })
        doc['status']['total'] = 2
        doc['status']['current'] = 2
        doc["status"]["message"] = "완료되었습니다. :-)"
        sync(doc)
