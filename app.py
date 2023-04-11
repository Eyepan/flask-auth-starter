from functools import wraps
from flask import Flask, request
from database import db
import uuid
import bcrypt
app = Flask(__name__)


@app.route("/register", methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), db.get_salt())
    try:
        db.query("INSERT INTO users VALUES (?, ?, ?)",
                 (str(uuid.uuid4()), username, hashed_password))
    except Exception as e:
        return {"error": "username already exists; " + str(e)}, 400
    return {"message": "user created successfully"}, 201


@app.route("/login", methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), db.get_salt())
    user = db.query("SELECT * FROM users WHERE username = ? AND password = ?",
                    (username, hashed_password))
    if not user:
        return {"error": "invalid credentials"}, 401
    user = user[0]
    return {"message": "logged in successfully"}, 200


@app.route("/verify")
def verify_token():
    token = request.headers.get('Authorization')
    if not token:
        return {"error": "no token provided"}, 401
    res = db.query("SELECT * FROM users WHERE id = ?", (token,))
    if not res:
        return {"error": "invalid token"}, 401
    return {"message": "token is valid"}, 200


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {"error": "no token provided"}, 401
        res = db.query("SELECT * FROM users WHERE id = ?", (token,))
        if not res:
            return {"error": "invalid token"}, 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    return "hi mom"


@app.route("/protected")
@token_required
def protected_route():
    return "this is a protected route"
