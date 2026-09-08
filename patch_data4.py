with open("data.py", "r") as f:
    content = f.read()

funcs = """
def generate_study_plan(student_id: str) -> Dict[str, Any]:
    raw_data = get_student_raw(student_id)
    return ai_generate_study_plan(raw_data)
"""
content += funcs
with open("data.py", "w") as f:
    f.write(content)
