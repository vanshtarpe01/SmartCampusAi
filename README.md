# SmartCampus AI – Intelligent Student Assistant

## Description
SmartCampus AI is an intelligent student learning and decision-support application built using **Python and Streamlit**. It provides academic analytics, time-blocked study scheduling, personalized recommendations, and curriculum guidance for students in Artificial Intelligence and Computer Science courses.

This frontend prototype features an **Academic meets Futuristic** UI design with glass-morphism cards, interactive Plotly visualizations, responsive layouts, and a dedicated AI Study Companion.

---

## Features
- 🏠 **Academic Dashboard**: High-level Academic Health Meter displaying overall index (78%), attendance (82%), study pace (3.2 hrs/day), and risk level (LOW).
- 📊 **Interactive Analytics**: Knowledge Radar and Subject Performance graphs covering Mathematics, Artificial Intelligence, DBMS, and Networking, alongside weekly study hours tracking.
- 🤖 **AI Study Companion**: Natural chat interface featuring structured explanations for algorithms (BFS, DFS, A*, Minimax, Alpha-Beta Pruning, Expert Systems) and quick prompt chips.
- 📚 **Smart Study Planner**: Time-blocked revision timetable generator with spaced repetition, difficulty tailoring, and interactive task status checkboxes.
- 🎯 **Personalized Recommendations**: Priority-filtered intervention cards categorized into High, Medium, and Low priorities with impact and effort metrics.
- 📖 **AI Knowledge Explorer**: Curriculum encyclopedia detailing formal definitions, key concepts, applications, and computational complexity for 12 foundational AI topics.
- ℹ️ **About & Roadmap**: Project specification and architectural comparison detailing the evolution from React to Python/Streamlit.

---

## Technology Stack
- **Programming Language**: Python 3.10+
- **Frontend Framework**: Streamlit (v1.28+)
- **Data Manipulation**: Pandas, NumPy
- **Interactive Visualizations**: Plotly (Radar charts, Bar charts, Area curves)
- **Design System**: Glass-morphism, custom CSS gradients, and responsive card layouts

---

## Project Structure
```text
SmartCampusAI/
│
├── app.py                     # Main application entry point & sidebar navigation
├── data.py                    # Mock student data, knowledge topics, and AI responses
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation & run guide
├── MIGRATION_REPORT.md        # Architecture migration log (React -> Streamlit)
│
├── .streamlit/
│   └── config.toml           # Streamlit server and theme configuration
│
├── pages/
│   ├── dashboard.py          # Dashboard view & Academic Health Meter
│   ├── assistant.py          # AI Study Companion chat interface
│   ├── performance.py        # Granular assessment analytics & wellness radar
│   ├── planner.py            # AI Study Planner & timeline generator
│   ├── recommendations.py    # Priority-filtered recommendation cards
│   ├── knowledge.py          # AI Knowledge Explorer curriculum encyclopedia
│   └── about.py              # Project overview, tech stack & future scope
│
└── utils/
    ├── __init__.py           # Package marker
    ├── styles.py             # Custom CSS styling (Glass-morphism & Gradients)
    ├── ui.py                 # Reusable UI components & Plotly visualizers
    └── helpers.py            # Session state and formatting utilities
```

---

## Installation
Ensure you have Python 3.10 or higher installed, then install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Run Application
Launch the application with a single command:

```bash
streamlit run app.py
```

Open your browser to `http://localhost:3000` or the port displayed in your terminal.

---

## Current Development Phase
**Phase 1: Frontend Prototype**
- High-fidelity interactive UI constructed with native Streamlit components.
- Structured mock data stored in `data.py` with bridge functions ready for ML model integration.
- Zero dependencies on Node.js, React, npm, or external paid APIs.

---

## Future Scope (Phase 2 Roadmap)
1. **Decision Tree ML Classifier**: Train supervised Decision Tree models using Scikit-learn on student academic histories to predict letter grades and early-warning flags.
2. **Rule-Based Expert System**: Implement forward/backward chaining inference engines to automate academic interventions based on attendance and test drops.
3. **Recommendation Engine**: Dynamic prioritization algorithms that adapt study hour schedules according to student performance trends.
4. **Knowledge Base Expansion**: Expand curriculum topics with practice quizzes and automated flashcards.
5. **Study Planner Optimization**: Integrate algorithmic schedule optimization based on student circadian rhythm and topic complexity curves.
