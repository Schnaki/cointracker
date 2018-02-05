import pymongo
import json
import urllib.parse
import datetime

def connect():
    f = open("config/auth.json", "r")
    parsed = json.loads(f.read())
    username = urllib.parse.quote_plus(parsed["username"])
    password = urllib.parse.quote_plus(parsed["password"])
    client = pymongo.MongoClient("mongodb://%s:%s@127.0.0.1/cointracker" % (username, password))
    return client.cointracker

def init(db):
    db.users.create_index([("username", pymongo.ASCENDING)], unique=True)



