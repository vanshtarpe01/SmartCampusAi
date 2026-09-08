with open("data.py", "r") as f:
    content = f.read()

funcs = """
def get_performance_data(student_id: str) -> Dict[str, Any]:
    raw_data = get_student_raw(student_id)
    return analyze_student(raw_data)

def get_recommendations(priority_filter: str = "All", student_id: str = "SC-2026-001") -> List[Dict[str, Any]]:
    raw_data = get_student_raw(student_id)
    recs = ai_generate_recommendations(raw_data)
    if priority_filter == "All":
        return recs
    return [r for r in recs if r.get("priority", "") + " Priority" == priority_filter or r.get("priority") == priority_filter]
"""
content += funcs
with open("data.py", "w") as f:
    f.write(content)
