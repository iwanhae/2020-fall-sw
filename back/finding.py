from db import getCol, getDB
import time


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
        doc["status"]["total"] = 2
        doc["status"]["current"] = 1
        doc["status"]["message"] = "작업을 시작합니다."
        col.find_one_and_update({"_id": doc["_id"]}, {"$set": doc})
