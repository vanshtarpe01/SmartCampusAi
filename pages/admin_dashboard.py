import streamlit as st
from data import load_students_df, get_all_projects_data
from auth import get_all_users_by_role

def render_admin_dashboard():
    st.markdown("## 📊 Admin Dashboard")
    st.markdown("Overview of all system data.")
    
    df = load_students_df()
    
    teachers = get_all_users_by_role("teacher")
    
    total_students = len(df)
    total_teachers = len(teachers)
    
    avg_attendance = df["attendance"].mean() if not df.empty else 0
    avg_study_hours = df["study_hours"].mean() if not df.empty else 0
    avg_internal = df["internal_marks"].mean() if not df.empty else 0
    avg_previous = df["previous_marks"].mean() if not df.empty else 0
    
    needs_improvement = len(df[df["performance_level"] == "Needs Improvement"]) if not df.empty else 0
    
    projects_data = get_all_projects_data()
    total_projects = 0
    public_projects = 0
    private_projects = 0
    completed_projects = 0
    
    tech_counts = {}
    students_with_projects = 0
    
    for sid, projs in projects_data.items():
        if len(projs) > 0:
            students_with_projects += 1
        total_projects += len(projs)
        for p in projs:
            if p.get("visibility") == "Public":
                public_projects += 1
            else:
                private_projects += 1
            if p.get("status") == "Completed":
                completed_projects += 1
                
            techs = p.get("technologies", "")
            if techs:
                for t in [x.strip() for x in techs.split(",") if x.strip()]:
                    tech_counts[t] = tech_counts.get(t, 0) + 1
                    
    popular_techs = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    popular_techs_str = ", ".join([f"{t[0]} ({t[1]})" for t in popular_techs]) if popular_techs else "None"
    student_participation_pct = (students_with_projects / total_students * 100) if total_students > 0 else 0
                
    st.markdown("### 📌 Users & Academic Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", total_students)
    col2.metric("Total Teachers", total_teachers)
    col3.metric("Avg Attendance", f"{avg_attendance:.1f}%")
    col4.metric("Avg Study Hours", f"{avg_study_hours:.1f} hrs/day")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col5, col6, col7 = st.columns(3)
    col5.metric("Avg Internal Marks", f"{avg_internal:.1f}/50")
    col6.metric("Avg Previous Marks", f"{avg_previous:.1f}/100")
    col7.metric("Needs Improvement", needs_improvement)
    
    st.markdown("### 🚀 Project Analysis")
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Total Projects", total_projects)
    p2.metric("Completed", completed_projects)
    p3.metric("Public Projects", public_projects)
    p4.metric("Private Projects", private_projects)
    
    st.markdown("<br>", unsafe_allow_html=True)
    p5, p6 = st.columns(2)
    p5.metric("Student Participation (With Projects)", f"{student_participation_pct:.1f}%")
    p6.metric("Popular Technologies", popular_techs_str)


    st.info("Currently SmartCampus AI uses local/demo academic data. In a future implementation, the system can be integrated with the college ERP through secure APIs so that attendance, internal marks, external marks and other academic records can be fetched automatically.")
