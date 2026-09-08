import streamlit as st
import uuid
from data import get_student_projects, save_student_projects, create_public_project_notification
from utils.ui import render_top_brand

def render_projects():
    st.markdown("## 📁 My Projects")
    st.markdown("Manage your personal and academic projects.")
    
    active_sid = st.session_state.get("selected_student_id")
    if not active_sid:
        st.error("Session expired.")
        return
        
    projects = get_student_projects(active_sid)
    
    edit_proj_id = st.session_state.get("edit_proj_id")
    
    if edit_proj_id:
        proj_to_edit = next((p for p in projects if p["id"] == edit_proj_id), None)
        if proj_to_edit:
            with st.expander("✏️ Edit Project", expanded=True):
                with st.form("edit_project_form"):
                    e_name = st.text_input("Project Name *", value=proj_to_edit["name"])
                    e_desc = st.text_area("Description *", value=proj_to_edit["description"])
                    e_tech = st.text_input("Technologies", value=proj_to_edit.get("technologies", ""))
                    e_link = st.text_input("Project Link", value=proj_to_edit.get("link", ""))
                    e_status = st.selectbox("Status", ["Idea", "In Progress", "Completed"], index=["Idea", "In Progress", "Completed"].index(proj_to_edit["status"]))
                    e_visibility = st.selectbox("Visibility", ["Private", "Public"], index=["Private", "Public"].index(proj_to_edit.get("visibility", "Private")))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Save Changes"):
                            if e_name.strip() and e_desc.strip():
                                prev_vis = proj_to_edit.get("visibility", "Private")
                                proj_to_edit["name"] = e_name.strip()
                                proj_to_edit["description"] = e_desc.strip()
                                proj_to_edit["technologies"] = e_tech.strip()
                                proj_to_edit["link"] = e_link.strip()
                                proj_to_edit["status"] = e_status
                                proj_to_edit["visibility"] = e_visibility
                                save_student_projects(active_sid, projects)
                                
                                if prev_vis == "Private" and e_visibility == "Public":
                                    create_public_project_notification(active_sid, proj_to_edit)
                                
                                st.session_state.edit_proj_id = None
                                st.success("Project updated!")
                                st.rerun()
                            else:
                                st.error("Name and Description are required.")
                    with col2:
                        if st.form_submit_button("Cancel"):
                            st.session_state.edit_proj_id = None
                            st.rerun()
    else:
        with st.expander("➕ Add New Project", expanded=False):
            with st.form("add_project_form", clear_on_submit=True):
                p_name = st.text_input("Project Name *")
                p_desc = st.text_area("Description *")
                p_tech = st.text_input("Technologies (comma-separated)")
                p_link = st.text_input("Project Link (Optional)")
                p_status = st.selectbox("Status", ["Idea", "In Progress", "Completed"])
                p_visibility = st.selectbox("Visibility", ["Private", "Public"])
                
                submit = st.form_submit_button("Save Project")
                if submit:
                    if p_name.strip() and p_desc.strip():
                        new_proj = {
                            "id": str(uuid.uuid4()),
                            "name": p_name.strip(),
                            "description": p_desc.strip(),
                            "technologies": p_tech.strip(),
                            "link": p_link.strip(),
                            "status": p_status,
                            "visibility": p_visibility,
                            "inspirations": []
                        }
                        projects.append(new_proj)
                        save_student_projects(active_sid, projects)
                        
                        if p_visibility == "Public":
                            create_public_project_notification(active_sid, new_proj)
                            
                        st.success(f"Project '{p_name}' added!")
                        st.rerun()
                    else:
                        st.error("Project Name and Description are required.")
                    
    st.markdown("### Existing Projects")
    if not projects:
        st.info("You haven't added any projects yet.")
    else:
        for idx, p in enumerate(projects):
            vis_icon = "🌍" if p.get("visibility") == "Public" else "🔒"
            st.markdown("---")
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"#### {vis_icon} {p['name']}")
                st.markdown(f"**Status:** {p['status']} | **Visibility:** {p.get('visibility', 'Private')}")
                st.write(p['description'])
                st.markdown(f"**Tech:** {p.get('technologies', '')}")
                if p.get('link'):
                    st.markdown(f"[View Project]({p['link']})")
                
                insp_count = len(p.get("inspirations", []))
                if p.get("visibility") == "Public" and insp_count > 0:
                    st.caption(f"👏 {insp_count} students inspired")
                    
            with col2:
                # Toggle Visibility
                new_vis = "Private" if p.get("visibility") == "Public" else "Public"
                if st.button(f"Make {new_vis}", key=f"toggle_vis_{p['id']}"):
                    p["visibility"] = new_vis
                    save_student_projects(active_sid, projects)
                    if new_vis == "Public":
                        create_public_project_notification(active_sid, p)
                    st.rerun()
                
                if st.button("✏️ Edit", key=f"edit_proj_{p['id']}"):
                    st.session_state.edit_proj_id = p['id']
                    st.rerun()
                    
                if st.button("🗑️ Delete", key=f"del_proj_{p['id']}"):
                    projects.pop(idx)
                    save_student_projects(active_sid, projects)
                    st.rerun()
