"""SmartCampus AI - Performance Analysis Page
In-depth academic analytics, rule-based diagnostics, and Machine Learning
Decision Tree predictions with explainable AI factors, model metrics, and confusion matrix.
Combines Phase 2 Rule Engine with Phase 3 Machine Learning.
"""

import streamlit as st
import pandas as pd
from data import (
    get_student_data,
    get_performance_data
)
from ai.performance import analyze_student
from ai.ml_predictor import predict_performance
from ai.ml_model import get_model_metrics, get_feature_importance
from ai.model_utils import validate_student_inputs, combine_rule_and_ml
from utils.ui import (
    render_top_brand,
    build_performance_timeline_chart,
    build_wellness_radar,
    build_feature_importance_chart,
    build_confusion_matrix_heatmap
)


def render_performance():
    """Renders the unified Rule-Based and Machine Learning Performance Hub."""
    active_sid = st.session_state.get("selected_student_id", "SC-2026-001")
    perf_data = get_performance_data(active_sid)
    student = get_student_data(active_sid)

    st.markdown(
        f"""
<div style="margin-bottom: 22px;">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
<div>
<h2 class="smart-gradient-text" style="font-size: 1.65rem; margin: 0;">
📊 Student Performance Analysis & ML Predictor
</h2>
<p style="margin: 3px 0 0 0; color: #5a6275; font-size: 0.95rem;">
Dual-engine academic diagnostic combining <strong>Rule-Based Expert System</strong> with <strong>Decision Tree Machine Learning</strong> for <strong>{student['full_name']}</strong> ({student['student_id']}).
</p>
</div>
<div style="display: flex; gap: 8px;">
<span class="smart-chip chip-indigo">Decision Tree ML</span>
<span class="smart-chip chip-teal">Rule Engine Active</span>
</div>
</div>
</div>
""",
        unsafe_allow_html=True
    )

    # =========================================================================
    # INTERACTIVE STUDENT INPUT CONTROLS
    # =========================================================================
    st.markdown("### 🎛️ Student Academic Parameters")
    st.caption("Adjust the academic parameters below or use the active student's preloaded values, then click **Analyze Performance**.")

    # Container with clean inputs
    with st.container():
        in_col1, in_col2, in_col3, in_col4, in_col5 = st.columns(5)
        with in_col1:
            input_attendance = st.number_input(
                "Attendance (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(student.get("attendance", 85.0)),
                step=1.0,
                help="Class attendance percentage (0–100%)"
            )
        with in_col2:
            input_study_hours = st.number_input(
                "Study Hours (hrs/day)",
                min_value=0.0,
                max_value=24.0,
                value=float(student.get("study_hours", 3.5)),
                step=0.5,
                help="Average self-study duration per day (0–24 hrs)"
            )
        with in_col3:
            input_assignment = st.number_input(
                "Assignment Marks (0-10)",
                min_value=0.0,
                max_value=10.0,
                value=float(perf_data.get("assignments", 8.0) / 10.0),
                step=0.5,
                help="Continuous evaluation assignment marks out of 10"
            )
        with in_col4:
            input_internal = st.number_input(
                "Internal Marks (0-50)",
                min_value=0.0,
                max_value=50.0,
                value=float(perf_data.get("internal_test", 40.0) / 2.0),
                step=1.0,
                help="Mid-semester test score scaled out of 50"
            )
        with in_col5:
            input_previous = st.number_input(
                "Previous Marks (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(perf_data.get("previous_exam", 78.0)),
                step=1.0,
                help="Historical semester aggregate score (0–100%)"
            )

    btn_col1, btn_col2 = st.columns([0.25, 0.75])
    with btn_col1:
        run_analysis = st.button("🚀 Analyze Performance", type="primary", width="stretch")

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    # Input validation
    is_valid, err_msg = validate_student_inputs(
        input_attendance,
        input_study_hours,
        input_assignment,
        input_internal,
        input_previous
    )

    if not is_valid:
        st.error(f"⚠️ Validation Error: {err_msg}")
        return

    # Execute Rule Engine and ML Engine
    rule_analysis = analyze_student({
        "attendance": input_attendance,
        "study_hours": input_study_hours,
        "assignment_marks": input_assignment,
        "internal_marks": input_internal,
        "previous_marks": input_previous
    })

    ml_prediction = predict_performance(
        attendance=input_attendance,
        study_hours=input_study_hours,
        assignment_marks=input_assignment,
        internal_marks=input_internal,
        previous_marks=input_previous
    )

    combined_ai = combine_rule_and_ml(rule_analysis, ml_prediction)

    # =========================================================================
    # SECTION 1: RULE-BASED ANALYSIS & SECTION 2: MACHINE LEARNING PREDICTION
    # =========================================================================
    sec_col1, sec_col2 = st.columns(2)

    with sec_col1:
        st.markdown(
            """
<div class="smart-glass-card" style="padding: 18px; border-top: 4px solid #0077b6;">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
<div style="display: flex; align-items: center; gap: 8px;">
<span style="font-size: 1.25rem;">📐</span>
<h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #1a1a2e;">
SECTION 1: Rule-Based Analysis
</h3>
</div>
<span class="smart-chip chip-indigo">Deterministic Rules</span>
</div>
""",
            unsafe_allow_html=True
        )
        rk1, rk2, rk3 = st.columns(3)
        with rk1:
            st.metric("Performance Score", f"{rule_analysis['overall']}%")
        with rk2:
            st.metric("Performance Level", rule_analysis["level"])
        with rk3:
            st.metric("Risk Level", rule_analysis["risk"])

        st.markdown(
            f"""
<div style="margin-top: 10px; font-size: 0.88rem; color: #475569; background: rgba(0, 119, 182, 0.05); padding: 10px; border-radius: 8px;">
<strong>Academic Evaluation Rule:</strong> Score calculated via institutional weighting (Attendance 20%, Study 15%, Assignments 15%, Internal 25%, Previous 25%).
</div>
</div>
""",
            unsafe_allow_html=True
        )

    with sec_col2:
        st.markdown(
            """
<div class="smart-glass-card" style="padding: 18px; border-top: 4px solid #2a9d8f;">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
<div style="display: flex; align-items: center; gap: 8px;">
<span style="font-size: 1.25rem;">🌲</span>
<h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #1a1a2e;">
SECTION 2: Machine Learning Prediction
</h3>
</div>
<span class="smart-chip chip-emerald">Decision Tree (Depth 5)</span>
</div>
""",
            unsafe_allow_html=True
        )
        mk1, mk2, mk3 = st.columns(3)
        with mk1:
            st.metric("Predicted Performance", ml_prediction["predicted_level"])
        with mk2:
            st.metric("Prediction Confidence", f"{ml_prediction['confidence']:.0f}%")
        with mk3:
            st.metric("Primary Factor", ml_prediction["top_factor"])

        st.markdown(
            f"""
<div style="margin-top: 10px; font-size: 0.88rem; color: #475569; background: rgba(42, 157, 143, 0.05); padding: 10px; border-radius: 8px;">
<strong>Pattern Recognition:</strong> Decision tree traversal matched historical patterns from {student['name']}'s peer cohort.
</div>
</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 3: IMPORTANT FACTORS & SECTION 4: AI INSIGHT
    # =========================================================================
    sec_col3, sec_col4 = st.columns([1.0, 1.0])

    with sec_col3:
        st.markdown("### 📊 SECTION 3: Important Factors")
        st.caption("Calculated dynamically from the Decision Tree model's Gini importance values.")
        feat_fig = build_feature_importance_chart(ml_prediction["feature_importance"])
        st.plotly_chart(feat_fig, width="stretch")

    with sec_col4:
        st.markdown("### 💡 SECTION 4: AI Insight & Explainability")
        reasons_items = "".join([
            f"""<div style="display: flex; align-items: flex-start; gap: 8px; font-size: 0.86rem; margin-bottom: 6px;">
<span style="color: {'#065f46' if r['type'] == 'positive' else ('#b91c1c' if r['type'] == 'warning' else '#64748b')}; font-weight: 800;">{'✓' if r['type'] == 'positive' else ('⚠' if r['type'] == 'warning' else '•')}</span>
<span style="color: #334155;">{r['text']}</span>
</div>"""
            for r in combined_ai["reasons"]
        ])
        st.markdown(
            f"""
<div class="smart-glass-card" style="padding: 18px; border-left: 4px solid #0077b6; height: 93%;">
<div style="font-weight: 700; color: #0f172a; margin-bottom: 8px; font-size: 1.05rem;">
🤖 Automated AI Synthesis
</div>
<p style="color: #334155; font-size: 0.95rem; line-height: 1.5; margin-bottom: 12px;">
{combined_ai['ai_insight']}
</p>
<div style="font-size: 0.88rem; font-weight: 600; color: #0077b6; margin-bottom: 6px;">
Consensus Evaluation:
</div>
<p style="font-size: 0.88rem; color: #475569; margin-bottom: 12px;">
{combined_ai['consensus_text']}
</p>
<div style="font-size: 0.88rem; font-weight: 600; color: #0f172a; margin-bottom: 8px;">
Key Contributing Factors:
</div>
<div style="display: flex; flex-direction: column;">
{reasons_items}
</div>
</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # MACHINE LEARNING PERFORMANCE PREDICTOR: MODEL EVALUATION & DIAGNOSTICS
    # =========================================================================
    st.markdown("---")
    st.markdown("### 🌲 Machine Learning Performance Predictor")
    st.markdown(
        """
<p style="color: #475569; font-size: 0.95rem; margin-top: -6px; margin-bottom: 16px;">
SmartCampus AI uses a <strong>Decision Tree Machine Learning model</strong> to predict student performance based on academic and learning factors. The model is trained on a realistic local educational dataset and evaluated against an independent test partition.
</p>
""",
        unsafe_allow_html=True
    )

    # Model Metrics Display
    metrics = get_model_metrics()
    acc_pct = metrics.get("accuracy", 0.0) * 100.0
    prec_pct = metrics.get("precision", 0.0) * 100.0
    rec_pct = metrics.get("recall", 0.0) * 100.0
    f1_pct = metrics.get("f1_score", 0.0) * 100.0

    met1, met2, met3, met4, met5 = st.columns(5)
    with met1:
        st.metric("Model Architecture", "Decision Tree", delta="max_depth=5")
    with met2:
        st.metric("Model Accuracy", f"{acc_pct:.1f}%", delta="Test Partition")
    with met3:
        st.metric("Precision (Weighted)", f"{prec_pct:.1f}%")
    with met4:
        st.metric("Recall (Weighted)", f"{rec_pct:.1f}%")
    with met5:
        st.metric("F1 Score", f"{f1_pct:.1f}%")

    st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)

    # Confusion Matrix & How it Works
    col_diag_left, col_diag_right = st.columns([1.0, 1.0])

    with col_diag_left:
        st.markdown("#### 🎯 Performance Prediction Confusion Matrix")
        st.caption("Visualizes correct classifications along the diagonal vs misclassifications on the held-out test dataset.")
        cm_data = metrics.get("confusion_matrix", [[0]])
        cm_classes = metrics.get("classes", ["Average", "Excellent", "Good", "Needs Improvement"])
        cm_fig = build_confusion_matrix_heatmap(cm_data, cm_classes)
        st.plotly_chart(cm_fig, width="stretch")

    with col_diag_right:
        st.markdown("#### ❓ How does the prediction work?")
        st.markdown(
            """
<div class="smart-glass-card" style="padding: 16px;">
<ol style="margin: 0; padding-left: 20px; color: #334155; font-size: 0.9rem; line-height: 1.6;">
<li><strong>Student enters academic information:</strong> Attendance, daily study hours, continuous assignment marks, internal test scores, and previous marks are gathered.</li>
<li><strong>Feature extraction & normalization:</strong> The system formats input features into a structured vector matching the training schema.</li>
<li><strong>Decision Tree traversal:</strong> The trained model evaluates conditional branch thresholds (e.g. <em>attendance &ge; 75%</em>, <em>internal_marks &ge; 35</em>) learned from historical student records.</li>
<li><strong>Performance category prediction:</strong> The leaf node outputs the predicted academic tier (<em>Excellent</em>, <em>Good</em>, <em>Average</em>, or <em>Needs Improvement</em>) with confidence probability.</li>
<li><strong>Hybrid Rule + ML synthesis:</strong> SmartCampus AI fuses ML pattern recognition with rule-based institutional policies to produce explainable guidance.</li>
</ol>
</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # HISTORICAL TRAJECTORY & ACADEMIC WELLNESS (PHASE 2 VISUALIZATIONS)
    # =========================================================================
    st.markdown("### 📈 Continuous Evaluation Trajectory & Wellness")
    col_chart_left, col_chart_right = st.columns([1.2, 0.8])

    with col_chart_left:
        fig_timeline = build_performance_timeline_chart(perf_data["timeline"])
        st.plotly_chart(fig_timeline, width="stretch")
        st.caption("Weekly trajectory generated from continuous evaluation and assignment records.")

    with col_chart_right:
        fig_wellness = build_wellness_radar(perf_data["wellness"])
        st.plotly_chart(fig_wellness, width="stretch")

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # Granular Subject Breakdown Table
    st.markdown("### 📚 Granular Subject Breakdown")
    sub_details = perf_data.get("subject_details", {})
    records = []
    for sub, det in sub_details.items():
        records.append({
            "Subject": sub,
            "Total Score": f"{det['score']}%",
            "Assignments": f"{det['assignments']}%",
            "Quizzes": f"{det['quizzes']}%",
            "Midterm": f"{det['midterm']}%",
            "Trend": "↑ Ascending" if det["trend"] == "up" else ("↓ Falling" if det["trend"] == "down" else "→ Stable"),
            "Academic Status": det["status"]
        })
    df_details = pd.DataFrame(records)
    st.dataframe(df_details, width="stretch", hide_index=True)


if __name__ == "__main__":
    from utils.styles import CUSTOM_CSS
    st.set_page_config(page_title="Performance - SmartCampus AI", page_icon="📊", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    render_top_brand()
    render_performance()
