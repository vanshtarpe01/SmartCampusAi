"""SmartCampus AI - Unique Design System & Custom CSS Styling
Implements Academic meets Futuristic aesthetic:
- Deep Indigo (#1a1a2e)
- Soft Teal (#00b4d8)
- Warm Amber (#f4a261)
- Subtle glass-morphism cards with soft border glows
- Gradient typography and interactive hover enhancements
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --primary-indigo: #1a1a2e;
    --secondary-teal: #0077b6;
    --accent-amber: #b45309;
    --accent-coral: #b91c1c;
    --accent-emerald: #065f46;
    --surface-glass: rgba(255, 255, 255, 0.92);
    --surface-glass-border: rgba(0, 119, 182, 0.20);
    --shadow-soft: 0 10px 25px -5px rgba(15, 23, 42, 0.06);
}

/* Global Font & Canvas Atmosphere */
html, body, .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #0f172a !important;
    background: radial-gradient(circle at 10% 20%, rgba(240, 246, 255, 0.85) 0%, rgba(248, 250, 255, 1) 90%) !important;
}

/* Base Headings & Text Color */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
    color: #0f172a !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp p, .stApp span, .stApp label, .stApp li {
    color: #334155;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 8px;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #1a1a2e, #0077b6);
    border-radius: 8px;
}

/* Gradient Headings */
.smart-gradient-text {
    background: linear-gradient(120deg, #1a1a2e 15%, #0077b6 60%, #00b4d8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.sub-gradient-text {
    background: linear-gradient(120deg, #0077b6, #00b4d8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}

/* Glass-morphism Cards */
.smart-glass-card {
    background: #ffffff !important;
    border: 1px solid rgba(0, 119, 182, 0.18) !important;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 4px 18px -2px rgba(15, 23, 42, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    margin-bottom: 18px;
}

.smart-glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px -4px rgba(0, 119, 182, 0.12);
    border-color: rgba(0, 119, 182, 0.35) !important;
}

/* Academic Health Hero Container */
.health-meter-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 70%, #0369a1 100%) !important;
    color: #ffffff !important;
    border-radius: 20px;
    padding: 28px 32px;
    box-shadow: 0 16px 36px -8px rgba(15, 23, 42, 0.25);
    position: relative;
    overflow: hidden;
    margin-bottom: 24px;
}

.health-meter-box * {
    color: #ffffff !important;
}

.health-meter-box::after {
    content: "";
    position: absolute;
    top: -50%;
    right: -20%;
    width: 320px;
    height: 320px;
    background: radial-gradient(circle, rgba(0, 180, 216, 0.22) 0%, transparent 70%);
    pointer-events: none;
}

/* AI Spotlight Box */
.ai-spotlight-box {
    background: #ffffff !important;
    border: 1.5px solid rgba(0, 119, 182, 0.35) !important;
    border-radius: 16px;
    padding: 20px 24px;
    position: relative;
    margin-bottom: 20px;
    box-shadow: 0 4px 14px rgba(0, 119, 182, 0.06);
}

/* Badges & Chips - High Contrast & Legible */
.smart-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.01em;
    white-space: nowrap;
}

.chip-indigo {
    background: #ede9fe !important;
    color: #3730a3 !important;
    border: 1px solid #c7d2fe !important;
}

.chip-teal {
    background: #e0f2fe !important;
    color: #0369a1 !important;
    border: 1px solid #7dd3fc !important;
}

.chip-amber {
    background: #fef3c7 !important;
    color: #92400e !important;
    border: 1px solid #fde68a !important;
}

.chip-emerald {
    background: #d1fae5 !important;
    color: #065f46 !important;
    border: 1px solid #a7f3d0 !important;
}

.chip-coral {
    background: #fee2e2 !important;
    color: #991b1b !important;
    border: 1px solid #fecaca !important;
}

/* Top Navigation Bar */
.top-nav-container {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(0, 119, 182, 0.18);
    padding: 12px 20px;
    border-radius: 16px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04);
}

/* Timeline Layout */
.timeline-stem {
    border-left: 2px dashed rgba(0, 119, 182, 0.4);
    margin-left: 14px;
    padding-left: 20px;
    padding-bottom: 18px;
    position: relative;
}

.timeline-dot {
    position: absolute;
    left: -21px;
    top: 2px;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #0077b6;
    border: 3px solid #ffffff;
    box-shadow: 0 0 0 2px #0077b6;
}

.timeline-dot.completed {
    background: #065f46;
    box-shadow: 0 0 0 2px #065f46;
}

.timeline-dot.in-progress {
    background: #b45309;
    box-shadow: 0 0 0 2px #b45309;
}

/* Streamlit Buttons: High Contrast & Crisp */
div.stButton > button,
button[kind="secondary"],
button[data-testid="stBaseButton-secondary"] {
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1.5px solid #cbd5e1 !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04) !important;
    transition: all 0.2s ease !important;
}

div.stButton > button:hover,
button[kind="secondary"]:hover,
button[data-testid="stBaseButton-secondary"]:hover {
    background: #f1f5f9 !important;
    color: #0077b6 !important;
    border-color: #0077b6 !important;
}

div.stButton > button * {
    color: #0f172a !important;
}

div.stButton > button:hover * {
    color: #0077b6 !important;
}

div.stButton > button[kind="primary"],
button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #0077b6, #0096c7) !important;
    color: #ffffff !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 14px rgba(0, 119, 182, 0.25) !important;
}

div.stButton > button[kind="primary"]:hover,
button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover {
    background: linear-gradient(135deg, #023e8a, #0077b6) !important;
    color: #ffffff !important;
    box-shadow: 0 6px 18px rgba(0, 119, 182, 0.35) !important;
}

div.stButton > button[kind="primary"] *,
button[kind="primary"] * {
    color: #ffffff !important;
}

/* Metric Cards */
div[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid rgba(0, 119, 182, 0.18) !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03) !important;
}

div[data-testid="stMetricLabel"] label,
div[data-testid="stMetricLabel"] div {
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}

div[data-testid="stMetricValue"] > div {
    font-weight: 800 !important;
    color: #0f172a !important;
}

/* Chat Messages */
div[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
    padding: 16px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03) !important;
}

div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] span,
div[data-testid="stChatMessage"] div {
    color: #1e293b !important;
}

div[data-testid="stChatInput"] textarea {
    color: #0f172a !important;
    background-color: #ffffff !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}

section[data-testid="stSidebar"] * {
    color: #0f172a;
}

/* Hide default streamlit menu decoration if present */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Tab button enhancement */
button[data-baseweb="tab"] {
    font-weight: 600 !important;
    border-radius: 8px !important;
    color: #475569 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #0077b6 !important;
    font-weight: 700 !important;
}

/* Form inputs and select dropdowns */
div[data-baseweb="select"] {
    background-color: #ffffff !important;
}

div[data-baseweb="select"] * {
    color: #0f172a !important;
}
</style>
"""
