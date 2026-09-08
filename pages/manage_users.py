import streamlit as st
import pandas as pd
from auth import get_all_users_by_role, add_user, edit_user, delete_user
from data import load_students_df, save_students_df

def render_manage_users():
    role = st.session_state.get("role", "student")
    if role not in ["admin", "teacher"]:
        st.error("Unauthorized.")
        return

    st.markdown("## 👥 Manage Users")
    
    if role == "admin":
        tab1, tab2 = st.tabs(["Manage Teachers", "Manage Students"])
        
        with tab1:
            st.markdown("### Teachers")
            teachers = get_all_users_by_role("teacher")
            if teachers:
                for t_id, t_info in teachers.items():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{t_info['name']}** ({t_id})")
                    with col2:
                        if st.button("Delete", key=f"del_t_{t_id}"):
                            delete_user(t_id)
                            st.rerun()
            else:
                st.info("No teachers added yet.")
                
            with st.expander("➕ Add Teacher"):
                with st.form("add_teacher_form", clear_on_submit=True):
                    t_id = st.text_input("Teacher ID")
                    t_name = st.text_input("Teacher Name")
                    t_pass = st.text_input("Password", type="password")
                    if st.form_submit_button("Add Teacher"):
                        if t_id and t_name and t_pass:
                            if add_user(t_id, t_pass, "teacher", t_name):
                                st.success("Teacher added.")
                                st.rerun()
                            else:
                                st.error("User ID already exists.")
                        else:
                            st.error("All fields are required.")
                            
        with tab2:
            render_student_management(role)
            
    elif role == "teacher":
        render_student_management(role)

def render_student_management(role):
    st.markdown("### Manage Students")
    
    df = load_students_df()
    st.dataframe(df[["student_id", "name", "attendance", "performance_level"]], use_container_width=True)
    
    with st.expander("➕ Add Student"):
        with st.form("add_student_form", clear_on_submit=True):
            s_id = st.text_input("Student ID (e.g. SC-2026-005)")
            s_name = st.text_input("Student Name")
            s_pass = st.text_input("Password", type="password")
            
            s_att = st.number_input("Attendance %", min_value=0.0, max_value=100.0, value=80.0)
            s_sh = st.number_input("Study Hours", min_value=0.0, max_value=24.0, value=3.0)
            s_am = st.number_input("Assignment Marks (/10)", min_value=0.0, max_value=10.0, value=8.0)
            s_im = st.number_input("Internal Marks (/50)", min_value=0.0, max_value=50.0, value=40.0)
            s_pm = st.number_input("Previous Marks (/100)", min_value=0.0, max_value=100.0, value=75.0)
            
            if st.form_submit_button("Add Student"):
                if s_id and s_name and s_pass:
                    if add_user(s_id, s_pass, "student", s_name):
                        new_row = {
                            "student_id": s_id,
                            "name": s_name,
                            "attendance": s_att,
                            "study_hours": s_sh,
                            "assignment_marks": s_am,
                            "internal_marks": s_im,
                            "previous_marks": s_pm,
                            "performance_level": "Good"
                        }
                        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                        save_students_df(df)
                        st.success("Student added successfully.")
                        st.rerun()
                    else:
                        st.error("User ID already exists.")
                else:
                    st.error("Student ID, Name, and Password are required.")
