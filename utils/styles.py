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
    --secondary-teal: #00b4d8;
    --accent-amber: #f4a261;
    --accent-coral: #e76f51;
    --accent-emerald: #2a9d8f;
    --surface-glass: rgba(255, 255, 255, 0.78);
    --surface-glass-border: rgba(0, 180, 216, 0.22);
    --shadow-soft: 0 10px 30px -5px rgba(26, 26, 46, 0.08);
}

/* Global Font & Canvas Atmosphere */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1a1a2e;
    background: radial-gradient(circle at 10% 20%, rgba(240, 244, 255, 0.8) 0%, rgba(248, 250, 255, 1) 90%);
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #f1f4fa;
    border-radius: 8px;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #1a1a2e, #00b4d8);
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
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(0, 180, 216, 0.18);
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 8px 24px -4px rgba(26, 26, 46, 0.06), 0 0 0 1px rgba(255, 255, 255, 0.8) inset;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    margin-bottom: 18px;
}

.smart-glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 32px -4px rgba(0, 180, 216, 0.12), 0 0 0 1px rgba(0, 180, 216, 0.3) inset;
    border-color: rgba(0, 180, 216, 0.35);
}

/* Academic Health Hero Container */
.health-meter-box {
    background: linear-gradient(135deg, rgba(26, 26, 46, 0.96) 0%, rgba(21, 34, 56, 0.94) 70%, rgba(0, 119, 182, 0.88) 100%);
    color: #ffffff;
    border-radius: 20px;
    padding: 28px 32px;
    box-shadow: 0 16px 36px -8px rgba(26, 26, 46, 0.25);
    position: relative;
    overflow: hidden;
    margin-bottom: 24px;
}

.health-meter-box::after {
    content: "";
    position: absolute;
    top: -50%;
    right: -20%;
    width: 320px;
    height: 320px;
    background: radial-gradient(circle, rgba(0, 180, 216, 0.25) 0%, transparent 70%);
    pointer-events: none;
}

/* AI Spotlight Box */
.ai-spotlight-box {
    background: linear-gradient(135deg, rgba(0, 180, 216, 0.08) 0%, rgba(244, 162, 97, 0.08) 100%);
    border: 1.5px solid rgba(0, 180, 216, 0.35);
    border-radius: 16px;
    padding: 20px 24px;
    position: relative;
    margin-bottom: 20px;
}

/* Badges & Chips */
.smart-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.01em;
}

.chip-indigo {
    background: rgba(26, 26, 46, 0.08);
    color: #1a1a2e;
    border: 1px solid rgba(26, 26, 46, 0.15);
}

.chip-teal {
    background: rgba(0, 180, 216, 0.12);
    color: #0077b6;
    border: 1px solid rgba(0, 180, 216, 0.28);
}

.chip-amber {
    background: rgba(244, 162, 97, 0.15);
    color: #b05710;
    border: 1px solid rgba(244, 162, 97, 0.35);
}

.chip-emerald {
    background: rgba(42, 157, 143, 0.14);
    color: #1e6d63;
    border: 1px solid rgba(42, 157, 143, 0.3);
}

.chip-coral {
    background: rgba(230, 57, 70, 0.12);
    color: #c9182b;
    border: 1px solid rgba(230, 57, 70, 0.28);
}

/* Top Navigation Bar */
.top-nav-container {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(0, 180, 216, 0.18);
    padding: 12px 20px;
    border-radius: 16px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px -2px rgba(26, 26, 46, 0.04);
}

/* Timeline Layout */
.timeline-stem {
    border-left: 2px dashed rgba(0, 180, 216, 0.4);
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
    background: #00b4d8;
    border: 3px solid #ffffff;
    box-shadow: 0 0 0 2px #00b4d8;
}

.timeline-dot.completed {
    background: #2a9d8f;
    box-shadow: 0 0 0 2px #2a9d8f;
}

.timeline-dot.in-progress {
    background: #f4a261;
    box-shadow: 0 0 0 2px #f4a261;
}

/* Streamlit Native Component Fine Tuning */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(0, 180, 216, 0.18);
    border-radius: 14px;
    padding: 14px 18px;
    box-shadow: 0 4px 12px rgba(26, 26, 46, 0.03);
}

div[data-testid="stMetricValue"] > div {
    font-weight: 800 !important;
    color: #1a1a2e !important;
}

/* Hide default streamlit menu decoration if present */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Tab button enhancement */
button[data-baseweb="tab"] {
    font-weight: 600 !important;
    border-radius: 8px !important;
}
</style>
"""
