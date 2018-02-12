import json
import requests
import db
import auth
import user
from flask import Flask
from flask import render_template
from flask import request
app = Flask (__name__)



API_ENDPOINT = "https://api.coinmarketcap.com/v1/ticker/"

mydb = db.connect()
db.init(mydb)

@app.route("/api/signup", methods=['POST'])
def signup():
    data = json.loads(request.data)
    return auth.handle_signup(mydb, data)

@app.route("/api/signin", methods=['POST'])
def signin():
    data = json.loads(request.data)
    return auth.handle_signin(mydb, data)

@app.route('/api/add-coin', methods=['GET', 'POST'])
@auth.login_required
def add_coin(user_id):
    data = json.loads(request.data)
    return user.add_coin(mydb, user_id, data)

@app.route("/api/coin")
def get_coin_price():
    coin = request.args.get("coin")
    content = requests.get(API_ENDPOINT+coin+"?convert=EUR").content.decode("utf-8");
    return get_coin_price_helper(coin)

@app.route("/api/coins")
def get_coin_prices():
    coins = json.loads(request.args.get("coins"))
    coin_price = []
    for coin in coins:
        coin_price.append(get_coin_price_helper(coin));
    return json.dumps(coin_price)

def save_available_coin_ids():
    content = requests.get(API_ENDPOINT).content.decode("utf-8");
    parsed = json.loads(content)
    coin_ids = []
    for coin in parsed:
        coin_ids.append(coin["id"])

    coin_ids.sort()
    return coin_ids


COIN_IDS = save_available_coin_ids()

@app.route("/api/coin-ids")
def get_coin_ids():
    return json.dumps(COIN_IDS)

def get_coin_price_helper(coin):
    content = requests.get(API_ENDPOINT+coin+"?convert=EUR").content.decode("utf-8");
    return json.loads(content)[0]["price_eur"]


        
