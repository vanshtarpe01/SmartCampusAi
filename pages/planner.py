"""SmartCampus AI - Study Planner Page
Generates dynamic time-blocked study schedules and active recall timelines
based on student exam dates, available daily hours, subject targets, and difficulty.
"""

import streamlit as st
import datetime
from data import generate_study_plan
from utils.ui import render_top_brand

def render_planner():
    """Renders the AI Study Planner interface."""
    st.markdown(
        """
        <div style="margin-bottom: 22px;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h2 class="smart-gradient-text" style="font-size: 1.65rem; margin: 0;">
                        📚 Smart AI Study Planner
                    </h2>
                    <p style="margin: 3px 0 0 0; color: #5a6275; font-size: 0.95rem;">
                        Automated time-blocked revision schedules optimized for active recall and exam readiness.
                    </p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <span class="smart-chip chip-amber">⚡ Spaced Repetition Engine</span>
                    <span class="smart-chip chip-teal">📅 Exam Sync Ready</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Initialize plan session state if not set
    if "generated_plan" not in st.session_state or st.session_state.generated_plan is None:
        # Generate a default high-quality plan
        today = datetime.date.today()
        exam_default = today + datetime.timedelta(days=14)
        st.session_state.generated_plan = generate_study_plan(
            exam_date=exam_default,
            available_hours=3.5,
            subject="Networking",
            weak_topic="OSI Model & TCP/IP",
            difficulty="Intermediate"
        )

    # Input Configuration Panel
    with st.container():
        st.markdown(
            """
            <h4 style="margin: 0 0 14px 0; color: #0f172a; font-size: 1.1rem; font-weight: 700;">
                ⚙️ Plan Parameters & Target Configuration
            </h4>
            """,
            unsafe_allow_html=True
        )

        row1_col1, row1_col2, row1_col3 = st.columns(3)
        with row1_col1:
            exam_date = st.date_input(
                "📅 Upcoming Exam Date",
                value=datetime.date.today() + datetime.timedelta(days=14),
                min_value=datetime.date.today()
            )
        with row1_col2:
            available_hours = st.slider(
                "⏳ Available Daily Study Hours",
                min_value=1.0,
                max_value=8.0,
                value=3.5,
                step=0.5
            )
        with row1_col3:
            subject = st.selectbox(
                "📘 Target Subject",
                options=["Networking", "Artificial Intelligence", "DBMS", "Mathematics"],
                index=0
            )

        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            weak_topics_dict = {
                "Networking": ["OSI Model & TCP/IP", "Subnetting & Routing", "DNS & HTTP/HTTPS Protocols"],
                "Artificial Intelligence": ["BFS & DFS Concepts", "A* & Heuristic Proofs", "Minimax & Alpha-Beta Pruning"],
                "DBMS": ["Normalization (1NF to BCNF)", "ACID Transactions & Locking", "SQL Query Optimization"],
                "Mathematics": ["Probability & Bayes Theorem", "Linear Transformations", "Eigenvalues & Vectors"]
            }
            weak_topic = st.selectbox(
                "🎯 Priority Focus Topic",
                options=weak_topics_dict.get(subject, ["General Foundations"])
            )
        with row2_col2:
            difficulty = st.selectbox(
                "📊 Preparation Level / Difficulty",
                options=["Beginner (Concept Building)", "Intermediate (Problem Sets)", "Advanced (Exam Mock Test)"],
                index=1
            )

        btn_clicked = st.button("🚀 Generate AI Study Plan", type="primary", width="stretch")

    if btn_clicked:
        st.session_state.generated_plan = generate_study_plan(
            exam_date=exam_date,
            available_hours=available_hours,
            subject=subject,
            weak_topic=weak_topic,
            difficulty=difficulty
        )
        st.success("✅ Smart Study Plan generated successfully!")

    # Display Generated Study Plan
    plan = st.session_state.generated_plan
    if plan:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, rgba(0, 180, 216, 0.12), rgba(244, 162, 97, 0.12)); border: 1px solid rgba(0, 180, 216, 0.3); border-radius: 14px; padding: 16px 20px; margin-bottom: 22px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <div style="font-size: 0.8rem; font-weight: 700; color: #0077b6; text-transform: uppercase;">
                            Target: {plan['primary_subject']} • Days Remaining: {plan['days_until_exam']} Days
                        </div>
                        <div style="font-size: 1.15rem; font-weight: 800; color: #1a1a2e; margin-top: 2px;">
                            Active Daily Timeline ({plan['available_hours']} Hours Scheduled)
                        </div>
                    </div>
                    <div>
                        <span class="smart-chip chip-amber">Focus: {plan['weak_topic']}</span>
                    </div>
                </div>
                <div style="margin-top: 8px; font-size: 0.88rem; color: #475569;">
                    💡 <em>{plan['ai_note']}</em>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### ⏱️ Today's Interactive Study Schedule")

        # Timeline Display
        for idx, slot in enumerate(plan["slots"]):
            is_first = idx == 0
            is_completed = slot.get("status") == "Completed"
            status_badge_color = "#2a9d8f" if is_completed else ("#f4a261" if slot.get("status") == "In Progress" else "#64748b")
            
            c_time, c_content, c_action = st.columns([1, 2.5, 1])
            
            with c_time:
                st.markdown(
                    f"""
                    <div style="font-weight: 800; font-size: 1.05rem; color: #1a1a2e; margin-top: 6px;">
                        {slot['time']}
                    </div>
                    <span class="smart-chip chip-indigo" style="font-size: 0.72rem; padding: 2px 8px;">
                        {slot['difficulty']}
                    </span>
                    """,
                    unsafe_allow_html=True
                )
            
            with c_content:
                st.markdown(
                    f"""
                    <div class="smart-glass-card" style="padding: 12px 18px; margin-bottom: 8px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 1.2rem;">{slot.get('icon', '📚')}</span>
                            <span style="font-size: 1.05rem; font-weight: 700; color: #0077b6;">
                                {slot['subject']}
                            </span>
                        </div>
                        <div style="margin-top: 4px; font-size: 0.95rem; font-weight: 600; color: #1e293b;">
                            {slot['topic']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with c_action:
                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                current_status = slot.get("status", "Pending")
                new_status = st.selectbox(
                    "Status",
                    options=["Pending", "In Progress", "Completed"],
                    index=0 if current_status == "Pending" else (1 if current_status == "In Progress" else 2),
                    key=f"slot_status_{idx}"
                )
                slot["status"] = new_status

        # Study Progress Meter
        completed_count = sum(1 for s in plan["slots"] if s.get("status") == "Completed")
        total_slots = len(plan["slots"])
        progress_pct = int((completed_count / total_slots) * 100) if total_slots > 0 else 0

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        st.markdown(f"#### 📊 Session Completion Progress: **{progress_pct}%**")
        st.progress(progress_pct / 100)

if __name__ == "__main__":
    from utils.styles import CUSTOM_CSS
    st.set_page_config(page_title="Study Planner - SmartCampus AI", page_icon="📚", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    render_top_brand()
    render_planner()
