# %%
import os
import pymongo
mongoUri = 'mongodb://{id}:{pw}@{endpoint}/{db}?authSource={db}'
client = pymongo.MongoClient(
    mongoUri.format(
        id="2020sw",
        pw=os.environ['MONGO_PW'],
        endpoint="doctor.iptime.org",
        db="2020sw"
    ))
db = client.get_database()

print("Available collections:")
for c in db.list_collection_names():
    print("\t", c, db.get_collection(c).estimated_document_count())

# %%
import numpy as np
from numba import jit

@jit
def execRound(key_ndarray, lastRank, edgeSum):
    size=len(key_ndarray[0])
    newWeight=lastRank
    DF=0.85
    for i in range(size):
        pr=0.0        
        for j in range(size):
            if (key_ndarray[i][j]==0): continue
            else :
                pr+=(lastRank[j]/edgeSum[j])

        newWeight[i]=((1-DF)/size)+(DF*pr)
    return newWeight

def PageRank(dataSet):
    datalist=[]
    for doc in dataSet:
        datalist.append(doc)
    keyword_dict=dict()
    count=0
    for doc in datalist:
        for j in doc['keywords']:
            if(j['name'] not in keyword_dict):
                keyword_dict[j['name']]=count
                count+=1
    key_list=[]
    for i in keyword_dict:
        key_list.append(i)
    nodeNum=len(key_list)
    key_ndarray=np.zeros((nodeNum,nodeNum))
    pageRank=np.full(nodeNum,1/nodeNum)
    
    for doc in datalist:
        for j in doc['keywords']:
            init_name=j['name']
            for k in doc['keywords']:
                comp_name=k['name']
                if(init_name==comp_name):
                    continue
                key_ndarray[keyword_dict[init_name]][keyword_dict[comp_name]]=1
                key_ndarray[keyword_dict[comp_name]][keyword_dict[init_name]]=1


    edgeSum=key_ndarray[0]
    for i in range(nodeNum):
        edgeSum[i]=key_ndarray[i].sum()
    total = 2.0
    while total > 1.1:
        pageRank=execRound(key_ndarray,pageRank,edgeSum)
        total = pageRank.sum() 
    Rank_list=[]
    for i in range(nodeNum):
        Rank_list.append({'name':key_list[i],'rank':pageRank[i] / total}) # 총합을 1.0 으로 normalize
    return Rank_list, total
# %%
from pprint import pprint
articles = db.get_collection("articles")
ranked = db.get_collection("ranked")
ranked.update_many({"status" : 1}, {"$set": {"status": 0}})
while True:
    doc = ranked.find_one_and_update({"status": 0}, {"$set": {"status": 1}})
    if doc == None:
        break
    data = list(articles.find({'date':doc['date'], 'status': 3}))
    keywords, total = PageRank(data)
    keywords = sorted(keywords, key=lambda x : x['rank'], reverse=True)
    ranked.find_one_and_update(
        {"_id" : doc['_id']}, 
        {"$set": { 
            "status": 2, 
            "keywords": keywords, 
            "doc_count": len(data),
            "keyword_count": len(keywords),
            "total": total
            }
        })
    pprint({
        "date": doc["date"],
        "doc_count": len(data),
        "keyword_count": len(keywords),
        "total": total
    })
print("Finished!")
# %%
