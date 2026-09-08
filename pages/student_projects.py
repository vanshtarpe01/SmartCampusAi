import streamlit as st
from data import get_all_public_projects, update_project_inspiration
from utils.ui import render_top_brand

def render_student_projects():
    st.markdown("## 🌍 Student Projects Feed")
    st.markdown("Explore public projects built by your peers and get inspired.")
    
    active_sid = st.session_state.get("selected_student_id")
    if not active_sid:
        st.error("Session expired.")
        return
        
    public_projects = get_all_public_projects()
    
    # Filter out projects owned by the active student
    feed_projects = [p for p in public_projects if p.get("owner_id") != active_sid]
    
    if not feed_projects:
        st.info("No public projects from other students right now.")
    else:
        for p in feed_projects:
            st.markdown(
                f"""
                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                    <h3 style="margin: 0 0 8px 0; color: #1e293b; display: flex; align-items: center; gap: 8px;">
                        🌍 {p['name']}
                    </h3>
                    <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 12px;">
                        <strong>By:</strong> {p['owner_id']} &nbsp;|&nbsp; <strong>Status:</strong> {p['status']}
                    </div>
                    <p style="color: #334155; margin-bottom: 12px; line-height: 1.5;">{p['description']}</p>
                    <div style="font-size: 0.85rem; background: #f8fafc; padding: 8px 12px; border-radius: 6px; margin-bottom: 12px; display: inline-block;">
                        <strong>Tech:</strong> {p['technologies']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                insp_count = len(p.get("inspirations", []))
                if active_sid in p.get("inspirations", []):
                    st.button(f"👏 {insp_count} Inspired (You)", key=f"insp_btn_{p['id']}")
                else:
                    if st.button(f"👏 I'm Inspired", key=f"insp_btn_{p['id']}"):
                        if update_project_inspiration(p["owner_id"], p["id"], active_sid):
                            st.toast("Project inspired!")
                            st.rerun()
            with col2:
                if p.get("link"):
                    st.markdown(f"<div style='margin-top: 6px;'><a href='{p['link']}' target='_blank' style='color: #0ea5e9; font-weight: 600; text-decoration: none;'>🔗 View Project Link</a></div>", unsafe_allow_html=True)
            
            st.markdown("<hr style='border: none; margin: 20px 0;'>", unsafe_allow_html=True)
