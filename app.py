from functools import wraps
from flask import Flask, request
from auth import generate_token, token_required
from database import db
import uuid
import bcrypt
import jwt
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
    user = db.query("SELECT * FROM users WHERE username = ? AND password = ?",
                    (username, hashed_password))
    if not user:
        return {"error": "invalid credentials"}, 401
    user = user[0]
    token = generate_token(user[0])
    return {"message": "user created successfully", "token": token}, 201


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
    token = generate_token(user[0])
    return {"message": "logged in successfully", "token": token}, 200


@app.route("/verify")
@token_required
def verify_token():
    return {"message": "token is valid"}

@app.route('/')
def index():
    return "hi mom"


@app.route("/protected")
@token_required
def protected_route():
    return "this is a protected route"

