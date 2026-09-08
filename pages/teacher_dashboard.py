import streamlit as st
from data import load_students_df, get_all_projects_data

def render_teacher_dashboard():
    st.markdown("## 👨‍🏫 Teacher Dashboard")
    st.markdown("Overview of student performance and projects.")
    
    df = load_students_df()
    
    total_students = len(df)
    
    avg_attendance = df["attendance"].mean() if not df.empty else 0
    avg_study_hours = df["study_hours"].mean() if not df.empty else 0
    
    needs_improvement = len(df[df["performance_level"] == "Needs Improvement"]) if not df.empty else 0
    
    projects_data = get_all_projects_data()
    total_projects = 0
    completed_projects = 0
    
    tech_counts = {}
    students_with_projects = 0
    
    for sid, projs in projects_data.items():
        if len(projs) > 0:
            students_with_projects += 1
        total_projects += len(projs)
        for p in projs:
            if p.get("status") == "Completed":
                completed_projects += 1
                
            techs = p.get("technologies", "")
            if techs:
                for t in [x.strip() for x in techs.split(",") if x.strip()]:
                    tech_counts[t] = tech_counts.get(t, 0) + 1
                    
    popular_techs = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    popular_techs_str = ", ".join([f"{t[0]} ({t[1]})" for t in popular_techs]) if popular_techs else "None"
    student_participation_pct = (students_with_projects / total_students * 100) if total_students > 0 else 0
                
    st.markdown("### 📌 My Students Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Class Strength", total_students)
    col2.metric("Avg Attendance", f"{avg_attendance:.1f}%")
    col3.metric("Avg Study Hours", f"{avg_study_hours:.1f} hrs/day")
    col4.metric("Needs Improvement", needs_improvement)
    
    # -------------------------------------------------------------------------
    # CLASS STUDENT ROSTER (76 STUDENTS)
    # -------------------------------------------------------------------------
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(0, 180, 216, 0.2); margin: 24px 0 16px 0;'>", unsafe_allow_html=True)
    st.markdown(f"### 🎓 Class Student Roster — CSE (AIML) Sem-V ({total_students} Students)")

    t_search = st.text_input("🔍 Search Student by Roll No or Name:", key="teacher_dash_search", placeholder="e.g. MLU25S211 or Vansh")
    disp_df = df.copy()
    if t_search:
        m = (
            disp_df["student_id"].str.contains(t_search, case=False, na=False) |
            disp_df["name"].str.contains(t_search, case=False, na=False)
        )
        disp_df = disp_df[m]

    st.dataframe(
        disp_df[[
            "student_id", "name", "attendance", "study_hours",
            "assignment_marks", "internal_marks", "performance_level"
        ]].rename(columns={
            "student_id": "Roll No",
            "name": "Student Name",
            "attendance": "Attendance (%)",
            "study_hours": "Study Hrs/Day",
            "assignment_marks": "Assignment (/10)",
            "internal_marks": "MSE-1 / Internal (/50)",
            "performance_level": "Status"
        }),
        use_container_width=True,
        hide_index=True
    )
    st.caption(f"Showing {len(disp_df)} of {total_students} students.")

    st.markdown("<hr style='border: none; border-top: 1px solid rgba(0, 180, 216, 0.2); margin: 24px 0 16px 0;'>", unsafe_allow_html=True)
    st.markdown("### 🚀 Project Activity")
    p1, p2 = st.columns(2)
    p1.metric("Total Student Projects", total_projects)
    p2.metric("Completed Projects", completed_projects)
    
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    p3, p4 = st.columns(2)
    p3.metric("Student Participation (With Projects)", f"{student_participation_pct:.1f}%")
    p4.metric("Popular Technologies", popular_techs_str)
