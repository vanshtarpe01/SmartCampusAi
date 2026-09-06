"""SmartCampus AI - AI Knowledge Explorer Page
Structured academic encyclopedia covering Core AI algorithms, intelligent agents,
search paradigms, game playing algorithms, and expert systems with formal definitions,
key concepts, real-world applications, and asymptotic complexity formulas.
"""

import streamlit as st
from data import get_knowledge_topic, get_all_knowledge_topics
from utils.ui import render_top_brand

def render_knowledge():
    """Renders the AI Knowledge Explorer curriculum reference."""
    st.markdown(
        """
        <div style="margin-bottom: 22px;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h2 class="smart-gradient-text" style="font-size: 1.65rem; margin: 0;">
                        📖 AI Knowledge Explorer
                    </h2>
                    <p style="margin: 3px 0 0 0; color: #5a6275; font-size: 0.95rem;">
                        Rigorous academic knowledge repository covering fundamental AI algorithms and theories.
                    </p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <span class="smart-chip chip-teal">13 Core Topics</span>
                    <span class="smart-chip chip-indigo">Curriculum Aligned</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    all_topics = get_all_knowledge_topics()

    # Topic Selection Row
    col_select, col_cat = st.columns([1.6, 1.4])
    with col_select:
        selected_topic_name = st.selectbox(
            "Select an AI Curriculum Topic to Explore:",
            options=all_topics,
            index=0
        )

    topic_info = get_knowledge_topic(selected_topic_name)

    with col_cat:
        if topic_info:
            st.markdown(
                f"""
                <div style="padding-top: 24px; display: flex; gap: 8px; align-items: center;">
                    <span class="smart-chip chip-teal">Category: {topic_info.get('category', 'Core')}</span>
                    <span class="smart-chip chip-amber">Verified Syllabus</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    # Detailed Structured Topic Card
    if topic_info:
        # Header Box with Icon & Title
        st.markdown(
            f"""
            <div class="smart-glass-card" style="border-top: 4px solid #00b4d8; padding: 24px; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 14px;">
                    <div style="width: 50px; height: 50px; border-radius: 14px; background: linear-gradient(135deg, #1a1a2e, #00b4d8); display: flex; align-items: center; justify-content: center; font-size: 26px;">
                        {topic_info.get('icon', '💡')}
                    </div>
                    <div>
                        <h3 style="margin: 0; font-size: 1.45rem; font-weight: 800; color: #1a1a2e;">
                            {topic_info['title']}
                        </h3>
                        <div style="font-size: 0.84rem; color: #64748b; font-weight: 600;">
                            Field: {topic_info.get('category', 'Artificial Intelligence')}
                        </div>
                    </div>
                </div>

                <!-- Definition -->
                <div style="background: rgba(0, 180, 216, 0.08); border-left: 3px solid #0077b6; padding: 12px 16px; border-radius: 8px; margin-bottom: 18px;">
                    <div style="font-size: 0.78rem; font-weight: 800; text-transform: uppercase; color: #0077b6; margin-bottom: 4px;">
                        📝 Formal Definition
                    </div>
                    <div style="font-size: 1rem; color: #1e293b; font-weight: 600; line-height: 1.5;">
                        "{topic_info['definition']}"
                    </div>
                </div>

                <!-- Complexity Section -->
                <div style="background: rgba(26, 26, 46, 0.05); border: 1px dashed rgba(26, 26, 46, 0.2); padding: 10px 14px; border-radius: 8px; margin-bottom: 18px;">
                    <span style="font-weight: 800; color: #1a1a2e; font-size: 0.85rem;">📊 Computational Complexity: </span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.92rem; color: #0077b6; font-weight: 600;">
                        {topic_info['complexity']}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Columns for Key Concepts & Applications
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown(
                """
                <div class="smart-glass-card" style="padding: 20px; height: 100%;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                        <span style="font-size: 1.25rem;">🔑</span>
                        <h4 style="margin: 0; color: #1a1a2e; font-size: 1.05rem; font-weight: 700;">
                            Key Concepts & Mechanisms
                        </h4>
                    </div>
                    <ul style="margin: 0; padding-left: 20px; line-height: 1.7; color: #334155; font-size: 0.94rem;">
                """,
                unsafe_allow_html=True
            )
            for kc in topic_info["key_concepts"]:
                st.markdown(f"<li>{kc}</li>", unsafe_allow_html=True)
            st.markdown("</ul></div>", unsafe_allow_html=True)

        with col_right:
            st.markdown(
                """
                <div class="smart-glass-card" style="padding: 20px; height: 100%;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                        <span style="font-size: 1.25rem;">🎯</span>
                        <h4 style="margin: 0; color: #1a1a2e; font-size: 1.05rem; font-weight: 700;">
                            Real-World Applications
                        </h4>
                    </div>
                    <ul style="margin: 0; padding-left: 20px; line-height: 1.7; color: #334155; font-size: 0.94rem;">
                """,
                unsafe_allow_html=True
            )
            for app in topic_info["applications"]:
                st.markdown(f"<li>{app}</li>", unsafe_allow_html=True)
            st.markdown("</ul></div>", unsafe_allow_html=True)

        # Illustrative Example Box
        st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="smart-glass-card" style="border-left: 4px solid #f4a261; padding: 18px 22px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="font-size: 1.25rem;">💡</span>
                    <h4 style="margin: 0; color: #1a1a2e; font-size: 1.05rem; font-weight: 700;">
                        Illustrative Academic Example
                    </h4>
                </div>
                <p style="margin: 0; font-size: 0.94rem; color: #475569; line-height: 1.6;">
                    {topic_info['example']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Quick Action Buttons
        st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
        qa1, qa2 = st.columns(2)
        with qa1:
            if st.button(f"💬 Ask AI Study Companion about {topic_info['title']}", use_container_width=True):
                st.session_state.current_page = "AI Assistant"
                st.rerun()
        with qa2:
            if st.button(f"📅 Add {topic_info['title']} to Study Planner", use_container_width=True):
                st.session_state.current_page = "Study Planner"
                st.rerun()

if __name__ == "__main__":
    from utils.styles import CUSTOM_CSS
    st.set_page_config(page_title="AI Knowledge - SmartCampus AI", page_icon="📖", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    render_top_brand()
    render_knowledge()
