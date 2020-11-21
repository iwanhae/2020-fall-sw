import pymongo
from datetime import datetime, timedelta

# TASK Collection에 들어가는 문서 형태
document = {
    "status": {
        # 사용자에게 보여줄 진행상황
        "total": 0,
        "current": 0,
        "message": "string"
    },
    "meta": {
        # 데이터의 시작날짜와 끝 날짜
        "from": datetime,
        "to": datetime,
    },
    "data": [
        {
            "date": datetime,
            "value": 0,
        }
    ],
    "related": [
        {
            "keyword": "키워드",
            "similarity": 0.0,
            "data": [
                {
                    "date": datetime,
                    "value": 0,
                }
            ]
        }
    ]
}


def getDB() -> pymongo.database.Database:
    mongoUri = 'mongodb://{id}:{pw}@{endpoint}/{db}?authSource={db}'
    client = pymongo.MongoClient(
        mongoUri.format(
            id="2020sw",
            pw="changeme",  # os.environ['MONGO_PW'],
            endpoint="iwanhae.iptime.org",
            db="2020sw"
        ))
    db = client.get_database()
    return db


def getCol() -> pymongo.collection.Collection:
    db = getDB()
    return db.get_collection("task")
