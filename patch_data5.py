with open("data.py", "r") as f:
    content = f.read()

content = content.replace(
    'return {"student_id": student_id, "full_name": "Unknown", "level": "Unknown", "risk": "Unknown", "attendance": 0, "performance": 0}',
    'return {"student_id": student_id, "full_name": "Unknown", "name": "Unknown", "level": "Unknown", "risk": "Unknown", "attendance": 0, "performance": 0, "study_hours": 0}'
)

with open("data.py", "w") as f:
    f.write(content)
