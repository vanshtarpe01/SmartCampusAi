"""SmartCampus AI - Helper Functions
Provides formatting, filtering, search utilities, and session state initialization.
"""

from typing import Dict, Any, List, Optional
import streamlit as st
import datetime
import os
import json
import hmac
import hashlib
import base64

SESSION_SECRET = "smartcampus-ai-session-key-2026"

def create_session_token(user_id: str, role: str) -> str:
    """Generates a secure HMAC-signed session token for browser persistence."""
    try:
        payload = json.dumps({"uid": str(user_id), "role": str(role)})
        payload_b64 = base64.urlsafe_b64encode(payload.encode("utf-8")).decode("utf-8")
        sig = hmac.new(SESSION_SECRET.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256).hexdigest()[:16]
        return f"{payload_b64}.{sig}"
    except Exception as e:
        print(f"Error creating session token: {e}")
        return ""

def verify_session_token(token: str) -> Optional[Dict[str, str]]:
    """Verifies HMAC signature on session token and returns dict if valid."""
    if not token or "." not in token:
        return None
    try:
        payload_b64, sig = token.split(".", 1)
        expected_sig = hmac.new(SESSION_SECRET.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256).hexdigest()[:16]
        if hmac.compare_digest(sig, expected_sig):
            raw_bytes = base64.urlsafe_b64decode(payload_b64.encode("utf-8"))
            data = json.loads(raw_bytes.decode("utf-8"))
            if isinstance(data, dict) and "uid" in data and "role" in data:
                return data
    except Exception as e:
        print(f"Error verifying session token: {e}")
    return None

def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves user profile (role, user_id, name) with local JSON fast lookup and Supabase fallback."""
    # 1. Fast local users.json lookup (instant, zero network delay)
    users_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "users.json")
    if os.path.exists(users_path):
        try:
            with open(users_path, "r", encoding="utf-8") as f:
                users = json.load(f)
                u = users.get(user_id)
                if u:
                    return {"role": u.get("role", "student"), "user_id": user_id, "name": u.get("name", user_id)}
        except Exception:
            pass

    # 2. Supabase lookup fallback
    try:
        from database.connection import get_supabase_client
        db = get_supabase_client()
        if db:
            res = db.table("users").select("*").eq("username", user_id).execute()
            if res.data and len(res.data) > 0:
                u = res.data[0]
                if u.get("is_active", True):
                    return {"role": u["role"], "user_id": user_id, "name": u.get("name", user_id)}
    except Exception as e:
        print(f"Notice: Supabase get_user error: {e}")

    return None

def init_session_state():
    """Initializes all necessary Streamlit session variables."""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if "generated_plan" not in st.session_state:
        st.session_state.generated_plan = None

    if "completed_tasks" not in st.session_state:
        st.session_state.completed_tasks = set(["09:00 - 10:00"])

    if "rec_filter" not in st.session_state:
        st.session_state.rec_filter = "All"

def format_percentage(value: float) -> str:
    """Formats float as percentage string."""
    return f"{value:.1f}%"

def get_status_color(status: str) -> str:
    """Returns hex color code for academic status."""
    status_lower = status.lower()
    if "excellent" in status_lower or "completed" in status_lower or "low" in status_lower or "good" in status_lower:
        return "#2a9d8f"
    elif "attention" in status_lower or "pending" in status_lower or "medium" in status_lower or "progress" in status_lower:
        return "#f4a261"
    else:
        return "#e63946"
