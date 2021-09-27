from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client.Velib

user_position_long = float(input("Enter your position longitude :"))
user_position_lat = float(input("Enter your position latitude :"))

result = db.All.find({   'geometry': {'$near': {'$geometry': {'type': "Point", 'coordinates': [ user_position_long, user_position_lat ]},
                '$maxDistance': 300, '$minDistance': 0}}})

for x in result:
    print(x)