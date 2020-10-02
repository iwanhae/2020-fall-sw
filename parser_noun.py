import pymongo
mongoUri = 'mongodb://{id}:{pw}@{endpoint}/{db}?authSource={db}'
client = pymongo.MongoClient(
    mongoUri.format(
        id="2020sw",
        pw="changeme",
        endpoint="doctor.iptime.org",
        db="2020sw"
    ))
db = client.get_database()

print("Available collections:")
for c in db.list_collection_names():
    print("\t", c, db.get_collection(c).estimated_document_count())


# %%
col = db.get_collection("articles")
col.update_many({"status": { "$exists":False }}, {"$set": {"status": 0}})
col.create_index([("status", pymongo.DESCENDING)])


# %%
from konlpy.tag import Kkma
km = Kkma()


# %%
col = db.get_collection("articles")
while True:
    doc = col.find_one_and_update({"status" : 0}, {"$set": {"status": 1}})
    keywords = {}
    for noun in km.nouns(doc['body']):
        if len(noun) < 2:
            continue
        if noun not in keywords:
            keywords[noun] = 0
        keywords[noun] += 1
    col.find_one_and_update({"_id": doc["_id"]}, {"$set": {"status": 2, "keywords": keywords}})
    print(doc['link'], doc['title'])
