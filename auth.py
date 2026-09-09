"""Authentication for SmartCampus AI.
Uses Supabase PostgreSQL for persistent user storage."""

import json
import os
import hmac
import hashlib
import base64
from typing import Optional, Dict, Any
from database.connection import get_supabase_client

from utils.helpers import (
    SESSION_SECRET,
    create_session_token,
    verify_session_token,
    get_user_profile as get_user
)


# Local fallback for tests if Supabase is unavailable
USERS_JSON_PATH = os.path.join(os.path.dirname(__file__), "data", "users.json")

def load_users_fallback():
    if not os.path.exists(USERS_JSON_PATH):
        return {}
    with open(USERS_JSON_PATH, "r") as f:
        return json.load(f)

def get_db():
    return get_supabase_client()

def authenticate_student(student_id: str, password: str) -> bool:
    db = get_db()
    if not db:
        users = load_users_fallback()
        user = users.get(student_id)
        return user is not None and user.get("role") == "student" and user.get("password") == password
        
    try:
        res = db.table("users").select("*").eq("username", student_id).eq("role", "student").execute()
        if len(res.data) > 0:
            return res.data[0]["password_hash"] == password
    except Exception as e:
        print(f"DB auth error: {e}")
    return False

def authenticate_user(user_id: str, password: str):
    db = get_db()
    if not db:
        users = load_users_fallback()
        user = users.get(user_id)
        if user and user.get("password") == password:
            return {"role": user["role"], "user_id": user_id, "name": user.get("name", user_id)}
        return None
        
    try:
        res = db.table("users").select("*").eq("username", user_id).execute()
        if len(res.data) > 0:
            u = res.data[0]
            if u["password_hash"] == password and u["is_active"]:
                return {"role": u["role"], "user_id": user_id, "name": u.get("name", user_id)}
    except Exception as e:
        print(f"DB auth error: {e}")
    return None

def add_user(user_id, password, role, name):
    db = get_db()
    if not db: return False
    try:
        db.table("users").insert({
            "username": user_id,
            "password_hash": password,
            "role": role,
            "name": name
        }).execute()
        return True
    except Exception as e:
        print(f"DB add_user error: {e}")
        return False

def edit_user(user_id, **kwargs):
    db = get_db()
    if not db: return False
    try:
        updates = {}
        if "name" in kwargs: updates["name"] = kwargs["name"]
        if "password" in kwargs: updates["password_hash"] = kwargs["password"]
        if "role" in kwargs: updates["role"] = kwargs["role"]
        
        db.table("users").update(updates).eq("username", user_id).execute()
        return True
    except Exception:
        return False

def delete_user(user_id):
    db = get_db()
    if not db: return False
    try:
        db.table("users").delete().eq("username", user_id).execute()
        return True
    except Exception:
        return False

def get_all_users_by_role(role):
    db = get_db()
    if db:
        try:
            res = db.table("users").select("*").eq("role", role).execute()
            if res.data and len(res.data) > 0:
                return {u["username"]: u for u in res.data}
        except Exception as e:
            print(f"Notice: Supabase get_all_users_by_role error: {e}")
            
    users = load_users_fallback()
    return {uid: u for uid, u in users.items() if u.get("role") == role}
