"""SmartCampus AI - Recommendations Page
Displays personalized, prioritized academic recommendations with category badges,
impact/effort matrix tags, and filterable priority levels.
"""

import streamlit as st
from data import get_recommendations, get_student_data, get_admin_recommendation
from utils.ui import render_top_brand

def render_recommendations():
    """Renders the prioritized recommendations view."""
    active_sid = st.session_state.get("selected_student_id", "SC-2026-001")
    student = get_student_data(active_sid)

    st.markdown(
        f"""
<div style="margin-bottom: 22px;">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
<div>
<h2 class="smart-gradient-text" style="font-size: 1.65rem; margin: 0;">
🎯 Personalized Recommendations
</h2>
<p style="margin: 3px 0 0 0; color: #5a6275; font-size: 0.95rem;">
Data-driven interventions prioritized for <strong>{student['full_name']}</strong> ({student['student_id']}) to maximize grade progression and subject mastery.
</p>
</div>
<div style="display: flex; gap: 8px;">
<span class="smart-chip chip-coral">⚡ Priority Engine</span>
<span class="smart-chip chip-teal">Risk: {student['risk'].upper()}</span>
</div>
</div>
</div>
""",
        unsafe_allow_html=True
    )

    # -----------------------------------------------------------------
    # ADMIN ACADEMIC RECOMMENDATION (STUDY HOURS GUIDANCE)
    # -----------------------------------------------------------------
    admin_rec = get_admin_recommendation(active_sid)
    if admin_rec:
        st.markdown(
            f"""
            <div style="background: rgba(42, 157, 143, 0.08); border: 1px solid #2a9d8f; border-radius: 12px; padding: 20px; margin-bottom: 24px;">
                <h3 style="margin-top: 0; color: #2a9d8f; display: flex; align-items: center; gap: 8px;">
                    <span>👨‍🏫</span> Faculty / Mentor Guidance
                </h3>
                <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 12px;">
                    <div><strong>Recommended Study Time:</strong> <span style="background: white; padding: 2px 8px; border-radius: 6px; border: 1px solid #ddd;">{admin_rec.get('recommended_hours', 'N/A')} hours/day</span></div>
                    <div><strong>Identified Weak Area:</strong> <span style="background: white; padding: 2px 8px; border-radius: 6px; border: 1px solid #ddd;">{admin_rec.get('weak_area', 'N/A')}</span></div>
                </div>
                <p style="color: #334155; margin: 0 0 10px 0; font-style: italic;">"{admin_rec.get('guidance', '')}"</p>
                <div style="font-size: 0.8rem; color: #64748b; border-top: 1px solid rgba(42, 157, 143, 0.2); padding-top: 8px;">
                    <strong>Note:</strong> This is a recommendation to help you plan your studies. You control your own study schedule.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Filter Control Row
    col_filter, col_stat = st.columns([1.2, 2.8])
    with col_filter:
        priority_filter = st.selectbox(
            "Filter by Priority Level:",
            options=["All", "High Priority", "Medium Priority", "Low Priority"],
            index=0
        )

    recs = get_recommendations(priority_filter, student_id=active_sid)

    with col_stat:
        st.markdown(
            f"""
<div style="display: flex; gap: 12px; align-items: center; height: 100%; padding-top: 24px;">
<span style="font-size: 0.9rem; color: #64748b;">
Showing <strong>{len(recs)}</strong> recommended actions for filter <strong>"{priority_filter}"</strong>
</span>
</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)

    # Render Recommendation Cards
    if not recs:
        st.info("No recommendations found for the selected filter.")
    else:
        for rec in recs:
            prio = rec["priority"].upper()
            if "HIGH" in prio:
                card_border = "#e63946"
                chip_class = "chip-coral"
            elif "MEDIUM" in prio:
                card_border = "#f4a261"
                chip_class = "chip-amber"
            else:
                card_border = "#2a9d8f"
                chip_class = "chip-emerald"

            st.markdown(
                f"""
<div class="smart-glass-card" style="border-left: 5px solid {card_border}; padding: 18px 22px; margin-bottom: 16px;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px; margin-bottom: 8px;">
<div style="display: flex; align-items: center; gap: 10px;">
<span style="font-size: 1.5rem;">{rec.get('icon', '📌')}</span>
<div>
<h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #1a1a2e;">
{rec['title']}
</h3>
<span style="font-size: 0.8rem; color: #64748b; font-weight: 500;">
Category: {rec['category']}
</span>
</div>
</div>
<div style="display: flex; gap: 8px; align-items: center;">
<span class="smart-chip {chip_class}">{rec['priority']}</span>
<span class="smart-chip chip-indigo">Impact: {rec['impact']}</span>
<span class="smart-chip chip-teal">Effort: {rec['effort']}</span>
</div>
</div>

<p style="margin: 8px 0 12px 0; font-size: 0.94rem; color: #334155; line-height: 1.5;">
{rec['description']}
</p>

<div style="background: rgba(255, 255, 255, 0.7); border-radius: 8px; padding: 8px 14px; display: inline-flex; align-items: center; gap: 8px; border: 1px solid rgba(0,0,0,0.06);">
<span style="font-size: 0.85rem; font-weight: 700; color: #0077b6;">Target Outcome:</span>
<span style="font-size: 0.88rem; font-weight: 600; color: #1e293b;">{rec['target']}</span>
</div>
</div>
""",
                unsafe_allow_html=True
            )

    # Priority Matrix Visual Concept
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    st.markdown("### 🧭 Strategic Impact vs. Effort Matrix")
    
    col_mat1, col_mat2 = st.columns(2)
    with col_mat1:
        st.markdown(
            """
<div class="smart-glass-card" style="padding: 16px;">
<h4 style="margin: 0 0 8px 0; color: #e63946; font-size: 0.98rem; font-weight: 700;">
⚡ Quick Wins (High Impact, Low/Medium Effort)
</h4>
<ul style="margin: 0; padding-left: 20px; font-size: 0.9rem; color: #334155;">
<li><strong>Networking Review:</strong> 30 mins daily OSI layer drill</li>
<li><strong>DBMS Normalization:</strong> 5 schema decompositions</li>
</ul>
</div>
""",
            unsafe_allow_html=True
        )
    with col_mat2:
        st.markdown(
            """
<div class="smart-glass-card" style="padding: 16px;">
<h4 style="margin: 0 0 8px 0; color: #2a9d8f; font-size: 0.98rem; font-weight: 700;">
🛡️ Sustained Foundations (Routine Maintenance)
</h4>
<ul style="margin: 0; padding-left: 20px; font-size: 0.9rem; color: #334155;">
<li><strong>Attendance Shield:</strong> Keep class attendance above 80%</li>
<li><strong>Study Consistency:</strong> Rebalance Thursday study dips</li>
</ul>
</div>
""",
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    from utils.styles import CUSTOM_CSS
    st.set_page_config(page_title="Recommendations - SmartCampus AI", page_icon="🎯", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    render_top_brand()
    render_recommendations()
