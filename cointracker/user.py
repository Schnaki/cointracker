import pymongo

def add_coin(user_id, data):
    pymongo.update_one({'_id': user_id, {'$addToSet': {'coins': {'name': data['name'], 'amount': data['amount']}}}})
    

