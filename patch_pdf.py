import re

with open("pages/pdf_report.py", "r") as f:
    content = f.read()

new_content = content.replace('active_sid = st.session_state.get("selected_student_id")', '''
    if st.session_state.get("role") in ["admin", "teacher"]:
        from data import load_students_df
        df = load_students_df()
        active_sid = st.selectbox("Select Student", options=df["student_id"].tolist())
    else:
        active_sid = st.session_state.get("selected_student_id")
''')

with open("pages/pdf_report.py", "w") as f:
    f.write(new_content)
