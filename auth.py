"""Simple authentication dictionary for SmartCampus AI."""

STUDENT_CREDENTIALS = {
    "SC-2026-001": "student123",
    "SC-2026-002": "student123",
    "SC-2026-003": "student123",
    "SC-2026-004": "student123",
}

def authenticate_student(student_id: str, password: str) -> bool:
    return STUDENT_CREDENTIALS.get(student_id) == password
