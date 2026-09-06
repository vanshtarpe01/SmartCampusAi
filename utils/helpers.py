"""SmartCampus AI - Helper Functions
Provides formatting, filtering, search utilities, and session state initialization.
"""

from typing import Dict, Any, List
import streamlit as st
import datetime

def init_session_state():
    """Initializes all necessary Streamlit session variables."""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello Aarav! I am your SmartCampus AI Study Companion.\n\n"
                    "You can ask me questions on topics like **BFS, DFS, A* Search, Minimax, "
                    "Alpha-Beta Pruning, Expert Systems**, or ask for revision tips on Networking and DBMS!"
                ),
                "timestamp": "09:00 AM",
                "category": "Welcome"
            }
        ]

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
