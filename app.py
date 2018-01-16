import json
import requests
from flask import Flask
from flask import render_template
from flask import request
app = Flask (__name__)


API_ENDPOINT = "https://api.coinmarketcap.com/v1/ticker/"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/coins")
def get_coin_prices():
    coins = json.loads(request.args.get("coins"))
    coin_price = []
    for coin in coins:
        coin_price.append(get_coin_price(coin));
    return json.dumps(coin_price)

def get_coin_price(coin):
    content = requests.get(API_ENDPOINT+coin+"?convert=EUR").content
    return json.loads(content)[0]["price_eur"]
        
