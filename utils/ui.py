"""SmartCampus AI - Reusable UI Components & Plotly Chart Visualizers
Provides custom rendered cards, health meters, badges, and academic visualizations.
"""

from typing import Dict, Any, List, Optional
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Theme Color Constants
COLOR_INDIGO = "#1a1a2e"
COLOR_TEAL = "#00b4d8"
COLOR_DEEP_BLUE = "#0077b6"
COLOR_AMBER = "#f4a261"
COLOR_EMERALD = "#2a9d8f"
COLOR_CORAL = "#e63946"
COLOR_BG_CARD = "rgba(255, 255, 255, 0.85)"

def render_top_brand():
    """Renders the top branding and header section."""
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, #1a1a2e, #00b4d8); display: flex; align-items: center; justify-content: center; font-size: 22px; color: white; box-shadow: 0 4px 14px rgba(0, 180, 216, 0.35);">
                    🤖
                </div>
                <div>
                    <h1 class="smart-gradient-text" style="font-size: 2rem; margin: 0; line-height: 1.1;">SmartCampus AI</h1>
                    <p style="margin: 0; color: #5a6275; font-size: 0.95rem; font-weight: 500;">
                        Intelligent Student Learning & Decision Support System
                    </p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span class="smart-chip chip-teal">⚡ Phase 1: Prototype</span>
                <span class="smart-chip chip-indigo">🎓 SC-2026</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_greeting(student_name: str = "Student"):
    """Renders personalized greeting banner."""
    st.markdown(
        f"""
        <div style="margin-top: 14px; margin-bottom: 22px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
            <div>
                <h2 style="font-size: 1.45rem; font-weight: 700; margin: 0; color: #1a1a2e;">
                    Good Morning, {student_name} 👋
                </h2>
                <p style="margin: 2px 0 0 0; color: #64748b; font-size: 0.9rem;">
                    Here is your real-time academic pulse and AI recommendations for today.
                </p>
            </div>
            <div style="display: flex; gap: 8px;">
                <span class="smart-chip chip-emerald">Academic Risk: LOW</span>
                <span class="smart-chip chip-amber">Weekly Goal: 80%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_academic_health_card(student: Dict[str, Any]):
    """Renders the comprehensive Academic Health Meter hero card."""
    perf = student.get("performance", 78)
    attendance = student.get("attendance", 82)
    study_hours = student.get("study_hours", 3.2)
    risk = student.get("risk", "LOW").upper()
    level = student.get("level", "GOOD").upper()
    assignments = student.get("assignments", 86)

    # Risk badge styling
    risk_color = "#2a9d8f" if risk == "LOW" else "#e76f51"

    html = f"""
    <div class="health-meter-box">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
            <div>
                <div style="font-size: 0.8rem; letter-spacing: 0.08em; text-transform: uppercase; color: #00b4d8; font-weight: 700; margin-bottom: 4px;">
                    ✦ ACADEMIC HEALTH METER
                </div>
                <div style="font-size: 1.85rem; font-weight: 800; line-height: 1.2; margin-bottom: 6px;">
                    Overall Index: {perf}%
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <span style="background: rgba(0, 180, 216, 0.25); border: 1px solid rgba(0, 180, 216, 0.5); padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 700; color: #caf0f8;">
                        LEVEL: {level}
                    </span>
                    <span style="background: rgba(42, 157, 143, 0.25); border: 1px solid {risk_color}; padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 700; color: #a7f3d0;">
                        RISK LEVEL: {risk}
                    </span>
                </div>
            </div>
            
            <div style="display: flex; gap: 20px; text-align: center; flex-wrap: wrap;">
                <div style="background: rgba(255, 255, 255, 0.08); padding: 12px 18px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.12); min-width: 100px;">
                    <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Attendance</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin-top: 2px;">{attendance}%</div>
                    <div style="font-size: 0.7rem; color: #2a9d8f; font-weight: 600;">+2% from baseline</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.08); padding: 12px 18px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.12); min-width: 100px;">
                    <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Study Pace</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin-top: 2px;">{study_hours} <span style="font-size: 0.85rem; font-weight: 500;">hrs/day</span></div>
                    <div style="font-size: 0.7rem; color: #f4a261; font-weight: 600;">Target: 3.5 hrs</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.08); padding: 12px 18px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.12); min-width: 100px;">
                    <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Assignments</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin-top: 2px;">{assignments}%</div>
                    <div style="font-size: 0.7rem; color: #00b4d8; font-weight: 600;">Top 10% Decile</div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_ai_spotlight(
    insight: str = "Your overall performance is good, but your Networking score is below your other subjects.",
    recommendation: str = "Spend 30 additional minutes per day practicing Networking."
):
    """Renders the AI Spotlight recommendation card."""
    html = f"""
    <div class="ai-spotlight-box">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.25rem;">🤖</span>
                <span style="font-size: 0.82rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: #0077b6;">
                    AI INSIGHT & SPOTLIGHT
                </span>
            </div>
            <span class="smart-chip chip-amber">Attention Recommended</span>
        </div>
        <p style="margin: 0 0 10px 0; font-size: 0.98rem; font-weight: 600; color: #1e293b; line-height: 1.5;">
            "{insight}"
        </p>
        <div style="background: rgba(255, 255, 255, 0.85); border-left: 3px solid #00b4d8; padding: 10px 14px; border-radius: 6px;">
            <div style="font-size: 0.76rem; font-weight: 700; text-transform: uppercase; color: #0077b6; margin-bottom: 2px;">
                Recommended Action:
            </div>
            <div style="font-size: 0.92rem; color: #334155; font-weight: 500;">
                {recommendation}
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ============================================================
# CREATIVE CHARTS WITH PLOTLY
# ============================================================

def build_subject_radar_chart(subjects_dict: Dict[str, int]) -> go.Figure:
    """Creates a stylized Knowledge Radar chart for subject performance."""
    categories = list(subjects_dict.keys())
    values = list(subjects_dict.values())
    
    # Close polygon
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()

    # Student polygon
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(0, 180, 216, 0.25)',
        line=dict(color='#0077b6', width=2.5),
        name='Your Score (%)',
        marker=dict(size=7, color='#1a1a2e')
    ))

    # Benchmark target polygon
    fig.add_trace(go.Scatterpolar(
        r=[75, 75, 75, 75, 75],
        theta=categories_closed,
        fill='none',
        line=dict(color='rgba(244, 162, 97, 0.7)', width=1.5, dash='dot'),
        name='Class Target (75%)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10, color='#64748b'),
                gridcolor='rgba(0, 180, 216, 0.15)'
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='#1a1a2e', family='Plus Jakarta Sans'),
                gridcolor='rgba(0, 180, 216, 0.15)'
            ),
            bgcolor='rgba(255, 255, 255, 0.4)'
        ),
        margin=dict(l=35, r=35, t=25, b=25),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        height=320,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def build_subject_bar_chart(subjects_dict: Dict[str, int]) -> go.Figure:
    """Creates a modern horizontal or vertical styled bar chart for subjects."""
    subjects = list(subjects_dict.keys())
    scores = list(subjects_dict.values())
    
    # Dynamic color array
    colors = ['#2a9d8f' if s >= 80 else '#00b4d8' if s >= 70 else '#f4a261' for s in scores]

    fig = go.Figure(data=[
        go.Bar(
            x=subjects,
            y=scores,
            marker=dict(
                color=colors,
                line=dict(color='#1a1a2e', width=1)
            ),
            text=[f"{s}%" for s in scores],
            textposition='outside',
            textfont=dict(size=12, color='#1a1a2e', family='Plus Jakarta Sans'),
            hoverinfo='x+y'
        )
    ])

    fig.update_layout(
        yaxis=dict(
            range=[0, 100],
            title="Score Percentage (%)",
            gridcolor='rgba(0,0,0,0.06)'
        ),
        xaxis=dict(
            tickfont=dict(size=11, family='Plus Jakarta Sans')
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def build_weekly_activity_chart(weekly_dict: Dict[str, float]) -> go.Figure:
    """Creates a weekly study activity chart with target threshold."""
    days = list(weekly_dict.keys())
    hours = list(weekly_dict.values())

    fig = go.Figure()

    # Bar series
    fig.add_trace(go.Bar(
        x=days,
        y=hours,
        name='Study Hours',
        marker=dict(
            color=['#0077b6', '#00b4d8', '#2a9d8f', '#f4a261', '#0077b6'],
            line=dict(color='#1a1a2e', width=1)
        ),
        text=[f"{h} hrs" for h in hours],
        textposition='outside',
        textfont=dict(size=11, color='#1a1a2e', family='Plus Jakarta Sans')
    ))

    # Daily target line (3.0 hrs)
    fig.add_shape(
        type='line',
        x0=-0.5,
        x1=len(days) - 0.5,
        y0=3.0,
        y1=3.0,
        line=dict(color='#e76f51', width=2, dash='dash')
    )

    fig.add_annotation(
        x=days[0],
        y=3.3,
        text="Target: 3.0 hrs",
        showarrow=False,
        font=dict(size=10, color='#e76f51', family='Plus Jakarta Sans')
    )

    fig.update_layout(
        yaxis=dict(
            range=[0, 5],
            title="Hours Studied",
            gridcolor='rgba(0,0,0,0.06)'
        ),
        xaxis=dict(
            tickfont=dict(size=11, family='Plus Jakarta Sans')
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    return fig

def build_performance_timeline_chart(timeline: List[Dict[str, Any]]) -> go.Figure:
    """Creates a smooth area timeline chart showing score progression."""
    weeks = [item["week"] for item in timeline]
    scores = [item["score"] for item in timeline]
    hours = [item["hours"] for item in timeline]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=weeks,
        y=scores,
        mode='lines+markers',
        name='Overall Score (%)',
        line=dict(color='#0077b6', width=3, shape='spline'),
        marker=dict(size=8, color='#1a1a2e', line=dict(width=2, color='#00b4d8')),
        fill='tozeroy',
        fillcolor='rgba(0, 180, 216, 0.12)'
    ))

    fig.update_layout(
        yaxis=dict(
            range=[50, 95],
            title="Performance Score (%)",
            gridcolor='rgba(0,0,0,0.06)'
        ),
        margin=dict(l=20, r=20, t=15, b=20),
        height=280,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    return fig

def build_wellness_radar(wellness_dict: Dict[str, int]) -> go.Figure:
    """Creates academic wellness dimensions radar chart."""
    dimensions = list(wellness_dict.keys())
    scores = list(wellness_dict.values())
    
    dimensions_closed = dimensions + [dimensions[0]]
    scores_closed = scores + [scores[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores_closed,
        theta=dimensions_closed,
        fill='toself',
        fillcolor='rgba(42, 157, 143, 0.22)',
        line=dict(color='#2a9d8f', width=2),
        name='Dimension Score'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(0,0,0,0.08)'),
            angularaxis=dict(tickfont=dict(size=11, family='Plus Jakarta Sans'))
        ),
        margin=dict(l=30, r=30, t=20, b=20),
        height=280,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    return fig


def build_feature_importance_chart(feature_importances: Dict[str, float]) -> go.Figure:
    """Builds a bar chart visualizing Decision Tree feature importances."""
    name_map = {
        "attendance": "Attendance",
        "study_hours": "Study Hours",
        "assignment_marks": "Assignment Marks",
        "internal_marks": "Internal Marks",
        "previous_marks": "Previous Marks"
    }

    # Sort descending
    items = sorted(feature_importances.items(), key=lambda x: x[1], reverse=True)
    labels = [name_map.get(k, k.replace("_", " ").title()) for k, _ in items]
    values = [round(v * 100.0, 1) for _, v in items]

    # Palette
    colors = ["#0077b6", "#00b4d8", "#2a9d8f", "#f4a261", "#e76f51"]

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation='h',
        text=[f"{v:.1f}%" for v in values],
        textposition='outside',
        marker=dict(
            color=colors[:len(labels)],
            line=dict(color='#1a1a2e', width=1)
        )
    ))

    fig.update_layout(
        title=dict(
            text="Factors Influencing Student Performance",
            font=dict(size=14, family='Plus Jakarta Sans', color='#1a1a2e')
        ),
        xaxis=dict(
            title="Importance Percentage (%)",
            range=[0, max(values + [50]) * 1.2],
            gridcolor='rgba(0,0,0,0.06)'
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=12, family='Plus Jakarta Sans', color='#1e293b')
        ),
        margin=dict(l=20, r=40, t=40, b=30),
        height=260,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    return fig


def build_confusion_matrix_heatmap(
    cm_matrix: List[List[int]],
    class_labels: List[str]
) -> go.Figure:
    """Builds a styled Plotly heatmap for model confusion matrix evaluation."""
    z = cm_matrix
    x = class_labels
    y = class_labels

    # Annotations formatted
    annotations = []
    for i, row in enumerate(z):
        for j, val in enumerate(row):
            annotations.append(
                dict(
                    x=x[j],
                    y=y[i],
                    text=str(val),
                    font=dict(color="white" if val > 2 else "#1a1a2e", size=14, family="Plus Jakarta Sans"),
                    showarrow=False
                )
            )

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        colorscale=[
            [0.0, "rgba(240, 244, 248, 0.8)"],
            [0.2, "#90e0ef"],
            [0.6, "#0077b6"],
            [1.0, "#03045e"]
        ],
        showscale=True,
        colorbar=dict(title="Count", len=0.8)
    ))

    fig.update_layout(
        title=dict(
            text="Performance Prediction Confusion Matrix",
            font=dict(size=14, family='Plus Jakarta Sans', color='#1a1a2e')
        ),
        xaxis=dict(
            title="Predicted Class",
            tickfont=dict(size=11, family='Plus Jakarta Sans')
        ),
        yaxis=dict(
            title="Actual Ground Truth",
            tickfont=dict(size=11, family='Plus Jakarta Sans'),
            autorange="reversed"
        ),
        annotations=annotations,
        margin=dict(l=40, r=20, t=40, b=40),
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

