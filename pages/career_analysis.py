import streamlit as st
import json
import os
from data import get_student_data, get_student_skills, get_student_projects

CAREER_KB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "career_kb.json")

def load_career_kb():
    if not os.path.exists(CAREER_KB_PATH):
        return {}
    with open(CAREER_KB_PATH, "r") as f:
        return json.load(f)

def render_career_analysis():
    st.markdown("## 🎯 Career & Skill Gap Analysis")
    
    
    if st.session_state.get("role") in ["admin", "teacher"]:
        from data import load_students_df
        df = load_students_df()
        active_sid = st.selectbox("Select Student", options=df["student_id"].tolist())
    else:
        active_sid = st.session_state.get("selected_student_id")

    if not active_sid:
        st.error("No student selected.")
        return
        
    student = get_student_data(active_sid)
    skills_data = get_student_skills(active_sid)
    projects_data = get_student_projects(active_sid)
    
    student_skills = [s["name"] for s in skills_data]
    
    career_kb = load_career_kb()
    
    # Calculate matches for careers based on skills
    career_matches = []
    for role, role_data in career_kb.items():
        core = set([s.lower() for s in role_data["core_skills"]])
        student_sk_lower = set([s.lower() for s in student_skills])
        match_count = len(core.intersection(student_sk_lower))
        career_matches.append((role, match_count))
        
    career_matches.sort(key=lambda x: x[1], reverse=True)
    top_career = career_matches[0][0] if career_matches else "Software Developer"
    
    st.markdown(f"### Recommended Career Direction: **{top_career}**")
    
    role_info = career_kb.get(top_career, {})
    core_skills = role_info.get("core_skills", [])
    rec_skills = role_info.get("recommended_skills", [])
    
    # Skill Gaps
    student_sk_lower_all = [s.lower() for s in student_skills]
    missing_core = [s for s in core_skills if s.lower() not in student_sk_lower_all]
    missing_rec = [s for s in rec_skills if s.lower() not in student_sk_lower_all]
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Current Strengths")
        if student_skills:
            for s in student_skills:
                st.markdown(f"- {s}")
        else:
            st.info("No skills recorded.")
            
    with col2:
        st.markdown("#### Skill Gaps (To Learn)")
        for ms in missing_core + missing_rec:
            st.markdown(f"- {ms}")
            
    st.markdown("---")
    st.markdown("### 💡 Recommended Next Project")
    example_projs = role_info.get("example_projects", ["Personal Portfolio"])
    proj = example_projs[0] if example_projs else "Full-Stack Application"
    
    st.success(f"**Project Idea:** {proj}")
    st.markdown(f"**Suggested Technologies:** {', '.join(missing_core[:2] + missing_rec[:2])}")
    st.markdown("**Reason:** This project builds upon your existing skills while introducing new core requirements for your target career.")
    
    st.markdown("---")
    st.markdown("### 🧠 Personal Assessment")
    # Using generic values, in a real scenario this would be a teacher's form
    st.markdown("- **Problem Solving**: 4/5")
    st.markdown("- **Quick Learning**: 5/5")
    st.markdown("- **Teamwork**: 4/5")
    st.caption("Self/Teacher Assessment values used as supporting inputs for guidance.")
    
