import os
os.environ["STREAMLIT_SERVER_PORT"] = "3000"
from data import create_public_project_notification
create_public_project_notification("SC-2026-001", {"id": "123", "name": "Test Project"})
print("Success")
