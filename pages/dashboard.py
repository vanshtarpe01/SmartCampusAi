"""SmartCampus AI - Dashboard Page
Visualizes academic health meter, metric cards, subject performance,
weekly activity trends, AI insights, and quick study action triggers.
"""

import streamlit as st
import pandas as pd
from data import (
    get_student_data,
    get_performance_data,
    get_recommendations,
    weekly_activity,
    recent_activities
)
from ai.ml_predictor import predict_performance
from ai.ml_model import get_model_metrics
from utils.ui import (
    render_top_brand,
    render_greeting,
    render_academic_health_card,
    render_ai_spotlight,
    build_subject_radar_chart,
    build_subject_bar_chart,
    build_weekly_activity_chart
)

def render_dashboard():
    """Renders the comprehensive student dashboard view."""
    active_sid = st.session_state.get("selected_student_id", "SC-2026-001")
    student = get_student_data(active_sid)
    perf_data = get_performance_data(active_sid)
    subject_perf = perf_data["subjects"]

    # Dynamic Greeting & Health Meter
    render_greeting(student.get("name", "Student"))
    render_academic_health_card(student)

    # Metric Cards Row using st.columns and st.metric
    st.markdown("### 📌 Key Academic Metrics")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            label="Overall Performance",
            value=f"{student['performance']}%",
            delta=f"Level: {student['level']}"
        )
    with m2:
        att_delta = "Eligible (≥75%)" if student['attendance'] >= 75 else "Shortage Warning (<75%)"
        st.metric(
            label="Class Attendance",
            value=f"{student['attendance']}%",
            delta=att_delta
        )
    with m3:
        hrs_delta = "Optimal (≥3.0h)" if student['study_hours'] >= 3.0 else "Needs Increase (<3.0h)"
        st.metric(
            label="Study Hours",
            value=f"{student['study_hours']} hrs/day",
            delta=hrs_delta
        )
    with m4:
        risk_label = student["risk"].upper()
        risk_delta = "Safe Zone" if risk_label == "LOW" else ("Monitor Closely" if risk_label == "MEDIUM" else "Intervention Required")
        st.metric(
            label="Academic Risk",
            value=risk_label,
            delta=risk_delta
        )

    # AI Performance Prediction Section (Phase 3 ML Integration)
    ml_pred = predict_performance(
        attendance=float(student.get("attendance", 85.0)),
        study_hours=float(student.get("study_hours", 3.5)),
        assignment_marks=float(perf_data.get("assignments", 8.0) / 10.0),
        internal_marks=float(perf_data.get("internal_test", 40.0) / 2.0),
        previous_marks=float(perf_data.get("previous_exam", 78.0))
    )
    metrics = get_model_metrics()
    acc_pct = metrics.get("accuracy", 0.0) * 100.0

    st.markdown(
        """
<div style="margin-top: 18px; margin-bottom: 8px;">
<h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #1a1a2e; display: flex; align-items: center; gap: 8px;">
<span>🤖</span> AI Performance Prediction
<span class="smart-chip chip-indigo" style="font-size: 0.75rem;">Decision Tree Model</span>
</h3>
</div>
""",
        unsafe_allow_html=True
    )
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.metric(
            label="Predicted Level",
            value=ml_pred["predicted_level"],
            delta=f"Confidence: {ml_pred['confidence']:.0f}%"
        )
    with p2:
        st.metric(
            label="Risk",
            value=student["risk"],
            delta="Evaluated"
        )
    with p3:
        st.metric(
            label="ML Model Accuracy",
            value=f"{acc_pct:.0f}%",
            delta="Decision Tree"
        )
    with p4:
        st.metric(
            label="Important Factor",
            value=ml_pred["top_factor"],
            delta="Gini Split"
        )

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Visualizations Row: Subject Performance & Weekly Activity
    col_chart1, col_chart2 = st.columns([1.1, 0.9])

    with col_chart1:
        st.markdown(
            """
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
<h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #1a1a2e;">
📊 Subject Performance Matrix
</h3>
<span class="smart-chip chip-indigo">4 Active Courses</span>
</div>
""",
            unsafe_allow_html=True
        )

        chart_tab1, chart_tab2 = st.tabs(["📈 Bar Chart", "🧭 Knowledge Radar"])
        with chart_tab1:
            fig_bar = build_subject_bar_chart(subject_perf)
            st.plotly_chart(fig_bar, use_container_width=True)
        with chart_tab2:
            fig_radar = build_subject_radar_chart(subject_perf)
            st.plotly_chart(fig_radar, use_container_width=True)

        # Subject breakdown table
        sub_df = pd.DataFrame([
            {"Subject": k, "Score": f"{v}%", "Target": "75%", "Status": "On Track" if v >= 74 else "Action Needed"}
            for k, v in subject_perf.items()
        ])
        st.dataframe(sub_df, use_container_width=True, hide_index=True)

    with col_chart2:
        st.markdown(
            """
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
<h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #1a1a2e;">
📅 Weekly Study Activity
</h3>
<span class="smart-chip chip-teal">Goal: 3.0 hrs/day</span>
</div>
""",
            unsafe_allow_html=True
        )
        fig_week = build_weekly_activity_chart(weekly_activity)
        st.plotly_chart(fig_week, use_container_width=True)

        # Weekly Activity summary table
        week_df = pd.DataFrame([
            {"Day": d, "Hours": f"{h:.1f} hrs", "Goal Status": "✓ Met" if h >= 2.5 else "⚠ Review"}
            for d, h in weekly_activity.items()
        ])
        st.dataframe(week_df, use_container_width=True, hide_index=True)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # Dynamic AI Insight Section
    recs = get_recommendations(student_id=active_sid)
    primary_rec = recs[0]["description"] if recs else "Maintain steady daily revision and adhere to regular practice problem schedules."
    render_ai_spotlight(
        insight=perf_data["ai_insight"],
        recommendation=primary_rec
    )

    # Bottom Row: Recent Activity Timeline and Quick Actions
    col_timeline, col_actions = st.columns([1.1, 0.9])

    with col_timeline:
        st.markdown(
            """
<h3 style="font-size: 1.15rem; font-weight: 700; color: #1a1a2e; margin-bottom: 12px;">
⏱️ Recent Academic Activity
</h3>
""",
            unsafe_allow_html=True
        )

        for act in recent_activities:
            badge_color = "#00b4d8" if act["badge"] in ["Completed", "Verified"] else "#f4a261"
            st.markdown(
                f"""
<div class="smart-glass-card" style="padding: 12px 16px; margin-bottom: 10px;">
<div style="display: flex; justify-content: space-between; align-items: center;">
<span style="font-size: 0.78rem; font-weight: 600; color: #64748b;">{act['time']}</span>
<span style="background: rgba(0, 180, 216, 0.12); color: {badge_color}; padding: 2px 8px; border-radius: 10px; font-size: 0.72rem; font-weight: 700;">
{act['badge']}
</span>
</div>
<div style="font-size: 0.92rem; font-weight: 600; color: #1e293b; margin-top: 4px;">
{act['title']}
</div>
</div>
""",
                unsafe_allow_html=True
            )

    with col_actions:
        st.markdown(
            """
<h3 style="font-size: 1.15rem; font-weight: 700; color: #1a1a2e; margin-bottom: 8px;">
⚡ Quick Actions & Study Hub
</h3>
<p style="font-size: 0.88rem; color: #475569; margin: 0 0 14px 0;">
Jump directly into high-impact academic actions curated by your AI companion.
</p>
""",
            unsafe_allow_html=True
        )

        b1, b2 = st.columns(2)
        with b1:
            if st.button("📝 Start Study Session", use_container_width=True):
                st.session_state.current_page = "Study Planner"
                st.rerun()
        with b2:
            if st.button("🤖 Ask AI Assistant", use_container_width=True):
                st.session_state.current_page = "AI Assistant"
                st.rerun()

        b3, b4 = st.columns(2)
        with b3:
            if st.button("📊 View Performance", use_container_width=True):
                st.session_state.current_page = "Performance"
                st.rerun()
        with b4:
            if st.button("🎯 Priority Focus", use_container_width=True):
                st.session_state.current_page = "Recommendations"
                st.rerun()

if __name__ == "__main__":
    from utils.styles import CUSTOM_CSS
    st.set_page_config(page_title="Dashboard - SmartCampus AI", page_icon="🏠", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    render_top_brand()
    render_dashboard()
