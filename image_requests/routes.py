from flask import Blueprint, jsonify, request, session
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dotenv import load_dotenv
import os
import secrets
import string
from datetime import datetime, timezone
from temporalio.client import Client
import asyncio
from temporal_workflow.workflows import ImageRequestWorkflow
from .utils import is_valid_date, is_end_after_start, is_integer

image_requests_bp = Blueprint("image_requests", __name__)

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["satellite_requests_database"]
image_request_collection = db["image_requests"]

async def start_workflow(request_code):
    client = await Client.connect("temporal:7233")
    handle = await client.start_workflow(  # actually there is no need to "handle" for now but it is here because it is open to develop.
        ImageRequestWorkflow.run,
        request_code,
        id=f"workflow-{request_code}",
        task_queue="image-request-task-queue",
    )

# Create_image_request endpoint
@image_requests_bp.route("/api/create-image-request", methods=["POST"])
def Create_image_request():

    if "username" not in session:
        return jsonify({"Error": "Unauthorized"}), 401
    
    allowed_chars = string.ascii_lowercase + string.digits
    request_code = ''.join(secrets.choice(allowed_chars) for _ in range(8))  # random code generator

    data = request.get_json()
    username = session["username"]
    request_type = data.get("request_type")

    if request_type == "single":
        single_image_start_date = data.get("single image start date")
        if not is_valid_date(single_image_start_date):
            return jsonify({"Error": "It is not a valid date (expected YYYY-MM-DD, not expected YYYY/MM/DD)"}), 400
        single_image_end_date = data.get("single image end date")
        if not is_valid_date(single_image_end_date):
            return jsonify({"Error": "It is not a valid date (expected YYYY-MM-DD, not expected YYYY/MM/DD)"}), 400
        if not is_end_after_start(single_image_start_date, single_image_end_date):
            return jsonify({"Error": "End date must be after start date."}), 400

    elif request_type == "systematic":
        systematic_image_start_date = data.get("systematic image start date")
        if not is_valid_date(systematic_image_start_date):
            return jsonify({"Error": "It is not a valid date (expected YYYY-MM-DD, not expected YYYY/MM/DD)"}), 400
        systematic_image_end_date = data.get("systematic image end date")
        if not is_valid_date(systematic_image_end_date):
            return jsonify({"Error": "It is not a valid date (expected YYYY-MM-DD, not expected YYYY/MM/DD)"}), 400
        if not is_end_after_start(systematic_image_start_date, systematic_image_end_date):
            return jsonify({"Error": "End date must be after start date."}), 400

    elif request_type == "periodic":    
        periodic_image_frequency = data.get("periodic image frequency")
        if not is_integer(periodic_image_frequency):
            return jsonify({"Error" : "Frequency can only be integer as day"}) ,400
        periodic_image_consecutive_days = data.get("number of consecutive days")
        if not is_integer(periodic_image_consecutive_days):
            return jsonify({"Error" : "Just an integer can be used as consecutive day "}), 400
        
        periodic_image_start_date = data.get("periodic image start date")
        if not is_valid_date(periodic_image_start_date):
            return jsonify({"Error": "It is not a valid date (expected YYYY-MM-DD, not expected YYYY/MM/DD)"}), 400
        periodic_image_end_date = data.get("periodic image end date")
        if not is_valid_date(periodic_image_end_date):
            return jsonify({"Error": "It is not a valid date (expected YYYY-MM-DD, not expected YYYY/MM/DD)"}), 400
        if not is_end_after_start(periodic_image_start_date, periodic_image_end_date):
            return jsonify({"Error": "End date must be after start date."}), 400

    elif request_type == "recurring":
        recurring_image_outer_loop_duration = data.get("recurring image outer loop duration")
        if not is_integer(recurring_image_outer_loop_duration):
            return jsonify({"Error" : "Outer loop duration can only be integer  as day"}), 400
        inner_loop_duration_per_outer_loop = data.get("inner loop duration per outer loop")
        if not is_integer(inner_loop_duration_per_outer_loop):
            return jsonify({"Error" : "Inner loop duration can only be integer as day"}), 400
        
        outer_loop_start_date = data.get("outer loop start date")
        if not is_valid_date(outer_loop_start_date):
            return jsonify({"Error": "It is not a valid date (expected YYYY-MM-DD, not expected YYYY/MM/DD)"}), 400
        outer_loop_end_date = data.get("outer loop end date")
        if not is_valid_date(outer_loop_end_date):
            return jsonify({"Error": "It is not a valid date (expected YYYY-MM-DD, not expected YYYY/MM/DD)"}), 400
        if not is_end_after_start(outer_loop_start_date, outer_loop_end_date):
            return jsonify({"Error": "End date must be after start date."}), 400
        
        inner_loop_start_date = data.get("inner loop start date")
        if not is_valid_date(inner_loop_start_date):
            return jsonify({"Error": "It is not a valid date (expected YYYY-MM-DD, not expected YYYY/MM/DD)"}), 400
        inner_loop_end_date = data.get("inner loop end date")
        if not is_valid_date(inner_loop_end_date):
            return jsonify({"Error": "It is not a valid date (expected YYYY-MM-DD, not expected YYYY/MM/DD)"}), 400
        if not is_end_after_start(inner_loop_start_date, inner_loop_end_date):
            return jsonify({"Error": "End date must be after start date."}), 400

    image_request = {
    "username" : username,
    "request_code" : request_code,
    "request_type" : request_type,
    "created_at" : datetime.now(timezone.utc),
    "status": "under evaluation"

    } 

    if request_type == "single":
        image_request.update({
        "single image start date" : single_image_start_date,
        "single image end date" : single_image_end_date
        })

    elif request_type == "systematic":
        image_request.update({
        "systematic image start date" : systematic_image_start_date,
        "systematic image end date" : systematic_image_end_date
        })

    elif request_type == "periodic":
        image_request.update({
        "periodic image frequency" : periodic_image_frequency,
        "number of consecutive days" : periodic_image_consecutive_days,
        "periodic image start date" : periodic_image_start_date,
        "periodic image end date" : periodic_image_end_date,
        })

    elif request_type == "recurring":
        image_request.update({
        "recurring image outer loop duration" : recurring_image_outer_loop_duration,
        "inner loop duration per outer loop" : inner_loop_duration_per_outer_loop,
        "outer loop start date" : outer_loop_start_date,
        "outer loop end date" : outer_loop_end_date,
        "inner loop start date" : inner_loop_start_date,
        "inner loop end date" : inner_loop_end_date
        })

    try:
        image_request_collection.insert_one(image_request)

        asyncio.run(start_workflow(request_code))

        return jsonify({
            "Message" : "Request submitted successfully!",
            "Request Code:" : f" {request_code} (This will appear in your requests list.)"
        }), 201

    except DuplicateKeyError:
        return jsonify({
            "Error" : "Congratulations, you just hit a 1 in 2 trillion 821 billion chance! This code already exists. Please try to submit again."
        }), 409
    
# All_image_requests endpoint
@image_requests_bp.route("/api/all-image-requests", methods=["GET"])
def All_image_requests():

    if "username" not in session:
        return jsonify({"Error": "Unauthorized"}), 401

    username = session["username"]
    
    requests = list(
    image_request_collection
        .find({"username": username}, {"_id": 0})
        .sort("created_at", -1)
    )

    if not requests:
        return jsonify({
            "requests": [],
            "Message": "No requests found."
        }), 200

    return jsonify({"requests": requests}), 200

# Delete_image_request endpoint
@image_requests_bp.route("/api/delete-image-request", methods=["POST"])
def Delete_image_request():

    if "username" not in session:
        return jsonify({"Error": "Unauthorized"}), 401
     
    data = request.get_json()
    request_code = data.get("request_code")
    username = session["username"]

    result = image_request_collection.delete_one({
        "request_code" : request_code,
        "username" : username
    })

    if result.deleted_count == 1:
        return jsonify({"Message" : "Image request is deleted successfully!"}), 200
    else:
        return jsonify({"Error" : "Image request not found!"}), 404