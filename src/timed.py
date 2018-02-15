import coinmarketcap
import datetime
import threading


def update_coins(db):
    threading.Timer(60.0, update_coins, [db]).start()
    try:
        coin_prices = coinmarketcap.get_prices()
        coins = db.coins.find({})
        for coin in coins:
            price = coin_prices[coin['cmc_id']]
            db.coins.update(
                    {'_id': coin['_id']},
                    {
                        '$set': {
                            'price': price,
                            'total': float(coin['amount']) * price
                        }
                    }
            )
        users = db.users.find({})
        for user in users:
            total = 0
            user_coins = db.coins.find({'user_id': user['_id']})
            for uc in user_coins:
                total += uc['total']

            db.users.update({'_id': user['_id']}, {'$set': {'total': total}})

    except Exception as e:
        print(e)


def save_total(db):
    threading.Timer(3600.0, update_coins, [db]).start()
    try:
        users = db.users.find({})
        for user in users:
            db.users.update({'_id': user['_id']}, {'$push': {
                'total_history': {
                    'datetime': datetime.datetime.utcnow(),
                    'total': user['total']
                }
            }})
    except Exception as e:
        print(e)
                    
