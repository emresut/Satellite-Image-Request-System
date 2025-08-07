from temporalio import activity,workflow

@activity.defn
async def update_request_status(request_code: str):
    with workflow.unsafe.imports_passed_through():
        import os    # imports should be used inside of function to make it deterministic
        from pymongo import MongoClient
        from dotenv import load_dotenv

    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client["satellite_requests_database"]
    image_request_collection = db["image_requests"]

    result = image_request_collection.update_one(
        {"request_code": request_code},
        {"$set": {"status": "image request is accepted"}}
    )
    if result.modified_count:
        print(f"Request {request_code} is updated successfully.")
    else:
        print(f"Request {request_code} not found.")