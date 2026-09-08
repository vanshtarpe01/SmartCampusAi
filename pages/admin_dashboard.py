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
    col1.metric("Total Enrolled Students", total_students)
    col2.metric("Total Faculty / Teachers", total_teachers)
    col3.metric("Avg Attendance", f"{avg_attendance:.1f}%")
    col4.metric("Avg Study Hours", f"{avg_study_hours:.1f} hrs/day")
    
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    col5, col6, col7 = st.columns(3)
    col5.metric("Avg Internal Marks", f"{avg_internal:.1f}/50")
    col6.metric("Avg Previous Marks", f"{avg_previous:.1f}/100")
    col7.metric("Needs Improvement", needs_improvement)
    
    # -------------------------------------------------------------------------
    # ENROLLED STUDENTS ROSTER (CSE-AIML SEM-V)
    # -------------------------------------------------------------------------
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(0, 180, 216, 0.2); margin: 24px 0 16px 0;'>", unsafe_allow_html=True)
    st.markdown(f"### 🎓 Enrolled Students Roster — B.Tech CSE (AIML) Sem-V ({total_students} Students)")
    st.caption("Real-world class data synchronized with Supabase database.")

    # Performance Level Pills
    p_exc = len(df[df["performance_level"] == "Excellent"])
    p_good = len(df[df["performance_level"] == "Good"])
    p_avg = len(df[df["performance_level"] == "Average"])
    p_ni = len(df[df["performance_level"] == "Needs Improvement"])

    pill_col1, pill_col2, pill_col3, pill_col4 = st.columns(4)
    with pill_col1:
        st.info(f"🌟 **Excellent:** {p_exc} students")
    with pill_col2:
        st.success(f"✅ **Good:** {p_good} students")
    with pill_col3:
        st.warning(f"⚡ **Average:** {p_avg} students")
    with pill_col4:
        st.error(f"⚠️ **Needs Improvement:** {p_ni} students")

    # Search & Filter Controls
    search_c1, search_c2 = st.columns([3, 1])
    with search_c1:
        student_search = st.text_input("🔍 Search student by Roll No or Name:", placeholder="e.g. MLU25S211 or Vansh Tarpe", key="admin_dash_search")
    with search_c2:
        perf_filter = st.selectbox("Filter Level:", ["All Levels", "Excellent", "Good", "Average", "Needs Improvement"], key="admin_dash_perf_filter")

    filtered_df = df.copy()
    if student_search:
        s_mask = (
            filtered_df["student_id"].str.contains(student_search, case=False, na=False) |
            filtered_df["name"].str.contains(student_search, case=False, na=False)
        )
        filtered_df = filtered_df[s_mask]

    if perf_filter != "All Levels":
        filtered_df = filtered_df[filtered_df["performance_level"] == perf_filter]

    display_cols = [
        "student_id", "name", "attendance", "study_hours",
        "assignment_marks", "internal_marks", "previous_marks", "performance_level"
    ]
    renamed_cols = {
        "student_id": "Roll No",
        "name": "Student Name",
        "attendance": "Attendance (%)",
        "study_hours": "Study Hrs/Day",
        "assignment_marks": "Assignment (/10)",
        "internal_marks": "MSE-1 / Internal (/50)",
        "previous_marks": "Previous (%)",
        "performance_level": "Performance Status"
    }
    
    st.dataframe(
        filtered_df[display_cols].rename(columns=renamed_cols),
        use_container_width=True,
        hide_index=True
    )
    st.caption(f"Showing {len(filtered_df)} of {total_students} students.")

    # -------------------------------------------------------------------------
    # FACULTY ROSTER
    # -------------------------------------------------------------------------
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(0, 180, 216, 0.2); margin: 24px 0 16px 0;'>", unsafe_allow_html=True)
    st.markdown(f"### 👨‍🏫 Department Faculty & Teaching Staff ({total_teachers} Members)")
    
    if teachers:
        t_cols = st.columns(min(len(teachers), 4))
        for idx, (t_id, t_info) in enumerate(teachers.items()):
            col_target = t_cols[idx % len(t_cols)]
            with col_target:
                st.markdown(
                    f"""
                    <div style="background: white; border: 1px solid rgba(0, 119, 182, 0.2); border-radius: 12px; padding: 12px; margin-bottom: 10px;">
                        <div style="font-weight: 700; color: #1a1a2e; font-size: 0.95rem;">{t_info.get('name', t_id)}</div>
                        <div style="font-size: 0.8rem; color: #64748b;">Code: <code>{t_id}</code></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # -------------------------------------------------------------------------
    # PROJECT ANALYSIS
    # -------------------------------------------------------------------------
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(0, 180, 216, 0.2); margin: 24px 0 16px 0;'>", unsafe_allow_html=True)
    st.markdown("### 🚀 Student Project & Innovation Metrics")
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Total Projects", total_projects)
    p2.metric("Completed", completed_projects)
    p3.metric("Public Projects", public_projects)
    p4.metric("Private Projects", private_projects)
    
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    p5, p6 = st.columns(2)
    p5.metric("Student Participation (With Projects)", f"{student_participation_pct:.1f}%")
    p6.metric("Popular Technologies", popular_techs_str)
