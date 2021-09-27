from typing import Collection
from pymongo import MongoClient
from pprint import pprint
import requests
import json
import datetime
from dateutil import parser
import time

client = MongoClient('mongodb://localhost:27017/')
db = client.Velib

def get_veloStations_by_city(url):
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])
    

cities_urls = {
    "lille" : "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion",
    "paris" : "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=3000&facet=etatconnexion"
}

while(1):    
    records = []
    lille_stations = get_veloStations_by_city(cities_urls["lille"])
    for station in lille_stations:
        tempStation = { "name" : station["fields"]["nom"],
                        "city" : "Lille",
                        "geometry" : station["geometry"],
                    "size" : station["fields"]["nbplacesdispo"] + station["fields"]["nbvelosdispo"],
                        "tpe" : station["fields"]["type"],
                        "available" : station["fields"]["etatconnexion"],
                        "date" : parser.parse(station["record_timestamp"])
                        }

        records.append(tempStation)

    paris_stations = get_veloStations_by_city(cities_urls["paris"])

    for station in paris_stations:
        tempStation = { "name" : station["fields"]["name"],
                        "city" : "Paris",
                        "geometry" : station["geometry"],
                        "size" : station["fields"]["capacity"],
                        "tpe" : "",
                        "available" : station["fields"]["is_renting"],
                        "date" : parser.parse(station["record_timestamp"])
                        }
        records.append(tempStation)
        
    db.History.insert_many(records)
    time.sleep(60)


