with open("data.py", "r") as f:
    content = f.read()

content += """
def get_ai_response(query: str) -> str:
    return ai_get_response(query)
"""
with open("data.py", "w") as f:
    f.write(content)
