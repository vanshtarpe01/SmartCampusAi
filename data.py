"""SmartCampus AI - Central Data Layer & Backend Bridge
Loads student data from Supabase PostgreSQL."""

import os
from datetime import date
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
import uuid
import datetime

from ai.knowledge_base import (
    get_topic as ai_get_topic,
    search_topic as ai_search_topic,
    get_all_topics as ai_get_all_topics,
    get_all_topic_details,
    KNOWLEDGE_TOPICS
)
from ai.rule_engine import evaluate_student_rules
from ai.performance import analyze_student
from ai.recommendations import generate_recommendations as ai_generate_recommendations
from ai.study_planner import generate_study_plan as ai_generate_study_plan
from ai.assistant import get_ai_response as ai_get_response

from database.connection import get_supabase_client

# Path to local student dataset CSV
STUDENTS_CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "students.csv")

# We maintain a cached DataFrame for existing ML/Rule engines if needed, 
# but fetch it from Supabase primarily.
_students_df_cache: Optional[pd.DataFrame] = None

def get_db():
    return get_supabase_client()

def _clean_student_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes types and handles missing values for student dataframe."""
    df = df.copy()
    if df.empty:
        return pd.DataFrame(columns=["student_id", "name", "attendance", "study_hours", "assignment_marks", "internal_marks", "previous_marks", "performance_level"])
    
    if "student_id" in df.columns:
        df = df.dropna(subset=["student_id"])
        df["student_id"] = df["student_id"].astype(str)
    
    if "name" in df.columns:
        df["name"] = df["name"].fillna("Unknown").astype(str)
    else:
        df["name"] = "Unknown"
        
    if "performance_level" in df.columns:
        df["performance_level"] = df["performance_level"].fillna("Average").astype(str)
    else:
        df["performance_level"] = "Average"
        
    for col in ["attendance", "study_hours", "assignment_marks", "internal_marks", "previous_marks"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0).astype(float)
        else:
            df[col] = 0.0

    return df

def load_students_df() -> pd.DataFrame:
    """Loads and returns the student records dataframe from Supabase, with automatic CSV fallback."""
    global _students_df_cache
    db = get_db()
    
    # 1. Try Supabase
    if db:
        try:
            response = db.table("students").select("*").execute()
            if response.data and len(response.data) > 0:
                df = pd.DataFrame(response.data)
                df = _clean_student_dataframe(df)
                if not df.empty:
                    _students_df_cache = df
                    return df
        except Exception as e:
            print(f"Notice: Supabase fetch error ({e}), loading local dataset.")
            
    # 2. Check memory cache if already populated
    if _students_df_cache is not None and not _students_df_cache.empty:
        return _students_df_cache

    # 3. Fail-safe Fallback to data/students.csv
    if os.path.exists(STUDENTS_CSV_PATH):
        try:
            df = pd.read_csv(STUDENTS_CSV_PATH)
            df = _clean_student_dataframe(df)
            if not df.empty:
                _students_df_cache = df
                return df
        except Exception as e:
            print(f"Notice: CSV fallback read error: {e}")

    return pd.DataFrame(columns=["student_id", "name", "attendance", "study_hours", "assignment_marks", "internal_marks", "previous_marks", "performance_level"])

def save_students_df(df: pd.DataFrame):
    """Saves the student records dataframe to Supabase and updates cache."""
    global _students_df_cache
    db = get_db()
    if not db:
        print("No DB connection to save students.")
        return
        
    try:
        for _, row in df.iterrows():
            db.table("students").upsert({
                "student_id": row["student_id"],
                "name": row["name"],
                "attendance": float(row.get("attendance", 0)),
                "study_hours": float(row.get("study_hours", 0)),
                "assignment_marks": float(row.get("assignment_marks", 0)),
                "internal_marks": float(row.get("internal_marks", 0)),
                "previous_marks": float(row.get("previous_marks", 0)),
                "performance_level": row.get("performance_level", "Average")
            }).execute()
        _students_df_cache = df
    except Exception as e:
        print(f"Error saving students to DB: {e}")

def update_student_study_hours(student_id: str, study_hours: float) -> bool:
    """Updates only the student's study hours in Supabase and local cache."""
    global _students_df_cache
    try:
        hrs = round(float(study_hours), 1)
        db = get_db()
        if db:
            db.table("students").update({"study_hours": hrs}).eq("student_id", student_id).execute()
            
        if _students_df_cache is not None and not _students_df_cache.empty:
            _students_df_cache.loc[_students_df_cache["student_id"] == student_id, "study_hours"] = hrs
            
        if os.path.exists(STUDENTS_CSV_PATH):
            df_csv = pd.read_csv(STUDENTS_CSV_PATH)
            if "student_id" in df_csv.columns and "study_hours" in df_csv.columns:
                df_csv.loc[df_csv["student_id"] == student_id, "study_hours"] = hrs
                df_csv.to_csv(STUDENTS_CSV_PATH, index=False)
        return True
    except Exception as e:
        print(f"Error updating study hours: {e}")
        return False

def get_student_raw(student_id: str) -> Dict[str, Any]:
    df = load_students_df()
    if df.empty:
        return {}
    student = df[df["student_id"] == student_id]
    if student.empty:
        return {}
    return student.iloc[0].to_dict()

def get_student_data(student_id: str) -> Dict[str, Any]:
    raw_data = get_student_raw(student_id)
    if not raw_data:
        return {
            "student_id": student_id,
            "full_name": "Unknown",
            "name": "Unknown",
            "level": "Unknown",
            "risk": "Unknown",
            "attendance": 0,
            "performance": 0,
            "study_hours": 0,
            "weak_areas": [],
            "strengths": []
        }
        
    analysis = analyze_student(raw_data)
    
    return {
        "student_id": raw_data.get("student_id", student_id),
        "full_name": raw_data.get("name", "Unknown"),
        "name": raw_data.get("name", "Unknown"),
        "attendance": raw_data.get("attendance", 0),
        "study_hours": raw_data.get("study_hours", 0),
        "assignment_marks": raw_data.get("assignment_marks", 0),
        "internal_marks": raw_data.get("internal_marks", 0),
        "previous_marks": raw_data.get("previous_marks", 0),
        "performance": analysis.get("overall", analysis.get("performance", 0)),
        "level": raw_data.get("performance_level", analysis.get("level", "Average")),
        "risk": analysis.get("risk", "LOW"),
        "weak_areas": analysis.get("weaknesses", []),
        "strengths": analysis.get("strengths", []),
        "warnings": analysis.get("warnings", []),
        "observations": analysis.get("observations", [])
    }

def get_all_student_summaries() -> List[Dict[str, Any]]:
    df = load_students_df()
    summaries = []
    if df.empty:
        return summaries
    for _, row in df.iterrows():
        sid = row["student_id"]
        summaries.append(get_student_data(sid))
    return summaries

# ------------------------------------------------------------
# AI / KNOWLEDGE BASE ADAPTERS
# ------------------------------------------------------------
def get_knowledge_topic(topic_name: str) -> Optional[Dict[str, Any]]:
    return ai_get_topic(topic_name)

def search_knowledge_topics(query: str) -> List[Dict[str, Any]]:
    return ai_search_topic(query)

def get_all_knowledge_topics() -> List[str]:
    return ai_get_all_topics()

# ------------------------------------------------------------
# BACKWARD COMPATIBLE EXPORTS & DATA STRUCTURES
# ------------------------------------------------------------
student_data = {}
subject_performance = []
subject_details = []
weekly_activity = {
    "Monday": 3.0,
    "Tuesday": 3.5,
    "Wednesday": 4.0,
    "Thursday": 2.5,
    "Friday": 3.5
}
weekly_activity_detailed = [
    {"day": "Monday", "hours": 3.0, "focus": "AI & Math", "status": "Target Met"},
    {"day": "Tuesday", "hours": 3.5, "focus": "DBMS & Networking", "status": "Target Met"},
    {"day": "Wednesday", "hours": 4.0, "focus": "AI Lab & Algorithms", "status": "Exceeded Target"},
    {"day": "Thursday", "hours": 2.5, "focus": "Networking Revision", "status": "Target Met"},
    {"day": "Friday", "hours": 3.5, "focus": "Mock Test & Quizzes", "status": "Target Met"}
]
performance_timeline = [
    {"week": "Week 1", "score": 68, "attendance": 80, "hours": 2.6},
    {"week": "Week 2", "score": 71, "attendance": 81, "hours": 2.8},
    {"week": "Week 3", "score": 70, "attendance": 80, "hours": 2.9},
    {"week": "Week 4", "score": 75, "attendance": 83, "hours": 3.1},
    {"week": "Week 5", "score": 74, "attendance": 82, "hours": 3.0},
    {"week": "Week 6", "score": 78, "attendance": 82, "hours": 3.2}
]
academic_wellness = {
    "Conceptual Knowledge": 80,
    "Study Consistency": 75,
    "Understanding": 82,
    "Practical Application": 70,
    "Problem Solving": 85
}
recent_activities = [
    {"time": "Today, 10:30 AM", "title": "Completed AI Lab Assignment on BFS/DFS", "type": "assignment", "badge": "Completed"},
    {"time": "Yesterday, 04:00 PM", "title": "Studied 3.0 hours: DBMS Normalization", "type": "study", "badge": "Verified"},
    {"time": "2 days ago", "title": "Networking Quiz 3 submitted (Scored 68%)", "type": "quiz", "badge": "Needs Review"},
    {"time": "3 days ago", "title": "Math Problem Set #5 top percentile score", "type": "achievement", "badge": "Top 5%"}
]
recommendations_data = []
knowledge_topics = get_all_topic_details()
ai_responses = {}

def load_admin_recommendations() -> Dict[str, Any]:
    db = get_db()
    if not db:
        return {}
    try:
        res = db.table("recommendations").select("*").execute()
        return {r["student_id"]: r for r in res.data}
    except Exception:
        return {}

def save_admin_recommendation(student_id: str, rec_data: Dict[str, Any]):
    db = get_db()
    if not db: return
    try:
        db.table("recommendations").upsert({
            "student_id": student_id,
            "recommended_hours": rec_data.get("recommended_hours", ""),
            "weak_area": rec_data.get("weak_area", ""),
            "guidance": rec_data.get("guidance", "")
        }).execute()
    except Exception as e:
        print(f"Error saving recommendation: {e}")

def get_admin_recommendation(student_id: str) -> Optional[Dict[str, Any]]:
    recs = load_admin_recommendations()
    return recs.get(student_id)

# --- Skills ---
def get_all_skills_data() -> Dict[str, List[Dict[str, Any]]]:
    db = get_db()
    if not db: return {}
    try:
        res = db.table("skills").select("*").execute()
        skills_dict = {}
        for row in res.data:
            sid = row["student_id"]
            if sid not in skills_dict:
                skills_dict[sid] = []
            skills_dict[sid].append(row)
        return skills_dict
    except Exception:
        return {}

def get_student_skills(student_id: str) -> List[Dict[str, Any]]:
    db = get_db()
    if not db: return []
    try:
        res = db.table("skills").select("*").eq("student_id", student_id).execute()
        return res.data
    except Exception:
        return []

def save_student_skills(student_id: str, skills: List[Dict[str, Any]]):
    db = get_db()
    if not db: return
    try:
        # First delete existing to match the list approach, or just upsert and delete missing
        existing = get_student_skills(student_id)
        existing_ids = {s["id"] for s in existing}
        new_ids = {s["id"] for s in skills if "id" in s}
        
        to_delete = existing_ids - new_ids
        for del_id in to_delete:
            db.table("skills").delete().eq("id", del_id).execute()
            
        for s in skills:
            if "id" not in s:
                s["id"] = str(uuid.uuid4())
            db.table("skills").upsert({
                "id": s["id"],
                "student_id": student_id,
                "name": s["name"],
                "category": s.get("category"),
                "level": s.get("level")
            }).execute()
    except Exception as e:
        print(f"Error saving skills: {e}")

# --- Projects ---
def get_all_projects_data() -> Dict[str, List[Dict[str, Any]]]:
    db = get_db()
    if not db: return {}
    try:
        res = db.table("projects").select("*, project_inspirations(student_id)").execute()
        projs_dict = {}
        for row in res.data:
            sid = row["student_id"]
            if sid not in projs_dict:
                projs_dict[sid] = []
            row["inspirations"] = [i["student_id"] for i in row.get("project_inspirations", [])]
            projs_dict[sid].append(row)
        return projs_dict
    except Exception as e:
        print(f"Error getting projects: {e}")
        return {}

def get_student_projects(student_id: str) -> List[Dict[str, Any]]:
    data = get_all_projects_data()
    return data.get(student_id, [])

def save_student_projects(student_id: str, projects: List[Dict[str, Any]]):
    db = get_db()
    if not db: return
    try:
        existing = get_student_projects(student_id)
        existing_ids = {p["id"] for p in existing}
        new_ids = {p["id"] for p in projects if "id" in p}
        
        to_delete = existing_ids - new_ids
        for del_id in to_delete:
            db.table("projects").delete().eq("id", del_id).execute()
            
        for p in projects:
            if "id" not in p:
                p["id"] = str(uuid.uuid4())
            db.table("projects").upsert({
                "id": p["id"],
                "student_id": student_id,
                "name": p["name"],
                "description": p.get("description"),
                "technologies": p.get("technologies"),
                "link": p.get("link"),
                "status": p.get("status"),
                "visibility": p.get("visibility", "Private")
            }).execute()
    except Exception as e:
        print(f"Error saving projects: {e}")

def get_all_public_projects() -> List[Dict[str, Any]]:
    db = get_db()
    if not db: return []
    try:
        res = db.table("projects").select("*, project_inspirations(student_id)").eq("visibility", "Public").execute()
        public_projects = []
        for row in res.data:
            row["owner_id"] = row["student_id"]
            row["inspirations"] = [i["student_id"] for i in row.get("project_inspirations", [])]
            public_projects.append(row)
        return public_projects
    except Exception:
        return []

def update_project_inspiration(owner_id: str, project_id: str, inspirer_id: str) -> bool:
    db = get_db()
    if not db: return False
    try:
        # Avoid duplicate via unique constraint
        db.table("project_inspirations").insert({
            "project_id": project_id,
            "student_id": inspirer_id
        }).execute()
        return True
    except Exception as e:
        print(f"Inspiration error: {e}")
        return False

# --- Notifications ---
def get_student_notifications(student_id: str) -> List[Dict[str, Any]]:
    db = get_db()
    if not db: return []
    try:
        res = db.table("notifications").select("*").eq("recipient_id", student_id).order("created_at", desc=True).execute()
        for r in res.data:
            r["read"] = r.get("is_read", False)
        return res.data
    except Exception:
        return []

def add_notification(recipient_id: str, message: str, project_id: str, owner_id: str, project_name: str):
    db = get_db()
    if not db: return
    try:
        db.table("notifications").insert({
            "id": str(uuid.uuid4()),
            "recipient_id": recipient_id,
            "project_id": project_id,
            "owner_id": owner_id,
            "project_name": project_name,
            "message": message,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "is_read": False
        }).execute()
    except Exception as e:
        print(f"Error adding notification: {e}")

def mark_notification_read(student_id: str, notif_id: str):
    db = get_db()
    if not db: return
    try:
        db.table("notifications").update({"is_read": True}).eq("id", notif_id).execute()
    except Exception:
        pass

def create_public_project_notification(owner_id: str, project: Dict[str, Any]):
    df = load_students_df()
    if df.empty: return
    all_sids = df["student_id"].tolist()
        
    msg = f"{owner_id} published a new project: {project['name']}"
    for sid in all_sids:
        if sid != owner_id:
            add_notification(sid, msg, project["id"], owner_id, project["name"])

def get_performance_data(student_id: str) -> Dict[str, Any]:
    raw_data = get_student_raw(student_id)
    return analyze_student(raw_data)

def get_recommendations(priority_filter: str = "All", student_id: str = "MLU25S211") -> List[Dict[str, Any]]:
    raw_data = get_student_raw(student_id)
    recs = ai_generate_recommendations(raw_data)
    if priority_filter == "All":
        return recs
    return [r for r in recs if r.get("priority", "") + " Priority" == priority_filter or r.get("priority") == priority_filter]

def get_ai_response(query: str, student_id: Optional[str] = None) -> Dict[str, Any]:
    context = None
    if student_id:
        context = get_student_data(student_id)
    return ai_get_response(query, student_context=context)

def generate_study_plan(exam_date_or_sid=None, available_hours=3.5, subject="Artificial Intelligence", weak_topic="BFS & DFS Graph Traversals", difficulty="Intermediate", **kwargs) -> Dict[str, Any]:
    import datetime
    if isinstance(exam_date_or_sid, str) and not kwargs and "exam_date" not in kwargs:
        student = get_student_data(exam_date_or_sid)
        today = datetime.date.today()
        return ai_generate_study_plan(
            exam_date=today + datetime.timedelta(days=14),
            available_hours=float(student.get("study_hours", 3.5)),
            subject="Artificial Intelligence",
            weak_topic="Core Fundamentals",
            difficulty="Intermediate"
        )
    
    exam_date = kwargs.get("exam_date", exam_date_or_sid)
    if exam_date is None:
        exam_date = datetime.date.today() + datetime.timedelta(days=14)
        
    return ai_generate_study_plan(
        exam_date=exam_date,
        available_hours=available_hours,
        subject=subject,
        weak_topic=weak_topic,
        difficulty=difficulty
    )
