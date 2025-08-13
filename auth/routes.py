from flask import Blueprint, jsonify, request, session, redirect
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["satellite_requests_database"]
user_collection = db["users"]

# Register endpoint
@auth_bp.route("/api/register", methods=["POST"])
def Register():

    if not request.is_json:
        return jsonify({"Error": "Content-Type must be application/json"}), 415

    data = request.get_json()
    username = data.get("username")
    if len(username) > 20:
        return jsonify({"Error" : "Please enter a username of less than 20 characters."})
    password = data.get("password")
    if len(password) > 20:
        return jsonify({"Error" : "Please enter a password of less than 20 characters."})
    confirm_password = data.get("confirm_password")

    if not username or not password or not confirm_password:
        return jsonify({"Error" : "You must fill all fields!"}), 400

    if user_collection.find_one({"username" : username}):
        return jsonify({"Error" : "This username is already taken!"}), 409
        
    if password != confirm_password:
        return jsonify({"Error" : "Passwords don't match!"}), 400
        
    hashed_password = generate_password_hash(password)
    user_collection.insert_one({
        "username" : username,
        "hashed_password" : hashed_password
    })
        
    return jsonify({"message" : "Registration is successful!"}), 201

# Login endpoint
@auth_bp.route("/api/login", methods=["POST"])
def Login():

    if not request.is_json:
        return jsonify({"Error": "Content-Type must be application/json"}), 415


    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"Error" : "You must fill all fields!"}), 400

    user = user_collection.find_one({"username" : username})

    if not user:
        return jsonify({"Error" : "User not found!"}), 404
    
    if not check_password_hash(user["hashed_password"], password):
        return jsonify({"Error": "Password is incorrect!" }), 401
    
    if user and check_password_hash(user["hashed_password"], data["password"]):
        session["username"] = data["username"]
        return jsonify({"message": f"Welcome {username}", "username": username}), 200
    
# This is an endpoint that makes synchronization between UI and backend. It keeps the information whether it logged in.
@auth_bp.route("/api/check_login", methods=["GET"])
def check_login():
    username = session.get("username") # Shouldn't use "username = session["username"]", because it does not return none.
    if username:
        return jsonify({"logged_in": True, "username": username}), 200
    return jsonify({"logged_in": False}), 200
    
# Logout endpoint
@auth_bp.route("/api/logout", methods=["POST"])
def Logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200