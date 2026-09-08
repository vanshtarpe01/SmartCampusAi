import os
os.environ["STREAMLIT_SERVER_PORT"] = "3000"
from pages.projects import render_projects
print("render_projects ok")
