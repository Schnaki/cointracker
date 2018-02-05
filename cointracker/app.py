import json
import requests
import db
import auth
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/add-coin', methods=['GET', 'POST'])
@auth.login_required
def add_coin(user_id):
    data = json.loads(request.data)
    return user_id

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

@app.route("/api/coin-ids")
def get_coin_ids():
    f = open("config/coin_ids.json", "r")
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
    
    f = open("config/coin_ids.json", "w+")
    f.write(json.dumps(coin_ids))
    f.close()


save_available_coin_ids()
        
