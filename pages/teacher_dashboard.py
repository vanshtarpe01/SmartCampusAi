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
    col1.metric("My Students", total_students)
    col2.metric("Avg Attendance", f"{avg_attendance:.1f}%")
    col3.metric("Avg Study Hours", f"{avg_study_hours:.1f} hrs/day")
    col4.metric("Needs Improvement", needs_improvement)
    
    st.markdown("### 🚀 Project Activity")
    p1, p2 = st.columns(2)
    p1.metric("Total Student Projects", total_projects)
    p2.metric("Completed Projects", completed_projects)
    
    st.markdown("<br>", unsafe_allow_html=True)
    p3, p4 = st.columns(2)
    p3.metric("Student Participation (With Projects)", f"{student_participation_pct:.1f}%")
    p4.metric("Popular Technologies", popular_techs_str)


    st.info("Currently SmartCampus AI uses local/demo academic data. In a future implementation, the system can be integrated with the college ERP through secure APIs so that attendance, internal marks, external marks and other academic records can be fetched automatically.")
