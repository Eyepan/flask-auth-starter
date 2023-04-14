from flask import request
from functools import wraps
import jwt
from database import db

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {"error": "no token provided"}, 401
        try:
            decoded_token = jwt.decode(token, "super secret key", algorithms=['HS256'])
        except Exception as e:
            return {"error": "invalid token"}, 401
        id = decoded_token.get('id')
        if not id:
            return {"error": "invalid token"}, 401
        res = db.query("SELECT * FROM users WHERE id = ?", (id,))
        if not res:
            return {"error": "invalid token"}, 401
        return f(*args, **kwargs)
    return decorated_function

def generate_token(id):
    return jwt.encode({"id": id}, "super secret key")