"""SmartCampus AI - Student Academic Performance Page
Focused strictly on the student's personal academic performance, official institutional
evaluations, study habits, strengths, diagnostic insights, and learning trajectory.
"""

import streamlit as st
import pandas as pd
from data import (
    get_student_data,
    get_performance_data,
    update_student_study_hours
)
from utils.ui import (
    build_performance_timeline_chart,
    build_wellness_radar
)


def render_performance():
    """Renders the student-centric academic performance dashboard."""
    active_sid = st.session_state.get("selected_student_id", "MLU25S211")
    student = get_student_data(active_sid)
    perf_data = get_performance_data(active_sid)

    # Risk badge styling
    risk_chip_class = "chip-emerald"
    if str(student.get("risk", "")).upper() == "HIGH":
        risk_chip_class = "chip-coral"
    elif str(student.get("risk", "")).upper() == "MEDIUM":
        risk_chip_class = "chip-amber"

    # Page Header
    st.markdown(
        f"""
<div style="margin-bottom: 20px;">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
        <div>
            <h2 class="smart-gradient-text" style="font-size: 1.65rem; margin: 0;">
                📊 Student Academic Performance
            </h2>
            <p style="margin: 3px 0 0 0; color: #5a6275; font-size: 0.95rem;">
                Official academic records, diagnostic evaluation, and performance analysis for <strong>{student['full_name']}</strong> ({student['student_id']}).
            </p>
        </div>
        <div style="display: flex; gap: 8px;">
            <span class="smart-chip chip-indigo">Level: {student['level']}</span>
            <span class="smart-chip {risk_chip_class}">Risk: {student['risk'].upper()}</span>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True
    )

    # =========================================================================
    # SECTION 1: OFFICIAL INSTITUTIONAL ACADEMIC RECORDS (READ-ONLY)
    # =========================================================================
    st.markdown("### 🏫 Institutional Academic Records")
    st.markdown(
        """
<p style="color: #64748b; font-size: 0.88rem; margin-top: -6px; margin-bottom: 14px;">
    🔒 <em>Official records entered and authenticated by faculty & department examination controllers. These official academic parameters are strictly read-only for students.</em>
</p>
""",
        unsafe_allow_html=True
    )

    rec_col1, rec_col2, rec_col3, rec_col4 = st.columns(4)
    with rec_col1:
        att_val = student.get("attendance", 0.0)
        att_status = "Eligible (≥75%)" if att_val >= 75.0 else "Shortage (<75%)"
        st.metric(
            label="Classroom Attendance",
            value=f"{att_val:.1f}%",
            delta=att_status,
            delta_color="normal" if att_val >= 75.0 else "inverse"
        )
    with rec_col2:
        internal_val = student.get("internal_marks", 0.0)
        internal_pct = (internal_val / 50.0) * 100.0 if internal_val <= 50.0 else internal_val
        st.metric(
            label="Internal Test (MSE-1)",
            value=f"{internal_val:.1f} / 50",
            delta=f"{internal_pct:.1f}% Score"
        )
    with rec_col3:
        assign_val = student.get("assignment_marks", 0.0)
        st.metric(
            label="Assignment Submissions",
            value=f"{assign_val:.1f} / 10",
            delta="Continuous Assessment"
        )
    with rec_col4:
        prev_val = student.get("previous_marks", 0.0)
        st.metric(
            label="Previous Semester Score",
            value=f"{prev_val:.1f}%",
            delta="Historical Aggregate"
        )

    st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 2: STUDENT SELF-STUDY TRACKER (THE ONLY FIELD STUDENT CAN UPDATE)
    # =========================================================================
    st.markdown("### ⏱️ Personal Self-Study Hours")
    st.markdown(
        """
<p style="color: #64748b; font-size: 0.88rem; margin-top: -6px; margin-bottom: 12px;">
    ✏️ <em>Students can log and update their daily self-study hours. Your logged study hours directly refine your study schedule and AI academic pacing.</em>
</p>
""",
        unsafe_allow_html=True
    )

    with st.container():
        study_col1, study_col2, study_col3 = st.columns([1.2, 1.0, 1.8])
        with study_col1:
            current_study_hours = float(student.get("study_hours", 3.5))
            new_study_hours = st.number_input(
                "Self-Study Duration (hours/day)",
                min_value=0.0,
                max_value=24.0,
                value=current_study_hours,
                step=0.5,
                help="Enter your average daily dedicated self-study hours outside class."
            )
        with study_col2:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            if st.button("💾 Save Study Hours", type="primary", use_container_width=True):
                success = update_student_study_hours(active_sid, new_study_hours)
                if success:
                    st.toast(f"✅ Study hours successfully updated to {new_study_hours:.1f} hrs/day!", icon="📚")
                    st.success(f"✅ Study hours updated to **{new_study_hours:.1f} hrs/day**. Record saved to database.")
                    st.rerun()
                else:
                    st.error("Failed to update study hours. Please try again.")
        with study_col3:
            st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
            if new_study_hours >= 4.0:
                st.info("🌟 **High Study Habit:** You are spending 4+ hours daily on focused self-study. Excellent consistency!")
            elif new_study_hours >= 2.5:
                st.info("👍 **Steady Study Habit:** Solid daily dedication. Aim to maintain 3+ hours during mid-term preparation.")
            else:
                st.warning("⚠️ **Low Study Hours:** Increasing daily self-study to at least 2.5–3 hours will boost your test scores.")

    st.markdown("<div style='margin-top: 22px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 3: ACADEMIC PERFORMANCE & DIAGNOSTIC STANDING
    # =========================================================================
    st.markdown("### 🎯 Academic Performance Standing")

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown(
            f"""
<div class="smart-glass-card" style="padding: 16px; text-align: center; border-top: 3px solid #00b4d8;">
    <div style="font-size: 0.82rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Overall Score</div>
    <div style="font-size: 2.1rem; font-weight: 800; color: #1a1a2e; margin: 4px 0;">{student['performance']}%</div>
    <div style="font-size: 0.82rem; color: #0077b6; font-weight: 600;">Composite Index</div>
</div>
""",
            unsafe_allow_html=True
        )
    with p2:
        st.markdown(
            f"""
<div class="smart-glass-card" style="padding: 16px; text-align: center; border-top: 3px solid #2a9d8f;">
    <div style="font-size: 0.82rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Performance Tier</div>
    <div style="font-size: 1.8rem; font-weight: 800; color: #2a9d8f; margin: 6px 0;">{student['level']}</div>
    <div style="font-size: 0.82rem; color: #64748b;">Academic Standing</div>
</div>
""",
            unsafe_allow_html=True
        )
    with p3:
        risk_color = "#2a9d8f" if student['risk'].upper() == "LOW" else ("#f4a261" if student['risk'].upper() == "MEDIUM" else "#e63946")
        st.markdown(
            f"""
<div class="smart-glass-card" style="padding: 16px; text-align: center; border-top: 3px solid {risk_color};">
    <div style="font-size: 0.82rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Academic Risk</div>
    <div style="font-size: 1.8rem; font-weight: 800; color: {risk_color}; margin: 6px 0;">{student['risk'].upper()}</div>
    <div style="font-size: 0.82rem; color: #64748b;">Risk Assessment</div>
</div>
""",
            unsafe_allow_html=True
        )
    with p4:
        st.markdown(
            f"""
<div class="smart-glass-card" style="padding: 16px; text-align: center; border-top: 3px solid #7209b7;">
    <div style="font-size: 0.82rem; color: #64748b; font-weight: 600; text-transform: uppercase;">Daily Study</div>
    <div style="font-size: 2.1rem; font-weight: 800; color: #7209b7; margin: 4px 0;">{student['study_hours']} <span style="font-size: 1rem;">h</span></div>
    <div style="font-size: 0.82rem; color: #64748b;">Hours per Day</div>
</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 4: STRENGTHS, ACTION AREAS & AI INSIGHTS
    # =========================================================================
    col_str, col_ai = st.columns([1.1, 1.1])

    with col_str:
        st.markdown("#### 🌟 Key Academic Strengths")
        strengths = student.get("strengths", [])
        if strengths:
            for s in strengths:
                st.markdown(
                    f"""
<div style="background: rgba(42, 157, 143, 0.08); border-left: 4px solid #2a9d8f; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; display: flex; align-items: center; gap: 10px;">
    <span style="color: #2a9d8f; font-size: 1.1rem; font-weight: 800;">✓</span>
    <span style="color: #1e293b; font-size: 0.92rem; font-weight: 500;">{s}</span>
</div>
""",
                    unsafe_allow_html=True
                )
        else:
            st.info("No recorded strengths yet.")

        weak_areas = student.get("weak_areas", [])
        if weak_areas:
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            st.markdown("#### ⚠️ Areas for Improvement")
            for w in weak_areas:
                st.markdown(
                    f"""
<div style="background: rgba(230, 57, 70, 0.08); border-left: 4px solid #e63946; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; display: flex; align-items: center; gap: 10px;">
    <span style="color: #e63946; font-size: 1.1rem; font-weight: 800;">⚠</span>
    <span style="color: #1e293b; font-size: 0.92rem; font-weight: 500;">{w}</span>
</div>
""",
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                """
<div style="background: rgba(0, 180, 216, 0.08); border-left: 4px solid #00b4d8; border-radius: 8px; padding: 10px 14px; margin-top: 10px; display: flex; align-items: center; gap: 10px;">
    <span style="font-size: 1.1rem;">🎯</span>
    <span style="color: #1e293b; font-size: 0.92rem; font-weight: 500;">Zero critical risk flags identified across your academic metrics! Keep up the great work.</span>
</div>
""",
                unsafe_allow_html=True
            )

    with col_ai:
        st.markdown("#### 💡 Personalized AI Academic Insight")
        observations = student.get("observations", [])
        obs_html = "".join([
            f"<li style='margin-bottom: 8px; color: #334155; line-height: 1.5;'>{obs}</li>"
            for obs in observations
        ])

        st.markdown(
            f"""
<div class="smart-glass-card" style="padding: 18px; border-left: 4px solid #0077b6;">
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
        <span style="font-size: 1.25rem;">🤖</span>
        <h4 style="margin: 0; font-size: 1.05rem; font-weight: 700; color: #0f172a;">Academic Advisor Evaluation</h4>
    </div>
    <p style="color: #334155; font-size: 0.92rem; line-height: 1.55; margin-bottom: 12px;">
        Student <strong>{student['full_name']}</strong> maintains an outstanding institutional standing with an overall academic performance of <strong>{student['performance']}%</strong> ({student['level']}). Daily self-study dedication of <strong>{student['study_hours']} hrs/day</strong> combined with <strong>{student['attendance']}%</strong> classroom immersion reflects exemplary consistency.
    </p>
    <div style="font-size: 0.88rem; font-weight: 700; color: #0077b6; margin-bottom: 6px;">Key Observations:</div>
    <ul style="margin: 0; padding-left: 20px; font-size: 0.9rem;">
        {obs_html if obs_html else "<li>Profile demonstrates exemplary academic rigor across all monitored indicators.</li><li>Student is well-positioned for top-bracket academic honors and competitive placements.</li>"}
    </ul>
</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 5: HISTORICAL TRAJECTORY & ACADEMIC WELLNESS
    # =========================================================================
    st.markdown("### 📈 Continuous Evaluation Trajectory & Wellness")
    col_chart_left, col_chart_right = st.columns([1.2, 0.8])

    with col_chart_left:
        fig_timeline = build_performance_timeline_chart(perf_data.get("timeline", []))
        st.plotly_chart(fig_timeline, use_container_width=True)
        st.caption("Weekly trajectory generated from continuous evaluation and assignment records.")

    with col_chart_right:
        fig_wellness = build_wellness_radar(perf_data.get("wellness", {}))
        st.plotly_chart(fig_wellness, use_container_width=True)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 6: GRANULAR SUBJECT BREAKDOWN
    # =========================================================================
    st.markdown("### 📚 Granular Subject Breakdown")
    sub_details = perf_data.get("subject_details", {})
    records = []
    for sub, det in sub_details.items():
        records.append({
            "Subject": sub,
            "Total Score": f"{det.get('score', 0)}%",
            "Assignments": f"{det.get('assignments', 0)}%",
            "Quizzes": f"{det.get('quizzes', 0)}%",
            "Midterm": f"{det.get('midterm', 0)}%",
            "Trend": "↑ Ascending" if det.get("trend") == "up" else ("↓ Falling" if det.get("trend") == "down" else "→ Stable"),
            "Academic Status": det.get("status", "Good")
        })
    df_details = pd.DataFrame(records)
    st.dataframe(df_details, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    from utils.styles import CUSTOM_CSS
    st.set_page_config(page_title="Performance - SmartCampus AI", page_icon="📊", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    render_performance()
