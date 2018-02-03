import json
import requests
import urllib.parse
import datetime
import pymongo
from pymongo import MongoClient
from flask import Flask
from flask import render_template
from flask import request
app = Flask (__name__)


API_ENDPOINT = "https://api.coinmarketcap.com/v1/ticker/"

def connect_mongodb():
    f = open("auth.json", "r")
    parsed = json.loads(f.read())
    username = urllib.parse.quote_plus(parsed["username"])
    password = urllib.parse.quote_plus(parsed["password"])
    client = MongoClient("mongodb://%s:%s@127.0.0.1/cointracker" % (username, password))
    return client.cointracker

db = connect_mongodb() 
db.users.create_index([("email", pymongo.ASCENDING)], unique=True)


@app.route("/signup", methods=['POST'])
def signup():
    parsed = json.loads(request.data)
    email = parsed["email"]
    password = parsed["password"]
    user = {"email": email, "password": password, "date": datetime.datetime.utcnow()}
    try:
        db.users.insert_one(user) 
        return "success"
    except:
        return "email already exists"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/coin")
def get_coin_price():
    coin = request.args.get("coin")
    content = requests.get(API_ENDPOINT+coin+"?convert=EUR").content.decode("utf-8");
    return get_coin_price_helper(coin)

@app.route("/coins")
def get_coin_prices():
    coins = json.loads(request.args.get("coins"))
    coin_price = []
    for coin in coins:
        coin_price.append(get_coin_price_helper(coin));
    return json.dumps(coin_price)

@app.route("/coin-ids")
def get_coin_ids():
    f = open("coin_ids.json", "r")
    return f.read()

def get_coin_price_helper(coin):
    content = requests.get(API_ENDPOINT+coin+"?convert=EUR").content.decode("utf-8");
    return json.loads(content)[0]["price_eur"]

def save_available_coin_ids():
    content = requests.get(API_ENDPOINT).content.decode("utf-8");
    parsed = json.loads(content)
    coin_ids = []
    for coin in parsed:
        coin_ids.append(coin["id"])

    coin_ids.sort()
    
    f = open("coin_ids.json", "w+")
    f.write(json.dumps(coin_ids))
    f.close()


save_available_coin_ids()
        
