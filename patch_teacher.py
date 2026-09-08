with open("pages/teacher_dashboard.py", "r") as f:
    content = f.read()

import re
old_section = """    projects_data = get_all_projects_data()
    total_projects = 0
    completed_projects = 0
    
    for sid, projs in projects_data.items():
        total_projects += len(projs)
        for p in projs:
            if p.get("status") == "Completed":
                completed_projects += 1
                
    st.markdown("### 📌 My Students Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("My Students", total_students)
    col2.metric("Avg Attendance", f"{avg_attendance:.1f}%")
    col3.metric("Avg Study Hours", f"{avg_study_hours:.1f} hrs/day")
    col4.metric("Needs Improvement", needs_improvement)
    
    st.markdown("### 🚀 Project Activity")
    p1, p2 = st.columns(2)
    p1.metric("Total Student Projects", total_projects)
    p2.metric("Completed Projects", completed_projects)"""

new_section = """    projects_data = get_all_projects_data()
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
    p4.metric("Popular Technologies", popular_techs_str)"""

if old_section in content:
    content = content.replace(old_section, new_section)
    with open("pages/teacher_dashboard.py", "w") as f:
        f.write(content)
    print("Patched teacher_dashboard.py")
else:
    print("Could not find section in teacher_dashboard.py")
