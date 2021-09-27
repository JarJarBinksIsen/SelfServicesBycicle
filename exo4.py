from pymongo import MongoClient
from pprint import pprint


client = MongoClient('mongodb://localhost:27017/')
db = client.Velib

search = input("Search a station by name :")

results = db.All.find({'name':{'$regex':search}})

for result in results:
    print(result)

update = db.All.update_one( {'name':nom},
                            {'$set':{'name':newName}})