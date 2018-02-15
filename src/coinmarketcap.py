import json
import requests

API_ENDPOINT = "https://api.coinmarketcap.com/v1/ticker/"


def get_price(coin):
    content = requests.get(API_ENDPOINT+coin).content.decode("utf-8");
    return float(json.loads(content)[0]['price_usd'])

def get_coin_ids():
    content = requests.get(API_ENDPOINT).content.decode("utf-8");
    parsed = json.loads(content)
    coin_ids = []
    for coin in parsed:
        coin_ids.append(coin["id"])
    coin_ids.sort()
    return coin_ids

