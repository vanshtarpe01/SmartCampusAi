"""SmartCampus AI - Main Application Entry Point
Intelligent Student Learning & Decision Support System
Built with Python and Streamlit.
Run command: streamlit run app.py
"""

import streamlit as st

# Set Streamlit page configuration as the very first Streamlit command
st.set_page_config(
    page_title="SmartCampus AI – Intelligent Student Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Custom CSS
from utils.styles import CUSTOM_CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Hide Streamlit native sidebar navigation
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Import Pages & Utilities
from utils.helpers import init_session_state, create_session_token, verify_session_token, get_user_profile
from utils.ui import render_top_brand
from pages.dashboard import render_dashboard
from pages.assistant import render_assistant
from pages.performance import render_performance
from pages.planner import render_planner
from pages.recommendations import render_recommendations
from pages.about import render_about
from pages.skills import render_skills
from pages.projects import render_projects
from pages.student_projects import render_student_projects
from pages.notifications import render_notifications
from data import get_student_data, get_all_student_summaries

# Initialize Session State
init_session_state()

# ------------------------------------------------------------
# SESSION RESTORATION & AUTHENTICATION CHECK
# ------------------------------------------------------------
# Check for persistent session token in cookies or query params to survive browser reloads
if not st.session_state.get("logged_in", False):
    cookie_token = None
    if hasattr(st, "context") and hasattr(st.context, "cookies"):
        cookie_token = st.context.cookies.get("smartcampus_session")
    session_token = st.query_params.get("session") or cookie_token

    if session_token:
        session_data = verify_session_token(session_token)
        if session_data:
            uid = session_data.get("uid")
            role = session_data.get("role")
            user_info = get_user_profile(uid)
            if user_info and user_info.get("role") == role:
                st.session_state["logged_in"] = True
                st.session_state["role"] = role
                st.session_state["user_id"] = uid
                st.session_state["user_name"] = user_info.get("name", uid)
                if role == "student":
                    st.session_state["student_id"] = uid
                    st.session_state["selected_student_id"] = uid

                # Restore previous page if saved in query params
                saved_page = st.query_params.get("page")
                if saved_page:
                    st.session_state["current_page"] = saved_page

if not st.session_state.get("logged_in", False):
    from login import render_login_page
    render_login_page()
    st.stop()

# Synchronize active session token to browser client storage
current_uid = st.session_state.get("user_id", "")
current_role = st.session_state.get("role", "")
if current_uid and current_role:
    curr_token = create_session_token(current_uid, current_role)
    if curr_token:
        if st.query_params.get("session") != curr_token:
            st.query_params["session"] = curr_token
        st.html(
            f"""
            <script>
            (function() {{
                try {{
                    localStorage.setItem("smartcampus_session", "{curr_token}");
                    sessionStorage.setItem("smartcampus_session", "{curr_token}");
                    document.cookie = "smartcampus_session={curr_token}; path=/; max-age=2592000; SameSite=Lax";
                }} catch(e) {{}}
            }})();
            </script>
            """,
            unsafe_allow_javascript=True
        )

role = st.session_state.get("role", "student")

if role == "admin":
    # Admin Navigation Mapping
    from pages.admin_dashboard import render_admin_dashboard
    from pages.admin_students import render_admin_students
    from pages.admin_recommendations import render_admin_recommendations
    from pages.manage_users import render_manage_users
    from pages.career_analysis import render_career_analysis
    from pages.pdf_report import render_pdf_report
    
    PAGES = {
        "📊 Admin Dashboard": render_admin_dashboard,
        "👥 Manage Users": render_manage_users,
        "📋 Student Academic Data": render_admin_students,
        "🎯 Academic Recommendations": render_admin_recommendations,
        "💼 Career Analysis": render_career_analysis,
        "📄 PDF Reports": render_pdf_report,
    }
elif role == "teacher":
    # Teacher Navigation Mapping
    from pages.teacher_dashboard import render_teacher_dashboard
    from pages.admin_students import render_admin_students
    from pages.admin_recommendations import render_admin_recommendations
    from pages.manage_users import render_manage_users
    from pages.career_analysis import render_career_analysis
    from pages.pdf_report import render_pdf_report
    
    PAGES = {
        "👨‍🏫 Teacher Dashboard": render_teacher_dashboard,
        "👥 Manage Students": render_manage_users,
        "📋 Student Academic Data": render_admin_students,
        "🎯 Academic Recommendations": render_admin_recommendations,
        "💼 Career Analysis": render_career_analysis,
        "📄 PDF Reports": render_pdf_report,
    }
else:
    # Student Navigation Mapping
    from pages.career_analysis import render_career_analysis
    PAGES = {
        "🏠 Dashboard": render_dashboard,
        "🤖 AI Assistant": render_assistant,
        "📊 Performance": render_performance,
        "📚 Study Planner": render_planner,
        "🎯 Recommendations": render_recommendations,
        "🛠️ Skills": render_skills,
        "📁 My Projects": render_projects,
        "🌍 Student Projects": render_student_projects,
        "🔔 Notifications": render_notifications,
        "💼 Career Analysis": render_career_analysis,
        "ℹ️ About": render_about
    }

# ------------------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """<div style="padding: 10px 0 16px 0; text-align: left;"><div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;"><div style="width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, #1a1a2e, #00b4d8); display: flex; align-items: center; justify-content: center; font-size: 20px; color: white;">🤖</div><div style="font-size: 1.35rem; font-weight: 800; color: #1a1a2e; letter-spacing: -0.02em;">SmartCampus AI</div></div><div style="font-size: 0.85rem; color: #5a6275; font-weight: 500; margin-left: 2px;">Your Intelligent Student Assistant</div></div>""",
        unsafe_allow_html=True
    )
    
    page_names = list(PAGES.keys())
    default_page = page_names[0]
    current_stored_page = st.session_state.get("current_page", default_page)
    
    # Resolve current active page key
    active_page_key = default_page
    for key in page_names:
        if current_stored_page.lower() in key.lower() or key.lower() in current_stored_page.lower():
            active_page_key = key
            break

    st.markdown("<div style='font-size: 0.74rem; font-weight: 700; color: #64748b; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px;'>Navigation Menu</div>", unsafe_allow_html=True)

    for page_key in page_names:
        is_active = (page_key == active_page_key)
        btn_type = "primary" if is_active else "secondary"
        if st.button(page_key, key=f"nav_btn_{page_key}", use_container_width=True, type=btn_type):
            st.session_state.current_page = page_key
            st.query_params["page"] = page_key
            if current_uid and current_role:
                curr_token = create_session_token(current_uid, current_role)
                if curr_token:
                    st.query_params["session"] = curr_token
            st.rerun()

    # Sidebar Student Profile Selector & Active Record
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(0, 180, 216, 0.2); margin: 18px 0 12px 0;'>", unsafe_allow_html=True)
    
    if role == "admin":
        st.markdown("<div style='font-size: 0.76rem; font-weight: 700; color: #64748b; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 6px;'>Admin Profile</div>", unsafe_allow_html=True)
        st.markdown(
            '''<div style="background: rgba(255, 255, 255, 0.9); border: 1px solid rgba(0, 180, 216, 0.22); border-radius: 12px; padding: 14px; margin-top: 8px;"><div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;"><div style="width: 34px; height: 34px; border-radius: 50%; background: linear-gradient(135deg, #1a1a2e, #00b4d8); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.82rem;">AD</div><div><div style="font-size: 0.92rem; font-weight: 700; color: #1a1a2e;">Administrator</div><div style="font-size: 0.75rem; color: #64748b;">System Access</div></div></div></div>''',
            unsafe_allow_html=True
        )
    elif role == "teacher":
        st.markdown("<div style='font-size: 0.76rem; font-weight: 700; color: #64748b; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 6px;'>Teacher Profile</div>", unsafe_allow_html=True)
        st.markdown(
            '''<div style="background: rgba(255, 255, 255, 0.9); border: 1px solid rgba(0, 180, 216, 0.22); border-radius: 12px; padding: 14px; margin-top: 8px;"><div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;"><div style="width: 34px; height: 34px; border-radius: 50%; background: linear-gradient(135deg, #f4a261, #e76f51); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.82rem;">TR</div><div><div style="font-size: 0.92rem; font-weight: 700; color: #1a1a2e;">Teacher</div><div style="font-size: 0.75rem; color: #64748b;">Faculty Access</div></div></div></div>''',
            unsafe_allow_html=True
        )
    else:
        st.markdown("<div style='font-size: 0.76rem; font-weight: 700; color: #64748b; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 6px;'>Active Student Profile</div>", unsafe_allow_html=True)
        
        selected_student_id = st.session_state.get("student_id")
        st.session_state.selected_student_id = selected_student_id
    
        # Load analyzed student data for the active student
        student = get_student_data(selected_student_id)
        
        # Initials and risk color styling
        name_parts = student["full_name"].split()
        initials = (name_parts[0][0] + (name_parts[1][0] if len(name_parts) > 1 else "")).upper()
        
        risk_color = "#2a9d8f"  # Low
        if student["risk"].upper() == "HIGH":
            risk_color = "#e63946"
        elif student["risk"].upper() == "MEDIUM":
            risk_color = "#f4a261"
    
        st.markdown(
            f'''<div style="background: rgba(255, 255, 255, 0.9); border: 1px solid rgba(0, 180, 216, 0.22); border-radius: 12px; padding: 14px; margin-top: 8px;"><div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;"><div style="width: 34px; height: 34px; border-radius: 50%; background: linear-gradient(135deg, #0077b6, #00b4d8); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.82rem;">{initials}</div><div><div style="font-size: 0.92rem; font-weight: 700; color: #1a1a2e;">{student['full_name']}</div><div style="font-size: 0.75rem; color: #64748b;">{student['student_id']} • {student['level']}</div></div></div><div style="display: flex; justify-content: space-between; font-size: 0.78rem; color: #475569; margin-top: 6px; padding-top: 6px; border-top: 1px dashed rgba(0,0,0,0.08);"><span>Att: <strong>{student['attendance']}%</strong></span><span>Score: <strong>{student['performance']}%</strong></span><span>Risk: <strong style="color: {risk_color};">{student['risk'].upper()}</strong></span></div></div>''',
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["student_id"] = None
        st.session_state["selected_student_id"] = None
        st.session_state["role"] = None
        st.session_state["user_id"] = None
        st.session_state["user_name"] = None
        st.query_params.clear()
        st.query_params["logout"] = "1"
        st.rerun()

    st.markdown(
        '''<div style="text-align: center; margin-top: 16px; font-size: 0.72rem; color: #94a3b8;">SmartCampus AI v2.0.0<br>Python AI Backend • Local Knowledge Base</div>''',
        unsafe_allow_html=True
    )

# ------------------------------------------------------------
# MAIN CONTENT RENDER
# ------------------------------------------------------------
# Render Selected View
default_render = render_admin_dashboard if role == "admin" else render_dashboard
active_page_render = PAGES.get(active_page_key, default_render)
active_page_render()
