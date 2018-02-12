import pymongo
import json
import urllib.parse
import datetime
import os

def connect():
    username = urllib.parse.quote_plus(os.getenv("COINTRACKER_USER"))
    password = urllib.parse.quote_plus(os.getenv("COINTRACKER_PASSWORD"))
    client = pymongo.MongoClient("mongodb://%s:%s@127.0.0.1/cointracker" % (username, password))
    return client.cointracker

def init(db):
    db.users.create_index([("username", pymongo.ASCENDING)], unique=True)



