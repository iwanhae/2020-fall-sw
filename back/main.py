from bottle import Bottle, run, request, response, static_file
from multiprocessing import Process, Queue
from datetime import datetime, timedelta
from db import getCol, getDB
from finding import finding_related
from bson.objectid import ObjectId
from processBody import processBody
import json
import hashlib


app = Bottle()


@app.route('/ping')
def ping():
    db = getDB()
    cols = db.list_collection_names()
    return {"ping": "pong", "collections": cols}


@app.route('/request', method='POST')
def handleRequest():
    # body = {
    #    "data": [
    #        {
    #            "date": "string",
    #            "value": 0,
    #        }
    #    ]
    # }
    body = json.load(request.body)  # 들어온 요청

    # 이제 이걸 채워줘야함
    document = {
        "status": {
            # 사용자에게 보여줄 진행상황
            "total": 0,
            "current": 0,
            "message": "string"
        },
        "meta": {
            # 데이터의 시작날짜와 끝 날짜
            "from": datetime(2020, 1, 1),
            "to": datetime(2020, 1, 1),
        },
        "data": [
            # 비교 요청받은 데이터
            {
                "date": datetime(2020, 1, 1),
                "value": 0,
            }
        ],
        "related": [
            {
                # 찾아낼 값
                "keyword": "키워드",
                "similarity": 0.0,
                "data": [
                    {
                        "date": datetime(2020, 1, 1),
                        "value": 0,
                    }
                ]
            }
        ]
    }

    body = processBody(body)
    document["status"]["total"] = 1
    document["status"]["message"] = "요청처리 대기중입니다."

    # TODO: document["meta"] 채워주기
    document["meta"]["from"] = body[0]["date"]
    document["meta"]["to"] = body[-1]["date"]

    # TODO: document["data"] 채워주기,
    # 1. 중간중간에 날짜는 있는데 값이 없는 경우가 있으니 해당 값은 중간값으로 넣어주기.
    # 2. date값이 string 형태로 들어오니 date 형태로 파싱하기
    document["data"] = body

    col = getCol()
    res = col.insert_one(document)
    return {'id': str(res.inserted_id)}


@app.route('/progress/<id>', method='GET')
def handleProgress(id):
    col = getCol()
    document = col.find_one({"_id": ObjectId(id)})
    return document["status"]


@app.route('/result/<id>', method='GET')
def handleResult(id):
    col = getCol()
    document = col.find_one({"_id": ObjectId(id)})

    return {
        "from": document["meta"]["from"],
        "to": document["meta"]["to"],
        "data": document["data"],
        "related": document["related"],
    }


@app.route('/<filepath:path>')
def server_static(filepath):
    if filepath.find('.') != -1:
        return static_file(filepath, root='dist')
    else:
        return static_file("index.html", root='dist')


if __name__ == '__main__':
    #col = getCol()
    # col.delete_many({})
    p1 = Process(target=finding_related, args=())
    p1.start()
    run(app, host='0.0.0.0', port=8080)
