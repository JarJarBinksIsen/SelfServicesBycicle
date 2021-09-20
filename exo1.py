from typing import Collection
from pymongo import MongoClient
from pprint import pprint
import requests
import json

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



for city_url in cities_urls.values():
    response_by_city = get_veloStations_by_city(city_url)
    for record in response_by_city:
        print(record["fields"])
