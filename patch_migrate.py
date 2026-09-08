with open("scripts/migrate_data.py", "r") as f:
    content = f.read()
content = content.replace("from dotenv import load_dotenv\n\nload_dotenv()", "try:\n    from dotenv import load_dotenv\n    load_dotenv()\nexcept ImportError:\n    pass")
with open("scripts/migrate_data.py", "w") as f:
    f.write(content)
