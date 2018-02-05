import pymongo
import jwt
import datetime
import bcrypt
import os
import json
from functools import wraps
from flask import g, request, redirect, url_for

SECRET_KEY = "NAKINAKINAK"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('x-access-token')
        try:
            user_id = decode_token(token)
            return f(user_id, **kwargs)
        except jwt.exceptions.ExpiredSignatureError:
            return json.dumps({
                'status':'forbidden',
                'message':'Signature Expired'
            })
        except jwt.exceptions.InvalidTokenError:
            return json.dumps({
                'status':'forbidden',
                'message':'Invalid Token'
            })

    return decorated_function

def handle_signup(db, data):
    email = data.get("email")
    username = data["username"]
    password = data["password"]
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {"username": username, "email": email, "password": hashed, "date": datetime.datetime.utcnow()}
    try:
        user_id = db.users.insert_one(user) 
        return json.dumps({
            'status':'success',
            'message': 'Signup Successfull',
            'token': encode_token(user_id)
        })
    except:
        return json.dumps({
            'status':'fail',
            'message': 'email already exists'
        })

def handle_signin(db, data):
    user = db.users.find_one({'username': data['username']})
    if bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        return json.dumps({
            'status':'success',
            'message':'successfully logged in',
            'token': encode_token(user.get('_id'))
        })
    else:
        return json.dumps({
            'status':'fail',
            'message': 'wrong password'
        })

def encode_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'sub': str(user_id)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithm='HS256')
    return payload['sub']
