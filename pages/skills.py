import streamlit as st
import uuid
from data import get_student_skills, save_student_skills
from utils.ui import render_top_brand

def render_skills():
    st.markdown("## 🛠️ My Skills")
    st.markdown("Manage your technical and soft skills portfolio.")
    
    active_sid = st.session_state.get("selected_student_id")
    if not active_sid:
        st.error("Session expired.")
        return
        
    skills = get_student_skills(active_sid)
    
    # Check if we're editing a skill
    edit_skill_id = st.session_state.get("edit_skill_id")
    
    if edit_skill_id:
        skill_to_edit = next((s for s in skills if s["id"] == edit_skill_id), None)
        if skill_to_edit:
            with st.expander("✏️ Edit Skill", expanded=True):
                with st.form("edit_skill_form"):
                    e_name = st.text_input("Skill Name", value=skill_to_edit["name"])
                    e_cat = st.text_input("Category", value=skill_to_edit["category"])
                    e_lvl = st.selectbox("Proficiency Level", ["Beginner", "Intermediate", "Advanced", "Expert"], index=["Beginner", "Intermediate", "Advanced", "Expert"].index(skill_to_edit["level"]))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Save Changes"):
                            if e_name.strip():
                                skill_to_edit["name"] = e_name.strip()
                                skill_to_edit["category"] = e_cat.strip()
                                skill_to_edit["level"] = e_lvl
                                save_student_skills(active_sid, skills)
                                st.session_state.edit_skill_id = None
                                st.success("Skill updated!")
                                st.rerun()
                            else:
                                st.error("Skill Name cannot be empty.")
                    with col2:
                        if st.form_submit_button("Cancel"):
                            st.session_state.edit_skill_id = None
                            st.rerun()
    else:
        with st.expander("➕ Add New Skill", expanded=False):
            with st.form("add_skill_form", clear_on_submit=True):
                skill_name = st.text_input("Skill Name (e.g., Python, React)")
                skill_category = st.text_input("Category (e.g., Programming, Design)")
                skill_level = st.selectbox("Proficiency Level", ["Beginner", "Intermediate", "Advanced", "Expert"])
                
                submit = st.form_submit_button("Add Skill")
                if submit:
                    if skill_name.strip():
                        new_skill = {
                            "id": str(uuid.uuid4()),
                            "name": skill_name.strip(),
                            "category": skill_category.strip(),
                            "level": skill_level
                        }
                        skills.append(new_skill)
                        save_student_skills(active_sid, skills)
                        st.success(f"Skill '{skill_name}' added!")
                        st.rerun()
                    else:
                        st.error("Skill Name cannot be empty.")
                        
    st.markdown("### Current Skills")
    if not skills:
        st.info("You haven't added any skills yet.")
    else:
        for idx, skill in enumerate(skills):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(
                    f"""
                    <div style="background: rgba(255, 255, 255, 0.9); border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; padding: 12px; margin-bottom: 8px;">
                        <h4 style="margin: 0; color: #1a1a2e;">{skill['name']}</h4>
                        <div style="font-size: 0.85rem; color: #64748b; margin-top: 4px;">
                            <span style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; margin-right: 8px;">{skill['category']}</span>
                            <span style="color: #0077b6; font-weight: 600;">{skill['level']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col2:
                if st.button("✏️ Edit", key=f"edit_skill_{skill['id']}"):
                    st.session_state.edit_skill_id = skill['id']
                    st.rerun()
            with col3:
                if st.button("🗑️ Delete", key=f"del_skill_{skill['id']}"):
                    skills.pop(idx)
                    save_student_skills(active_sid, skills)
                    st.rerun()
