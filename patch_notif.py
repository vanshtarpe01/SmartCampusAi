with open("data.py", "r") as f:
    content = f.read()

content = content.replace('def get_student_notifications(student_id: str) -> List[Dict[str, Any]]:\n    db = get_db()\n    if not db: return []\n    try:\n        res = db.table("notifications").select("*").eq("recipient_id", student_id).order("created_at", desc=True).execute()\n        return res.data', 
'''def get_student_notifications(student_id: str) -> List[Dict[str, Any]]:
    db = get_db()
    if not db: return []
    try:
        res = db.table("notifications").select("*").eq("recipient_id", student_id).order("created_at", desc=True).execute()
        for r in res.data:
            r["read"] = r.get("is_read", False)
        return res.data''')

with open("data.py", "w") as f:
    f.write(content)
