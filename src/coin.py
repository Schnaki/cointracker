import json
import coinmarketcap
import datetime
from util import JSONEncoder
from bson import ObjectId

def add_coin(db, user_id, data):
    try:
        price = coinmarketcap.get_price(data['cmc_id'])
        id = db.coins.insert_one({
            'user_id': ObjectId(user_id),
            'cmc_id': data['cmc_id'],
            'amount': float(data['amount']),
            'price': float(price),
            'total': float(data['amount']) * price,
            'created': datetime.datetime.utcnow(),
            'updated': datetime.datetime.utcnow()
        }).inserted_id

        db.users.update(
            {'_id': ObjectId(user_id)},
            {'$inc': {'total': float(data['amount']) * price}}
        )
        return JSONEncoder().encode({
            'status': 'success',
            'message': 'Successfully added coin',
            'id': id
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'status': 'fail',
            'message': 'adding coin failed'
        })


def update_coin(db, user_id, data):
    try:
        coin = db.coins.find_one({'_id': ObjectId(data['id'])})
        if ObjectId(user_id) != coin['user_id']:
            raise Exception('wrong user')

        total_diff = (float(data['amount']) - float(coin['amount'])) * float(coin['price'])

        db.users.update(
            {'_id': ObjectId(user_id)},
            {'$inc': {'total': total_diff}}
        )
        db.coins.update(
                {'_id': ObjectId(data['id'])},
                {
                    '$set': {
                        'amount': data['amount'],
                        'total': float(data['amount']) * coin['price']
                    }
                }
        )
        return json.dumps({
            'status': 'success',
            'message': 'Successfully updated coin'
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'status': 'fail',
            'message': 'updating coin failed'
        })



def remove_coin(db, user_id, data):
    try:
        coin = db.coins.find_one({'_id': ObjectId(data['id'])})
        if ObjectId(user_id) != coin['user_id']:
            raise Exception('wrong user')

        db.coins.remove({
            '_id': ObjectId(data['id'])
        })
        db.users.update(
            {'_id': ObjectId(user_id)},
            {'$inc': {'total': -coin['total']}}
        )
        return json.dumps({
            'status': 'success',
            'message': 'Successfully removed coin'
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'status': 'fail',
            'message': 'removing coin failed'
        })

def get_coin(db, id):
    try:
        coin = db.coins.find_one({'_id': ObjectId(id)})
        return JSONEncoder().encode({
            'status': 'success',
            'message': 'Successfully got coin',
            'coin': coin
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'status':'fail',
            'message': 'getting coin failed'
        })


def get_coins(db, user_id):
    try:
        coins = list(db.coins.find({'user_id': ObjectId(user_id)}))
        return JSONEncoder().encode({
            'status': 'success',
            'message': 'Successfully got coins',
            'coins': coins
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'status':'fail',
            'message': 'getting coins failed'
        })
