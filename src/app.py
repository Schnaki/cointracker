import json
import db
import auth
import coin
import coinmarketcap
import user
import timed
from flask import Flask
from flask import request
app = Flask(__name__)

mydb = db.connect()
db.init(mydb)

timed.update_coins(mydb)
timed.save_total(mydb)

@app.route("/api/signup", methods=['POST'])
def signup():
    data = json.loads(request.data.decode('utf-8'))
    return auth.handle_signup(mydb, data)

@app.route("/api/login", methods=['POST'])
def login():
    data = json.loads(request.data.decode('utf-8'))
    return auth.handle_login(mydb, data)

@app.route('/api/get-total', methods=['GET'])
@auth.login_required
def get_total(user_id):
    return user.get_total(mydb, user_id)

@app.route('/api/add-coin', methods=['POST'])
@auth.login_required
def add_coin(user_id):
    data = json.loads(request.data.decode('utf-8'))
    return coin.add_coin(mydb, user_id, data)

@app.route('/api/update-coin', methods=['POST'])
@auth.login_required
def update_coin(user_id):
    data = json.loads(request.data.decode('utf-8'))
    return coin.update_coin(mydb, user_id, data)

@app.route('/api/remove-coin', methods=['POST'])
@auth.login_required
def remove_coin(user_id):
    data = json.loads(request.data.decode('utf-8'))
    return coin.remove_coin(mydb, user_id, data)

@app.route('/api/get-coins', methods=['GET'])
@auth.login_required
def get_coins(user_id):
    return coin.get_coins(mydb, user_id)

@app.route('/api/get-coin', methods=['GET'])
@auth.login_required
def get_coin(user_id):
    return coin.get_coin(mydb, request.args.get('id'))

CMC_IDS = coinmarketcap.get_coin_ids()

@app.route("/api/cmc-ids")
def get_coin_ids():
    return json.dumps(CMC_IDS)



        
