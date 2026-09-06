"""SmartCampus AI - Recommendations Engine Module
Generates personalized, data-driven academic recommendations based on
a student's rule evaluations, weak metrics, and curriculum requirements.
Pure Python logic with priority tiers (High, Medium, Low).
"""

from typing import Dict, List, Any


def generate_recommendations(student_data: Dict[str, Any], analysis: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """Produces prioritized recommendations tailored to the student's metrics.

    Args:
        student_data: Raw student record or profile dictionary.
        analysis: Optional precomputed analysis dict from ai.performance.analyze_student.

    Returns:
        List of structured recommendation items.
    """
    attendance = float(student_data.get("attendance", 75.0))
    study_hours = float(student_data.get("study_hours", 2.5))
    assignment_marks = float(student_data.get("assignment_marks", 7.0))
    internal_marks = float(student_data.get("internal_marks", 35.0))
    previous_marks = float(student_data.get("previous_marks", 70.0))

    recommendations: List[Dict[str, Any]] = []
    rec_counter = 1

    # ------------------------------------------------------------
    # 1. ATTENDANCE INTERVENTIONS
    # ------------------------------------------------------------
    if attendance < 65.0:
        recommendations.append({
            "id": f"rec-{rec_counter}",
            "priority": "High Priority",
            "title": "Urgent: Restore Exam Attendance Eligibility",
            "category": "Attendance & Compliance",
            "description": f"Your current attendance is {attendance:.1f}%, which is critically below the 75% threshold. You face immediate risk of exam debarment.",
            "reason": "Attendance falls below mandatory institutional minimum.",
            "action": "Attend all upcoming lectures, tutorials, and practical sessions without missing a single class for the next 4 weeks.",
            "impact": "Critical",
            "effort": "Medium",
            "target": "Surpass 75% cutoff",
            "color": "#e63946",
            "icon": "🚨"
        })
        rec_counter += 1
    elif attendance < 75.0:
        recommendations.append({
            "id": f"rec-{rec_counter}",
            "priority": "High Priority",
            "title": "Elevate Attendance to 75%+ Requirement",
            "category": "Attendance & Compliance",
            "description": f"Current attendance is {attendance:.1f}%. Attending 8 additional consecutive classes will return your record to compliant status.",
            "reason": "Attendance is slightly below 75% regulatory requirement.",
            "action": "Prioritize attending morning lectures and verify biometric check-ins.",
            "impact": "High",
            "effort": "Low",
            "target": "Reach 75%+ baseline",
            "color": "#e63946",
            "icon": "⚠️"
        })
        rec_counter += 1
    else:
        recommendations.append({
            "id": f"rec-{rec_counter}",
            "priority": "Low Priority",
            "title": "Maintain Strong Attendance Record",
            "category": "Attendance & Compliance",
            "description": f"Your attendance ({attendance:.1f}%) meets all university criteria. Sustaining this will ensure internal grading bonus marks.",
            "reason": "Compliant attendance status.",
            "action": "Keep current attendance habits intact.",
            "impact": "Low",
            "effort": "Low",
            "target": "Retain 80%+ threshold",
            "color": "#2a9d8f",
            "icon": "✅"
        })
        rec_counter += 1

    # ------------------------------------------------------------
    # 2. STUDY HABITS & SCHEDULING
    # ------------------------------------------------------------
    if study_hours < 2.0:
        recommendations.append({
            "id": f"rec-{rec_counter}",
            "priority": "High Priority",
            "title": "Boost Daily Study Routine to 3.0+ Hours",
            "category": "Study Habits",
            "description": f"Currently averaging {study_hours:.1f} hrs/day. An engineering curriculum demands at least 3 hours of independent study for deep mastery.",
            "reason": "Study hours are inadequate to cover current semester course units.",
            "action": "Establish two dedicated study blocks: 1 hour in the morning and 2 hours in the evening with 10-minute active breaks.",
            "impact": "High",
            "effort": "Medium",
            "target": "Achieve 3.0+ hrs/day baseline",
            "color": "#e63946",
            "icon": "⏳"
        })
        rec_counter += 1
    elif study_hours < 3.5:
        recommendations.append({
            "id": f"rec-{rec_counter}",
            "priority": "Medium Priority",
            "title": "Optimize Study Consistency & Active Recall",
            "category": "Study Habits",
            "description": f"Your study routine ({study_hours:.1f} hrs/day) is steady. Introducing active recall and self-quizzing will double retention efficiency.",
            "reason": "Opportunities exist to level daily study fluctuations and improve efficiency.",
            "action": "Use the SmartCampus AI Study Planner to lock in 45 minutes of daily weak-topic revision.",
            "impact": "Medium",
            "effort": "Low",
            "target": "Reach 3.5 - 4.0 hrs/day",
            "color": "#f4a261",
            "icon": "⏰"
        })
        rec_counter += 1

    # ------------------------------------------------------------
    # 3. INTERNAL EXAMINATION REINFORCEMENT
    # ------------------------------------------------------------
    if internal_marks < 30.0:
        recommendations.append({
            "id": f"rec-{rec_counter}",
            "priority": "High Priority",
            "title": "Internal Exam Remediation & Question Drills",
            "category": "Exam Preparation",
            "description": f"Your internal score of {internal_marks:.1f}/50 ({internal_marks * 2:.0f}%) is in need of prompt reinforcement prior to semester finals.",
            "reason": "Internal assessment indicates conceptual gaps in core subjects.",
            "action": "Solve the last 3 years of mid-term question papers and consult faculty on tricky topics.",
            "impact": "High",
            "effort": "High",
            "target": "Target 38+/50 on next internal exam",
            "color": "#e63946",
            "icon": "🎯"
        })
        rec_counter += 1
    elif internal_marks < 40.0:
        recommendations.append({
            "id": f"rec-{rec_counter}",
            "priority": "Medium Priority",
            "title": "Solidify Midterm Exam Formats",
            "category": "Exam Preparation",
            "description": f"Your score of {internal_marks:.1f}/50 is good. Practicing timed sectional tests will help convert 70% results into 90%+ scores.",
            "reason": "Foundational understanding is present; exam execution speed needs polishing.",
            "action": "Practice 30-minute timed mock tests on key algorithms.",
            "impact": "Medium",
            "effort": "Medium",
            "target": "Target 44+/50 score bracket",
            "color": "#f4a261",
            "icon": "📝"
        })
        rec_counter += 1

    # ------------------------------------------------------------
    # 4. ASSIGNMENT & PRACTICAL LAB SUBMISSIONS
    # ------------------------------------------------------------
    if assignment_marks < 6.0:
        recommendations.append({
            "id": f"rec-{rec_counter}",
            "priority": "High Priority",
            "title": "Complete Pending Assignments & Lab Work",
            "category": "Continuous Assessment",
            "description": f"Assignment marks are currently {assignment_marks:.1f}/10. Incomplete laboratory files directly reduce your continuous assessment score.",
            "reason": "Low continuous assessment grades pull down the overall semester GPA.",
            "action": "Complete all pending lab code submissions and schedule review with teaching assistants.",
            "impact": "High",
            "effort": "Medium",
            "target": "Score 8.0+ on upcoming assignments",
            "color": "#e63946",
            "icon": "🔬"
        })
        rec_counter += 1
    elif assignment_marks < 8.0:
        recommendations.append({
            "id": f"rec-{rec_counter}",
            "priority": "Medium Priority",
            "title": "Enhance Practical Code & Documentation",
            "category": "Continuous Assessment",
            "description": f"Your assignment mark of {assignment_marks:.1f}/10 is respectable. Adding edge-case analysis and clean documentation will push it to maximum marks.",
            "reason": "Incremental improvements will yield full lab credits.",
            "action": "Document algorithms with Big-O complexity analysis and unit test cases.",
            "impact": "Medium",
            "effort": "Low",
            "target": "Attain 9.0+/10 marks",
            "color": "#f4a261",
            "icon": "💻"
        })
        rec_counter += 1

    # ------------------------------------------------------------
    # 5. CURRICULUM SUBJECT-SPECIFIC DRILLS
    # ------------------------------------------------------------
    # Look at subject details from analysis or default to Networking & DBMS
    lowest_subject = "Networking"
    if analysis and "subjects" in analysis:
        subjects_dict = analysis["subjects"]
        lowest_subject = min(subjects_dict, key=subjects_dict.get)

    if lowest_subject == "Networking":
        recommendations.append({
            "id": f"rec-{rec_counter}",
            "priority": "High Priority" if internal_marks < 33 else "Medium Priority",
            "title": "Focus Drill: Computer Networking Architecture",
            "category": "Curriculum Mastery",
            "description": "Networking concepts show lower performance scores. Spend 30 dedicated minutes daily mastering OSI layer functions and TCP 3-way handshakes.",
            "reason": "Subject diagnostic indicates lower proficiency in networking fundamentals.",
            "action": "Draw and explain the 7 layers of OSI and simulate subnet mask calculations.",
            "impact": "High",
            "effort": "Medium",
            "target": "+12% on Next Exam",
            "color": "#e63946" if internal_marks < 33 else "#f4a261",
            "icon": "🌐"
        })
        rec_counter += 1
    elif lowest_subject == "DBMS":
        recommendations.append({
            "id": f"rec-{rec_counter}",
            "priority": "Medium Priority",
            "title": "Focus Drill: DBMS Relational Decomposition",
            "category": "Curriculum Mastery",
            "description": "Practice SQL queries and functional dependency decomposition into 3NF and BCNF normal forms.",
            "reason": "Database theory requires hands-on decomposition practice.",
            "action": "Solve 5 practice normalization problems on BCNF lossless-join decompositions.",
            "impact": "Medium",
            "effort": "Low",
            "target": "Master BCNF & 3NF proofs",
            "color": "#f4a261",
            "icon": "🗄️"
        })
        rec_counter += 1
    elif lowest_subject == "Artificial Intelligence":
        recommendations.append({
            "id": f"rec-{rec_counter}",
            "priority": "Medium Priority",
            "title": "Focus Drill: AI Search & Heuristic Criteria",
            "category": "Curriculum Mastery",
            "description": "Review A* admissible heuristic conditions (h(n) <= h*(n)) and Minimax Alpha-Beta cutoff mechanics.",
            "reason": "Artificial Intelligence search proofs frequently appear on semester examinations.",
            "action": "Trace Alpha-Beta pruning on a 3-ply binary game tree step-by-step.",
            "impact": "High",
            "effort": "Low",
            "target": "Solidify A* & Minimax concepts",
            "color": "#f4a261",
            "icon": "🧠"
        })
        rec_counter += 1
    else:
        recommendations.append({
            "id": f"rec-{rec_counter}",
            "priority": "Medium Priority",
            "title": "Focus Drill: Applied Mathematics & Linear Algebra",
            "category": "Curriculum Mastery",
            "description": "Reinforce vector spaces, matrix eigenvalues, and probability distributions used in AI modeling.",
            "reason": "Mathematical foundations reinforce all AI and networking algorithms.",
            "action": "Solve 3 eigenvalue and conditional probability problem sets.",
            "impact": "Medium",
            "effort": "Medium",
            "target": "Consolidate 80%+ math standing",
            "color": "#f4a261",
            "icon": "📐"
        })
        rec_counter += 1

    return recommendations
