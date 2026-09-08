"""Login page for SmartCampus AI."""

import streamlit as st
from auth import authenticate_user

def render_login_page():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px;">
            <h1 style="color: #1a1a2e; margin-bottom: 5px;">SMARTCAMPUS AI</h1>
            <h3 style="color: #64748b; font-weight: 500;">Portal Login</h3>
        </div>
        <hr style="border: none; border-top: 1px solid rgba(0, 180, 216, 0.2); margin: 20px 0;">
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            user_id = st.text_input("User ID (Student ID or 'admin')", placeholder="e.g. SC-2026-001")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submit = st.form_submit_button("LOGIN")
            
            if submit:
                auth_result = authenticate_user(user_id, password)
                if auth_result:
                    st.session_state["logged_in"] = True
                    st.session_state["role"] = auth_result["role"]
                    st.session_state["user_id"] = user_id
                    
                    if auth_result["role"] == "student":
                        st.session_state["student_id"] = user_id
                        st.session_state["selected_student_id"] = user_id
                        st.session_state["current_page"] = "Dashboard"
                    elif auth_result["role"] == "admin":
                        st.session_state["current_page"] = "Admin Dashboard"
                    elif auth_result["role"] == "teacher":
                        st.session_state["current_page"] = "Teacher Dashboard"
                        
                    st.rerun()
                else:
                    st.error("Invalid User ID or Password.")
        
        st.markdown("</div>", unsafe_allow_html=True)
