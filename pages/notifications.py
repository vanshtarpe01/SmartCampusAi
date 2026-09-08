import streamlit as st
from data import get_student_notifications, mark_notification_read, get_student_projects
from utils.ui import render_top_brand

def render_notifications():
    st.markdown("## 🔔 Notifications")
    
    active_sid = st.session_state.get("selected_student_id")
    if not active_sid:
        st.error("Session expired.")
        return
        
    notifs = get_student_notifications(active_sid)
    
    if not notifs:
        st.info("No notifications.")
    else:
        for idx, n in enumerate(notifs):
            bg_color = "rgba(0, 180, 216, 0.05)" if not n.get("read") else "white"
            border_color = "#00b4d8" if not n.get("read") else "#e2e8f0"
            status_indicator = "🟢 New" if not n.get("read") else "⚪ Read"
            
            st.markdown(
                f"""
                <div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="font-weight: 600; font-size: 0.85rem; color: #475569;">{status_indicator} Project</span>
                        <span style="font-size: 0.8rem; color: #94a3b8;">{n['timestamp']}</span>
                    </div>
                    <div style="color: #1e293b; font-size: 1rem; margin-bottom: 8px;">{n['message']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("View Project", key=f"view_proj_{n['id']}"):
                    # Check if project is still public
                    owner_projects = get_student_projects(n['owner_id'])
                    is_public = False
                    for p in owner_projects:
                        if p.get("id") == n["project_id"] and p.get("visibility") == "Public":
                            is_public = True
                            break
                    if is_public:
                        st.session_state.current_page = "Student Projects"
                        st.rerun()
                    else:
                        st.warning("This project is no longer public or has been deleted.")
            with col2:
                if not n.get("read"):
                    if st.button("Mark as Read", key=f"mark_read_{n['id']}"):
                        mark_notification_read(active_sid, n['id'])
                        st.rerun()
                        
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
