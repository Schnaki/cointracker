import json
from bson import ObjectId

def get_total(db, user_id):
    try:
        user = db.users.find_one({'_id': ObjectId(user_id)})
        return json.dumps({
            'status': 'success',
            'message': 'Successfully got total from user',
            'total': user['total']
        })
    except Exception as e:
        print(e)
        return json.dumps({
            'status':'fail',
            'message': 'getting total failed'
        })
