"""SmartCampus AI - AI Assistant Page
Interactive study companion powered by structured mock responses for AI algorithms,
data structures, and curriculum subjects. Designed for Phase 2 ML backend integration.
"""

import streamlit as st
import datetime
from data import get_ai_response, get_student_data
from utils.ui import render_top_brand

def render_assistant():
    """Renders the AI Study Companion chat interface."""
    active_sid = st.session_state.get("selected_student_id") or st.session_state.get("student_id") or "MLU25S211"
    student = get_student_data(active_sid)
    student_name = student.get("full_name") or student.get("name") or st.session_state.get("user_name", "Student")
    first_name = student_name.split()[0] if student_name else "Student"

    st.markdown(
        f"""
<div style="margin-bottom: 20px;">
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
<div>
<h2 class="smart-gradient-text" style="font-size: 1.65rem; margin: 0;">
🤖 AI Study Companion
</h2>
<p style="margin: 3px 0 0 0; color: #5a6275; font-size: 0.95rem;">
Your intelligent personal tutor for Artificial Intelligence, search algorithms, and academic diagnostics.
</p>
</div>
<div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
<span class="smart-chip chip-teal">👤 Student: <strong>{student_name}</strong> ({active_sid})</span>
<span class="smart-chip chip-indigo">⚡ AI Study Companion</span>
</div>
</div>
</div>
""",
        unsafe_allow_html=True
    )

    # Initialize messages in session state if not present or if active student changed
    if "chat_messages" not in st.session_state or not st.session_state.chat_messages:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    f"Hello **{student_name}**! I am your SmartCampus AI Study Companion.\n\n"
                    "Ask me any question about Artificial Intelligence, search algorithms, "
                    r"or exam subjects (e.g. *What is BFS?*, *Explain A*\*). You can also ask *How is my performance?* or *What is my name?*!"
                ),
                "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
                "category": "Welcome"
            }
        ]
        st.session_state["chat_current_student"] = active_sid
    elif st.session_state.get("chat_current_student") != active_sid:
        st.session_state["chat_current_student"] = active_sid
        if len(st.session_state.chat_messages) <= 1:
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": (
                        f"Hello **{student_name}**! I am your SmartCampus AI Study Companion.\n\n"
                        "Ask me any question about Artificial Intelligence, search algorithms, "
                        r"or exam subjects (e.g. *What is BFS?*, *Explain A*\*). You can also ask *How is my performance?* or *What is my name?*!"
                    ),
                    "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
                    "category": "Welcome"
                }
            ]

    # Quick Suggestion Chips
    st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #475569; margin-bottom: 8px;'>💡 Quick Topics to Explore:</div>", unsafe_allow_html=True)
    
    chip_cols = st.columns(6)
    chips = [
        "What is BFS?",
        "Explain DFS",
        "How does A* work?",
        "How is my performance?",
        "What is my name?",
        "What is my risk level?"
    ]
    
    selected_quick_prompt = None
    for idx, (col, chip_text) in enumerate(zip(chip_cols, chips)):
        with col:
            if st.button(chip_text, key=f"quick_chip_{idx}", use_container_width=True):
                selected_quick_prompt = chip_text

    st.markdown("<hr style='border: none; border-top: 1px solid rgba(0, 180, 216, 0.15); margin: 16px 0;'>", unsafe_allow_html=True)

    # Controls row: Clear chat & Export
    col_ctrl1, col_ctrl2, col_info = st.columns([1, 1, 3])
    with col_ctrl1:
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": f"Conversation cleared. How can I assist you with your studies, **{first_name}**?",
                    "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
                    "category": "System"
                }
            ]
            st.rerun()

    with col_ctrl2:
        if "show_export_log" not in st.session_state:
            st.session_state.show_export_log = False
        if st.button("📥 Export Chat Log", use_container_width=True):
            st.session_state.show_export_log = not st.session_state.show_export_log

    with col_info:
        st.caption("ℹ️ SmartCampus AI Engine: Knowledge base of 12 AI topics, academic diagnostics, and real-time student context evaluation.")

    if st.session_state.get("show_export_log", False):
        export_text = "\n\n".join([
            f"[{msg.get('timestamp', '')}] {msg.get('sender_name', msg['role']).upper()}: {msg['content']}"
            for msg in st.session_state.chat_messages
        ])
        with st.expander("📄 Exported Chat Transcript", expanded=True):
            st.text_area(
                "Copy conversation transcript:",
                value=export_text,
                height=160,
                help="Select all and copy (Ctrl+C / Cmd+C) to save your session."
            )
            st.caption(f"📝 {len(st.session_state.chat_messages)} message(s) formatted • Export date: {datetime.date.today()}")

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    # Chat Messages Display Area
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                sender_label = msg.get("sender_name") or student_name
                with st.chat_message(sender_label, avatar="👤"):
                    st.markdown(f"<div style='font-size: 0.82rem; font-weight: 700; color: #0077b6; margin-bottom: 2px;'>{sender_label}</div>", unsafe_allow_html=True)
                    st.write(msg["content"])
                    st.caption(f"Sent at {msg.get('timestamp', '')}")
            else:
                with st.chat_message("SmartCampus AI", avatar="🤖"):
                    st.markdown(msg["content"])
                    meta = []
                    if "category" in msg:
                        meta.append(f"Category: {msg['category']}")
                    if "difficulty" in msg:
                        meta.append(f"Level: {msg['difficulty']}")
                    meta.append(msg.get("timestamp", ""))
                    st.caption(" • ".join(meta))

    # User Input Handling
    user_query = st.chat_input("Ask about AI algorithms, study strategies, or subjects...")

    # Process either chat_input or quick chip click
    query_to_process = selected_quick_prompt or user_query

    if query_to_process:
        now_str = datetime.datetime.now().strftime("%I:%M %p")
        # Append User Message with sender_name
        st.session_state.chat_messages.append({
            "role": "user",
            "sender_name": student_name,
            "content": query_to_process,
            "timestamp": now_str
        })

        # Fetch AI Response using local Assistant engine and student context
        ai_resp = get_ai_response(query_to_process, student_id=active_sid)
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": ai_resp["response"],
            "timestamp": now_str,
            "category": ai_resp.get("category", "General"),
            "difficulty": ai_resp.get("difficulty", "Standard")
        })
        st.rerun()

if __name__ == "__main__":
    from utils.styles import CUSTOM_CSS
    st.set_page_config(page_title="AI Assistant - SmartCampus AI", page_icon="🤖", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    render_top_brand()
    render_assistant()
