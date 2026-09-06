"""SmartCampus AI - Central Data Layer & Backend Bridge
Loads student data from 'data/students.csv' using Pandas, integrates with
the 'ai' package modules (rule_engine, performance, recommendations,
study_planner, knowledge_base, assistant), and provides backward-compatible
interfaces for all Streamlit pages.
"""

import os
from datetime import date
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

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

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "students.csv")

# ------------------------------------------------------------
# DATASET LOADING & CACHING
# ------------------------------------------------------------
_students_df_cache: Optional[pd.DataFrame] = None


def load_students_df() -> pd.DataFrame:
    """Loads and returns the student records dataframe from CSV."""
    global _students_df_cache
    if _students_df_cache is not None:
        return _students_df_cache

    if os.path.exists(CSV_PATH):
        try:
            df = pd.read_csv(CSV_PATH)
            # Ensure proper data types
            df["attendance"] = df["attendance"].astype(float)
            df["study_hours"] = df["study_hours"].astype(float)
            df["assignment_marks"] = df["assignment_marks"].astype(float)
            df["internal_marks"] = df["internal_marks"].astype(float)
            df["previous_marks"] = df["previous_marks"].astype(float)
            _students_df_cache = df
            return _students_df_cache
        except Exception as e:
            print(f"Error loading students CSV: {e}")

    # Fallback DataFrame if CSV is missing
    fallback_data = [
        {"student_id": "SC-2026-001", "name": "Aarav Sharma", "attendance": 90.0, "study_hours": 5.0, "assignment_marks": 9.0, "internal_marks": 45.0, "previous_marks": 85.0},
        {"student_id": "SC-2026-002", "name": "Rohan Verma", "attendance": 70.0, "study_hours": 2.0, "assignment_marks": 6.0, "internal_marks": 32.0, "previous_marks": 55.0},
        {"student_id": "SC-2026-003", "name": "Kavita Rao", "attendance": 50.0, "study_hours": 1.0, "assignment_marks": 4.0, "internal_marks": 20.0, "previous_marks": 35.0}
    ]
    _students_df_cache = pd.DataFrame(fallback_data)
    return _students_df_cache


def get_all_student_summaries() -> List[Dict[str, Any]]:
    """Returns a list of student summaries for selectboxes."""
    df = load_students_df()
    return df.to_dict(orient="records")


def get_student_raw(student_id: Optional[str] = None) -> Dict[str, Any]:
    """Retrieves a raw student row from CSV."""
    df = load_students_df()
    if student_id:
        match = df[df["student_id"] == student_id]
        if not match.empty:
            return match.iloc[0].to_dict()

    # Default to first student (Aarav Sharma / SC-2026-001)
    return df.iloc[0].to_dict()


# ------------------------------------------------------------
# CORE PROFILE & PERFORMANCE ADAPTERS
# ------------------------------------------------------------

def get_student_data(student_id: Optional[str] = None) -> Dict[str, Any]:
    """Returns the full analyzed profile for a student using the AI backend."""
    raw = get_student_raw(student_id)
    analysis = analyze_student(raw)

    # Bridge fields to maintain exact compatibility with Phase 1 frontend components
    return {
        "name": analysis["name"],
        "full_name": analysis["full_name"],
        "student_id": analysis["student_id"],
        "program": analysis["program"],
        "semester": analysis["semester"],
        "performance": int(analysis["performance"]),
        "level": analysis["level"],
        "risk": analysis["risk"],
        "attendance": int(analysis["attendance"]),
        "study_hours": analysis["study_hours"],
        "assignments": int(analysis["normalized"]["assignments"]),
        "internal_test": int(analysis["normalized"]["internal_marks"]),
        "previous_exam": int(analysis["previous_marks"]),
        "wellness_score": analysis["wellness_score"],
        "achievements": analysis["achievements"],
        "strengths": analysis["strengths"],
        "improvements": analysis["improvements"],
        "weaknesses": analysis["weaknesses"],
        "warnings": analysis["warnings"],
        "observations": analysis["observations"],
        "ai_insight": analysis["ai_insight"]
    }


def get_performance_data(student_id: Optional[str] = None) -> Dict[str, Any]:
    """Returns structured performance data, subjects, and wellness metrics."""
    raw = get_student_raw(student_id)
    analysis = analyze_student(raw)

    return {
        "overall": int(analysis["performance"]),
        "level": analysis["level"],
        "risk": analysis["risk"],
        "attendance": int(analysis["attendance"]),
        "study_hours": analysis["study_hours"],
        "assignments": int(analysis["normalized"]["assignments"]),
        "internal_test": int(analysis["normalized"]["internal_marks"]),
        "previous_exam": int(analysis["previous_marks"]),
        "subjects": analysis["subjects"],
        "subject_details": analysis["subject_details"],
        "timeline": analysis["timeline"],
        "wellness": analysis["wellness"],
        "strengths": analysis["strengths"],
        "improvements": analysis["improvements"],
        "warnings": analysis["warnings"],
        "observations": analysis["observations"],
        "ai_insight": analysis["ai_insight"],
        "raw_record": raw
    }


# ------------------------------------------------------------
# RECOMMENDATIONS ADAPTER
# ------------------------------------------------------------

def get_recommendations(priority: str = "All", student_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns AI-generated prioritized recommendations for a student."""
    raw = get_student_raw(student_id)
    analysis = analyze_student(raw)
    recs = ai_generate_recommendations(raw, analysis)

    if priority == "All" or not priority:
        return recs
    return [r for r in recs if priority.lower() in r["priority"].lower()]


# ------------------------------------------------------------
# STUDY PLANNER ADAPTER
# ------------------------------------------------------------

def generate_study_plan(
    exam_date: date,
    available_hours: float,
    subject: str,
    weak_topic: str,
    difficulty: str
) -> Dict[str, Any]:
    """Delegates study schedule generation to the AI planner module."""
    return ai_generate_study_plan(
        exam_date=exam_date,
        available_hours=available_hours,
        subject=subject,
        weak_topic=weak_topic,
        difficulty=difficulty
    )


# ------------------------------------------------------------
# ASSISTANT QUERY ADAPTER
# ------------------------------------------------------------

def get_ai_response(query: str, student_id: Optional[str] = None) -> Dict[str, Any]:
    """Provides conversational AI responses from the local assistant module."""
    student_ctx = None
    if student_id:
        raw = get_student_raw(student_id)
        student_ctx = analyze_student(raw)

    return ai_get_response(query, student_context=student_ctx)


# ------------------------------------------------------------
# KNOWLEDGE BASE ADAPTERS
# ------------------------------------------------------------

def get_knowledge_topic(topic_name: str) -> Optional[Dict[str, Any]]:
    """Retrieves knowledge topic from local knowledge base."""
    return ai_get_topic(topic_name)


def search_knowledge_topics(query: str) -> List[Dict[str, Any]]:
    """Searches knowledge topics matching user keywords."""
    return ai_search_topic(query)


def get_all_knowledge_topics() -> List[str]:
    """Returns all available topic names."""
    return ai_get_all_topics()


# ------------------------------------------------------------
# BACKWARD COMPATIBLE EXPORTS & DATA STRUCTURES
# ------------------------------------------------------------
# Default active student representation
student_data = get_student_data("SC-2026-001")
subject_performance = analyze_student(get_student_raw("SC-2026-001"))["subjects"]
subject_details = analyze_student(get_student_raw("SC-2026-001"))["subject_details"]

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

recommendations_data = ai_generate_recommendations(get_student_raw("SC-2026-001"))
knowledge_topics = get_all_topic_details()
ai_responses = {
    "bfs": ai_get_response("bfs"),
    "dfs": ai_get_response("dfs"),
    "a*": ai_get_response("a*"),
    "minimax": ai_get_response("minimax"),
    "alpha-beta pruning": ai_get_response("alpha beta pruning"),
    "artificial intelligence": ai_get_response("artificial intelligence"),
    "expert system": ai_get_response("expert system"),
    "python for ai": ai_get_response("python for ai"),
    "networking": ai_get_response("networking"),
    "dbms": ai_get_response("dbms")
}
