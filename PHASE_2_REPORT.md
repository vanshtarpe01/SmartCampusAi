# SmartCampus AI — Phase 2 Technical Report
## Python AI Backend, Rule Engine & Local Dataset Architecture

---

### 1. Overview
**SmartCampus AI Phase 2** replaced any mock/transient layers with a dedicated, explainable Python AI Backend. It introduced an expert Rule Engine, dynamic Academic Knowledge Base, local student dataset (`data/students.csv`), personalized Study Plan Generator, and automated multi-criteria Recommendation Engine.

---

### 2. Rule-Based AI Engine (`ai/rule_engine.py`)
The Rule-Based Engine evaluates deterministic educational heuristics modeled on university academic ordinances:
1. **Attendance Compliance Rule**:
   - $\ge 85\%$: Commended attendance.
   - $75\% - 84.9\%$: Eligible for exams.
   - $< 75\%$: Attendance shortage warning; flagged for academic risk.
2. **Study Habit Evaluation Rule**:
   - $\ge 4.0\text{ hrs/day}$: Optimal consistent revision.
   - $2.5 - 3.9\text{ hrs/day}$: Adequate.
   - $< 2.5\text{ hrs/day}$: Deficit flagged; daily revision plan scheduled.
3. **Continuous Assessment Rule**:
   - Checks assignment submissions ($\ge 8/10$ optimal; $< 6/10$ warning).
4. **Examination Readiness Rule**:
   - Internal test score ($\ge 40/50$ mastery; $< 30/50$ revision intervention required).
5. **Multi-Factor Weighted Performance Formula**:
   $$\text{Score} = (0.20 \times \text{Attendance}) + (0.15 \times \text{Study}) + (0.15 \times \text{Assignments}) + (0.25 \times \text{Internal}) + (0.25 \times \text{Previous})$$
   - $\ge 85.0 \implies \text{Excellent}$
   - $70.0 - 84.9 \implies \text{Good}$
   - $55.0 - 69.9 \implies \text{Average}$
   - $< 55.0 \implies \text{Needs Improvement}$

---

### 3. Knowledge Base (`ai/knowledge_base.py`)
Provides an offline dictionary of 25+ academic topics across core computer science disciplines:
- Mathematics (Linear Algebra, Calculus, Discrete Math, Probability)
- Artificial Intelligence (Search, ML Basics, Neural Networks, Decision Trees, NLP)
- Database Management Systems (SQL, Normalization, Transactions, Indexing)
- Computer Networks (OSI Model, TCP/IP, Routing, Protocols, Network Security)

---

### 4. Recommendation Engine (`ai/recommendation_engine.py`)
Scans student performance profiles and generates prioritized recommendations:
- High Risk ($< 55\%$ or attendance $< 75\%$): Urgent faculty consultation and remedial study schedules.
- Medium Risk ($55\% - 70\%$): Targeted subject practice and time management.
- Low Risk ($\ge 70\%$): Competitive coding, hackathons, and research projects.

---

### 5. Study Planner (`ai/study_planner.py`)
Generates structured daily 7-day revision timetables based on student available hours and weak subjects.

---

### 6. Technology Compliance
- 100% Python-based.
- No Node.js, React, or JavaScript.
- No cloud AI APIs.
- Local CSV file persistence.
