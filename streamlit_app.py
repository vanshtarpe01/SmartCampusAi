"""Streamlit Community Cloud Entry Point
Executes app.py as the primary application file.
"""
import runpy

if __name__ == "__main__" or True:
    runpy.run_path("app.py", run_name="__main__")
