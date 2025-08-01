from fastapi import APIRouter, HTTPException, Query
from models import User, Resource, StandardConfig, SignupUser
from database import users_collection, get_db, users_signup_collection
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
import bcrypt

router = APIRouter()

# === USER SIGNUP ===
@router.post("/signin")
def signin(user: SignupUser):
    existing_user = users_signup_collection.find_one({
        "email": user.email,
        "password": user.password
    })

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_data = {
        "id": str(existing_user.get("_id")),
        "firstname": existing_user.get("firstname"),
        "lastname": existing_user.get("lastname"),
        "email": existing_user.get("email")
    }

    return {
        "message": "Login successful",
        "user": user_data
    }

# === POST STANDARD CONFIG ===
@router.post("/api/configs")
def submit_config(config: StandardConfig):
    db = get_db()
    collection = db["standardConfigsDb"]
    data = jsonable_encoder(config)
    # Insert a new config for this type and email
    result = collection.insert_one(data)
    saved = collection.find_one({"_id": result.inserted_id})
    saved["_id"] = str(saved["_id"])
    return saved

# === GET LATEST CONFIG FOR SUMMARY (per type and user email) ===
@router.get("/api/config/latest")
def get_latest_config(
    type: str = Query(..., description="Config type"),
    email: str = Query(..., description="User email")
):
    db = get_db()
    collection = db["standardConfigsDb"]
    latest = list(
        collection.find({"type": type, "email": email})
        .sort("_id", -1)
        .limit(1)
    )
    if not latest:
        raise HTTPException(status_code=404, detail="No config found")
    config = latest[0]
    config["_id"] = str(config["_id"])
    return config

# ====User Onboarding routes============
@router.post("/bulk_signup")
def bulk_signup(users: List[User]):
    inserted_users = []
    for user in users:
        existing = users_collection.find_one({
            "$or": [
                {"username": user.username},
                {"password": user.password},
                {"project": user.project}
            ]
        })
        if existing:
            continue  # Skip if any of the fields already exist

        user_dict = user.dict()
        hashed_password = bcrypt.hashpw(user_dict["password"].encode("utf-8"), bcrypt.gensalt())
        user_dict["password"] = hashed_password.decode("utf-8")
        result = users_collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        inserted_users.append(user_dict)

    if not inserted_users:
        raise HTTPException(status_code=400, detail="Entries are duplicates")

    for user in inserted_users:
        user.pop("_id", None)

    return {
        "message": f"{len(inserted_users)} users added to Environment successfully",
        "data": inserted_users
    }