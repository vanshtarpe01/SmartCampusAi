"""SmartCampus AI - About Page
Presents project mission, architecture comparison, technology stack,
current prototype status, and comprehensive Phase 2 development roadmap.
"""

import streamlit as st
from utils.ui import render_top_brand

def render_about():
    """Renders the About SmartCampus AI project details and vision."""
    st.markdown(
        """
<div style="margin-bottom: 22px;">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
<div>
<h2 class="smart-gradient-text" style="font-size: 1.65rem; margin: 0;">
ℹ️ About SmartCampus AI
</h2>
<p style="margin: 3px 0 0 0; color: #5a6275; font-size: 0.95rem;">
Project overview, technology architecture, and forward roadmap.
</p>
</div>
<div style="display: flex; gap: 8px;">
<span class="smart-chip chip-teal">Python + Streamlit</span>
<span class="smart-chip chip-indigo">Academic Edition</span>
</div>
</div>
</div>
""",
        unsafe_allow_html=True
    )

    # Hero Project Summary Card
    st.markdown(
        """
<div class="health-meter-box" style="margin-bottom: 24px;">
<div style="font-size: 0.82rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: #00b4d8; margin-bottom: 4px;">
PROJECT OVERVIEW
</div>
<h3 style="margin: 0 0 8px 0; font-size: 1.6rem; font-weight: 800; color: #ffffff;">
SmartCampus AI – Intelligent Student Assistant
</h3>
<p style="margin: 0; font-size: 1.05rem; color: #e2e8f0; line-height: 1.6; max-width: 800px;">
<em>"An intelligent student learning and decision-support application based on
Artificial Intelligence and data-driven approaches."</em>
</p>
<div style="margin-top: 16px; display: flex; gap: 10px; flex-wrap: wrap;">
<span style="background: rgba(42, 157, 143, 0.3); padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; color: #ffffff;">
Status: Phase 3 Machine Learning AI Active
</span>
<span style="background: rgba(0, 180, 216, 0.25); padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
Target: College Mini-Project Viva & Academic Evaluation
</span>
</div>
<div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
<div style="font-size: 0.82rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: #a7f3d0; margin-bottom: 12px;">
DEVELOPER PROFILE
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px;">
<div><strong style="color: #ffffff;">Name:</strong> <span style="color: #e2e8f0;">Vansh Tarpe</span></div>
<div><strong style="color: #ffffff;">Roll:</strong> <span style="color: #e2e8f0;">MLU25S211</span></div>
<div><strong style="color: #ffffff;">Section:</strong> <span style="color: #e2e8f0;">3rd year A</span></div>
<div><strong style="color: #ffffff;">Branch:</strong> <span style="color: #e2e8f0;">Computer Science and Engineering (Artificial Intelligence and Machine Learning)</span></div>
</div>
</div>
</div>
""",
        unsafe_allow_html=True
    )

    # Technology Stack Row
    st.markdown("### 🛠️ Technology Stack")
    t1, t2, t3, t4 = st.columns(4)

    with t1:
        st.markdown(
            """
<div class="smart-glass-card" style="text-align: center; padding: 18px 12px;">
<div style="font-size: 2rem; margin-bottom: 6px;">🐍</div>
<div style="font-weight: 700; color: #1a1a2e; font-size: 1rem;">Python 3.10+</div>
<div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">Core Runtime Engine</div>
</div>
""",
            unsafe_allow_html=True
        )

    with t2:
        st.markdown(
            """
<div class="smart-glass-card" style="text-align: center; padding: 18px 12px;">
<div style="font-size: 2rem; margin-bottom: 6px;">👑</div>
<div style="font-weight: 700; color: #0077b6; font-size: 1rem;">Streamlit</div>
<div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">Modern Reactive UI</div>
</div>
""",
            unsafe_allow_html=True
        )

    with t3:
        st.markdown(
            """
<div class="smart-glass-card" style="text-align: center; padding: 18px 12px;">
<div style="font-size: 2rem; margin-bottom: 6px;">📊</div>
<div style="font-weight: 700; color: #2a9d8f; font-size: 1rem;">Plotly & Pandas</div>
<div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">Data & Visualizations</div>
</div>
""",
            unsafe_allow_html=True
        )

    with t4:
        st.markdown(
            """
<div class="smart-glass-card" style="text-align: center; padding: 18px 12px;">
<div style="font-size: 2rem; margin-bottom: 6px;">🤖</div>
<div style="font-weight: 700; color: #f4a261; font-size: 1rem;">Scikit-learn</div>
<div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">Future AI / Decision Tree</div>
</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # Architectural Transformation (React vs Streamlit)
    st.markdown("### 🔄 Architecture Migration: React → Streamlit")
    col_arch1, col_arch2 = st.columns(2)

    with col_arch1:
        st.markdown(
            """
<div class="smart-glass-card" style="border-left: 4px solid #e63946; padding: 20px;">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
<span style="font-size: 1.2rem;">❌</span>
<h4 style="margin: 0; color: #e63946; font-size: 1.05rem; font-weight: 700;">
Deprecated Architecture (React/TSX)
</h4>
</div>
<p style="font-size: 0.88rem; color: #64748b; margin-bottom: 10px;">
Originally created with client-side Node.js, Vite, and TSX components.
</p>
<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #475569; background: rgba(0,0,0,0.04); padding: 10px; border-radius: 8px;">
React.js<br>
&nbsp;&nbsp;↓<br>
TypeScript (.tsx)<br>
&nbsp;&nbsp;↓<br>
Vite Bundler & NPM<br>
&nbsp;&nbsp;↓<br>
Heavy Multi-toolchain Build
</div>
</div>
""",
            unsafe_allow_html=True
        )

    with col_arch2:
        st.markdown(
            """
<div class="smart-glass-card" style="border-left: 4px solid #2a9d8f; padding: 20px;">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
<span style="font-size: 1.2rem;">✅</span>
<h4 style="margin: 0; color: #2a9d8f; font-size: 1.05rem; font-weight: 700;">
Required Architecture (Python + Streamlit)
</h4>
</div>
<p style="font-size: 0.88rem; color: #64748b; margin-bottom: 10px;">
100% pure Python execution with native data science libraries.
</p>
<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #1e6d63; background: rgba(42, 157, 143, 0.08); padding: 10px; border-radius: 8px;">
Python 3.10+<br>
&nbsp;&nbsp;↓<br>
Streamlit Components<br>
&nbsp;&nbsp;↓<br>
Pandas & Plotly Visuals<br>
&nbsp;&nbsp;↓<br>
Simple Command: streamlit run app.py
</div>
</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # Project Milestones & Evolution
    st.markdown("### 🚀 Project Milestones & Evolution")
    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown(
            """
<div class="smart-glass-card" style="padding: 18px; border-top: 3px solid #00b4d8;">
<div style="font-size: 1.5rem; margin-bottom: 6px;">🖥️</div>
<h4 style="margin: 0 0 6px 0; font-size: 1rem; color: #1a1a2e; font-weight: 700;">
Phase 1: Streamlit UI
</h4>
<p style="margin: 0; font-size: 0.86rem; color: #475569; line-height: 1.5;">
Native Python interface, responsive dashboard cards, knowledge base explorer, study scheduler, and academic wellness radars.
</p>
</div>
""",
            unsafe_allow_html=True
        )

    with f2:
        st.markdown(
            """
<div class="smart-glass-card" style="padding: 18px; border-top: 3px solid #2a9d8f;">
<div style="font-size: 1.5rem; margin-bottom: 6px;">🧠</div>
<h4 style="margin: 0 0 6px 0; font-size: 1rem; color: #1a1a2e; font-weight: 700;">
Phase 2: Rule-Based AI
</h4>
<p style="margin: 0; font-size: 0.86rem; color: #475569; line-height: 1.5;">
Deterministic expert system with forward chaining, weighted evaluation formulas, risk categorization, and 120-student CSV repository.
</p>
</div>
""",
            unsafe_allow_html=True
        )

    with f3:
        st.markdown(
            """
<div class="smart-glass-card" style="padding: 18px; border-top: 3px solid #0077b6;">
<div style="font-size: 1.5rem; margin-bottom: 6px;">🌲</div>
<h4 style="margin: 0 0 6px 0; font-size: 1rem; color: #1a1a2e; font-weight: 700;">
Phase 3: Machine Learning
</h4>
<p style="margin: 0; font-size: 0.86rem; color: #475569; line-height: 1.5;">
Decision Tree Classifier with scikit-learn, joblib model persistence, feature importances, confusion matrix, and explainable AI.
</p>
</div>
""",
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    from utils.styles import CUSTOM_CSS
    st.set_page_config(page_title="About - SmartCampus AI", page_icon="ℹ️", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    render_top_brand()
    render_about()
