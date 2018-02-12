import json
from bson import ObjectId

def add_coin(db, user_id, data):
    try:
        db.users.update(
                {'_id': ObjectId(user_id)},
                {'$push': {
                    'coins': {
                        'name': data['name'], 
                        'amount': data['amount']
                        }
                     }
                 }
        )
        return json.dumps({
            'status':'success',
            'message': 'Successfully added coin'
        })
    except Exception as e:
        return json.dumps({
            'status':'fail',
            'message': 'adding coin failed'
        })

