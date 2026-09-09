"""SmartCampus AI - Modern Executive Login Portal
Features:
- Academic & Futuristic glassmorphic card design
- Interactive Role Tabs (Student, Teacher, Admin) with instant Auto-fill & Suggestion Dropdowns
- 1-Click Direct Sign-In buttons
- Form input state management with reliable session state synchronization
- Clear authentication error feedback and session handling
"""

import streamlit as st
from auth import authenticate_user, create_session_token

def set_credentials(uid: str, pwd: str):
    """Callback to reliably update session state input widgets."""
    st.session_state["login_user_id"] = uid
    st.session_state["login_password"] = pwd

def perform_direct_login(uid: str, pwd: str):
    """Directly authenticates and transitions to user's role page."""
    auth_result = authenticate_user(uid, pwd)
    if auth_result:
        role = auth_result["role"]
        st.session_state["logged_in"] = True
        st.session_state["role"] = role
        st.session_state["user_id"] = uid
        st.session_state["user_name"] = auth_result.get("name", uid)

        # Generate persistent session token to prevent logout on browser reload
        token = create_session_token(uid, role)
        if token:
            st.query_params["session"] = token

        if role == "student":
            st.session_state["student_id"] = uid
            st.session_state["selected_student_id"] = uid
            target_page = "Dashboard"
        elif role == "admin":
            target_page = "Admin Dashboard"
        elif role == "teacher":
            target_page = "Teacher Dashboard"
        else:
            target_page = "Dashboard"

        st.session_state["current_page"] = target_page
        st.query_params["page"] = target_page

        st.rerun()
    else:
        st.error(f"Invalid credentials for {uid}. Please check your password.")

def render_login_page():
    # Hide sidebar on login screen and apply custom login background
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] { display: none !important; }
            .login-container {
                max-width: 500px;
                margin: 30px auto 20px auto;
                background: #ffffff;
                border: 1px solid rgba(0, 119, 182, 0.22);
                border-radius: 20px;
                padding: 32px 28px;
                box-shadow: 0 16px 40px -10px rgba(15, 23, 42, 0.12);
                position: relative;
            }
            .login-badge {
                width: 56px;
                height: 56px;
                border-radius: 16px;
                background: linear-gradient(135deg, #1a1a2e, #0077b6);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 28px;
                color: white;
                margin: 0 auto 12px auto;
                box-shadow: 0 8px 20px rgba(0, 119, 182, 0.35);
            }
            .login-title {
                text-align: center;
                font-size: 1.75rem;
                font-weight: 800;
                color: #1a1a2e;
                margin-bottom: 4px;
                letter-spacing: -0.02em;
            }
            .login-subtitle {
                text-align: center;
                color: #64748b;
                font-size: 0.88rem;
                font-weight: 500;
                margin-bottom: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Initialize demo filler in session state if not set
    if "login_user_id" not in st.session_state:
        st.session_state["login_user_id"] = "MLU25S211"
    if "login_password" not in st.session_state:
        st.session_state["login_password"] = "student123"

    # Centered container layout
    _, col_center, _ = st.columns([1, 2.2, 1])

    with col_center:
        st.markdown(
            """
            <div class="login-container">
                <div class="login-badge">🤖</div>
                <div class="login-title smart-gradient-text">SmartCampus AI</div>
                <div class="login-subtitle">Intelligent Student Learning & Decision Support System</div>
            """,
            unsafe_allow_html=True
        )

        # Quick Role Selectors & 1-Click Demo Fill Tabs
        st.markdown(
            """
            <div style="font-size: 0.80rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">
                ⚡ Select Role & Autofill Suggestions
            </div>
            """,
            unsafe_allow_html=True
        )

        tab_student, tab_teacher, tab_admin = st.tabs(["🎓 Student", "👨‍🏫 Teacher", "🛡️ Admin"])

        with tab_student:
            st.markdown(
                """<div style="font-size: 0.82rem; color: #64748b; margin-bottom: 6px;">
                    Default Student: <code>MLU25S211</code> (Vansh Tarpe) • Pass: <code>student123</code>
                </div>""",
                unsafe_allow_html=True
            )
            
            # Real student options for autofill suggestions
            try:
                from data import load_students_df
                st_df = load_students_df()
                student_options = ["-- Select student to autofill --"] + [
                    f"{r['student_id']} - {r['name']}" for _, r in st_df.iterrows()
                ]
            except Exception:
                student_options = ["-- Select student to autofill --", "MLU25S211 - Vansh Vasant Tarpe"]

            sel_student = st.selectbox(
                "💡 Autofill Suggestion (Class Roster):",
                options=student_options,
                key="sb_autofill_student",
                help="Pick any student from your real CSE(AIML) Sem-V class to autofill credentials"
            )

            if sel_student and sel_student != "-- Select student to autofill --":
                chosen_roll = sel_student.split(" - ")[0].strip()
                if st.session_state.get("login_user_id") != chosen_roll:
                    set_credentials(chosen_roll, "student123")
                    st.rerun()

            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                st.button(
                    "✨ Autofill Vansh",
                    key="btn_fill_student",
                    use_container_width=True,
                    on_click=set_credentials,
                    args=("MLU25S211", "student123")
                )
            with c_btn2:
                if st.button("🚀 1-Click Login", key="btn_quick_student", type="primary", use_container_width=True):
                    perform_direct_login("MLU25S211", "student123")

        with tab_teacher:
            st.markdown(
                """<div style="font-size: 0.82rem; color: #64748b; margin-bottom: 6px;">
                    Faculty: <code>SSK</code> (Prof. Khatri) • Pass: <code>teacher123</code>
                </div>""",
                unsafe_allow_html=True
            )
            teacher_options = [
                "-- Select faculty to autofill --",
                "SSK - Prof. S. S. Khatri (AI)",
                "NCM - Dr. N. C. Mhala (DBMS)",
                "API - Prof. A. P. Ingle (OS)",
                "RAK - Prof. R. A. Kalamkar (MAD)",
                "VBK - Dr. V. B. Kute (DSA)",
                "ZIK - Dr. Z. I. Khan (HOD)",
                "VUD - Prof. V. U. Deshmukh"
            ]
            sel_teacher = st.selectbox(
                "💡 Autofill Suggestion (Faculty):",
                options=teacher_options,
                key="sb_autofill_teacher",
                help="Pick a faculty member from the Master Time Table to autofill credentials"
            )
            if sel_teacher and sel_teacher != "-- Select faculty to autofill --":
                chosen_tch = sel_teacher.split(" - ")[0].strip()
                if st.session_state.get("login_user_id") != chosen_tch:
                    set_credentials(chosen_tch, "teacher123")
                    st.rerun()

            c_t1, c_t2 = st.columns(2)
            with c_t1:
                st.button(
                    "✨ Autofill SSK",
                    key="btn_fill_teacher",
                    use_container_width=True,
                    on_click=set_credentials,
                    args=("SSK", "teacher123")
                )
            with c_t2:
                if st.button("🚀 1-Click Login", key="btn_quick_teacher", type="primary", use_container_width=True):
                    perform_direct_login("SSK", "teacher123")

        with tab_admin:
            st.markdown(
                """<div style="font-size: 0.82rem; color: #64748b; margin-bottom: 6px;">
                    Administrator: <code>admin</code> • Pass: <code>admin123</code>
                </div>""",
                unsafe_allow_html=True
            )
            c_a1, c_a2 = st.columns(2)
            with c_a1:
                st.button(
                    "✨ Autofill Admin",
                    key="btn_fill_admin",
                    use_container_width=True,
                    on_click=set_credentials,
                    args=("admin", "admin123")
                )
            with c_a2:
                if st.button("🚀 1-Click Login", key="btn_quick_admin", type="primary", use_container_width=True):
                    perform_direct_login("admin", "admin123")

        # Login Inputs & Sign In (Directly synchronized without st.form isolation)
        user_id = st.text_input(
            "User ID / Student ID",
            key="login_user_id",
            placeholder="e.g. MLU25S211, SSK, or admin",
            help="Enter your assigned campus ID or select from suggestions above"
        )
        password = st.text_input(
            "Password",
            key="login_password",
            type="password",
            placeholder="Enter your account password"
        )

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

        if st.button("Sign In to Portal ➔", key="btn_submit_login", type="primary", use_container_width=True):
            clean_uid = st.session_state.get("login_user_id", "").strip()
            clean_pwd = st.session_state.get("login_password", "").strip()

            if not clean_uid or not clean_pwd:
                st.error("Please enter both User ID and Password.")
            else:
                perform_direct_login(clean_uid, clean_pwd)

        st.markdown(
            """
            <div style="margin-top: 24px; padding-top: 14px; border-top: 1px solid #f1f5f9; text-align: center; font-size: 0.75rem; color: #94a3b8;">
                🔒 Secure 256-bit Encrypted Session • SmartCampus AI v2.0
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )
