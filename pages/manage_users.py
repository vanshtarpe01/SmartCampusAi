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
        tab1, tab2 = st.tabs(["🎓 Manage Enrolled Students (76)", "👨‍🏫 Manage Faculty / Teachers (7)"])
        
        with tab1:
            render_student_management(role)
            
        with tab2:
            st.markdown("### Faculty Members")
            teachers = get_all_users_by_role("teacher")
            if teachers:
                for t_id, t_info in teachers.items():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{t_info['name']}** (`{t_id}`)")
                    with col2:
                        if st.button("Delete", key=f"del_t_{t_id}"):
                            delete_user(t_id)
                            st.rerun()
            else:
                st.info("No faculty accounts configured yet.")
                
            with st.expander("➕ Add New Teacher / Faculty"):
                with st.form("add_teacher_form", clear_on_submit=True):
                    t_id = st.text_input("Teacher ID (e.g. TCH-002)")
                    t_name = st.text_input("Teacher Name")
                    t_pass = st.text_input("Password", type="password")
                    if st.form_submit_button("Add Teacher", use_container_width=True):
                        if t_id and t_name and t_pass:
                            if add_user(t_id, t_pass, "teacher", t_name):
                                st.success("Teacher added.")
                                st.rerun()
                            else:
                                st.error("User ID already exists.")
                        else:
                            st.error("All fields are required.")
            
    elif role == "teacher":
        render_student_management(role)

def render_student_management(role):
    st.markdown("### 🎓 Enrolled Students — Class Roster")
    
    df = load_students_df()
    st.caption(f"Total enrolled class students: **{len(df)}**")

    # Search bar for students
    s_query = st.text_input("🔍 Quick Search by Roll No or Student Name:", key="mu_student_search", placeholder="e.g. MLU25S211 or Vansh")
    
    display_df = df.copy()
    if s_query:
        mask = (
            display_df["student_id"].str.contains(s_query, case=False, na=False) |
            display_df["name"].str.contains(s_query, case=False, na=False)
        )
        display_df = display_df[mask]

    cols_to_show = ["student_id", "name", "attendance", "internal_marks", "performance_level"]
    renamed = {
        "student_id": "Roll No",
        "name": "Student Name",
        "attendance": "Attendance (%)",
        "internal_marks": "MSE-1 Marks",
        "performance_level": "Status"
    }

    st.dataframe(display_df[cols_to_show].rename(columns=renamed), use_container_width=True, hide_index=True)
    st.caption(f"Displaying {len(display_df)} student(s).")
    
    with st.expander("➕ Enroll New Student"):
        with st.form("add_student_form", clear_on_submit=True):
            s_id = st.text_input("Student Roll No (e.g. MLU25S219)")
            s_name = st.text_input("Student Full Name")
            s_pass = st.text_input("Password", type="password", value="student123")
            
            s_att = st.number_input("Attendance %", min_value=0.0, max_value=100.0, value=85.0)
            s_sh = st.number_input("Study Hours", min_value=0.0, max_value=24.0, value=3.5)
            s_am = st.number_input("Assignment Marks (/10)", min_value=0.0, max_value=10.0, value=8.5)
            s_im = st.number_input("Internal / MSE Marks (/50)", min_value=0.0, max_value=50.0, value=40.0)
            s_pm = st.number_input("Previous Marks (/100)", min_value=0.0, max_value=100.0, value=80.0)
            
            if st.form_submit_button("Enroll Student", use_container_width=True):
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
                        st.success(f"Student {s_name} ({s_id}) enrolled successfully.")
                        st.rerun()
                    else:
                        st.error("User ID already exists.")
                else:
                    st.error("Student ID, Name, and Password are required.")
