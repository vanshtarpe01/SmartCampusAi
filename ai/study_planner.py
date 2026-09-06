"""SmartCampus AI - Study Planner Module
Generates personalized, time-blocked study schedules based on exam dates,
available study hours, weak topics, and subject difficulty levels.
No external API calls; pure Python algorithmic scheduling.
"""

from datetime import date, datetime, timedelta
from typing import Dict, List, Any


def generate_study_plan(
    exam_date: date,
    available_hours: float,
    subject: str = "Artificial Intelligence",
    weak_topic: str = "BFS & DFS Graph Traversals",
    difficulty: str = "Intermediate"
) -> Dict[str, Any]:
    """Generates an optimal, time-blocked study plan tailored to the student's constraints.

    Args:
        exam_date: Date of the target examination.
        available_hours: Hours available to study today (e.g., 1.0 to 8.0).
        subject: Target course/subject (e.g. 'Artificial Intelligence', 'Networking').
        weak_topic: Focus area identified by the student or rule engine.
        difficulty: Complexity level ('Beginner', 'Intermediate', 'Advanced').

    Returns:
        Structured dictionary with slots, time intervals, topics, and AI notes.
    """
    today = date.today()
    days_left = max((exam_date - today).days, 1)

    # Sanitize available hours
    hours = max(1.0, min(8.0, float(available_hours)))
    diff_normalized = difficulty.capitalize()
    if diff_normalized not in ["Beginner", "Intermediate", "Advanced"]:
        diff_normalized = "Intermediate"

    # Define curriculum secondary subjects to balance the study day
    secondary_subjects = {
        "Artificial Intelligence": [
            ("Networking", "OSI 7 Layers & TCP/IP Handshake", "Intermediate", "⚡"),
            ("DBMS", "Normalization Forms (1NF to BCNF)", "Intermediate", "🗄️"),
            ("Mathematics", "Discrete Math & Probability Distributions", "Intermediate", "📐")
        ],
        "Networking": [
            ("Artificial Intelligence", "Informed Search: A* & Heuristics", "Intermediate", "🤖"),
            ("DBMS", "Transaction Processing & ACID Properties", "Intermediate", "🗄️"),
            ("Mathematics", "Graph Theory & Minimum Spanning Trees", "Intermediate", "📐")
        ],
        "DBMS": [
            ("Artificial Intelligence", "Adversarial Search: Minimax & Alpha-Beta", "Intermediate", "🤖"),
            ("Networking", "Routing Protocols (OSPF, BGP, RIP)", "Intermediate", "⚡"),
            ("Mathematics", "Relational Algebra & Set Theory", "Intermediate", "📐")
        ],
        "Mathematics": [
            ("Artificial Intelligence", "Machine Learning Mathematical Foundations", "Intermediate", "🤖"),
            ("Networking", "Subnetting & IP Addressing Calculations", "Intermediate", "⚡"),
            ("DBMS", "B-Trees & Indexing Algorithms", "Intermediate", "🗄️")
        ]
    }

    fallbacks = secondary_subjects.get(
        subject,
        [
            ("Artificial Intelligence", "Core AI Foundations & Search Algorithms", "Intermediate", "🤖"),
            ("Networking", "Computer Networking Fundamentals", "Intermediate", "⚡"),
            ("DBMS", "Relational Database Design", "Intermediate", "🗄️")
        ]
    )

    # Tailor focus activity by difficulty level
    if diff_normalized == "Advanced":
        primary_activity = f"Intensive Derivations & Edge Cases: {weak_topic}"
        primary_icon = "🔬"
        review_activity = "Past Year Midterm Exam Proofs & Hard Questions"
    elif diff_normalized == "Beginner":
        primary_activity = f"Concept Foundations & Visual Traces: {weak_topic}"
        primary_icon = "📖"
        review_activity = "Basic Solved Examples & Textbook Summary Notes"
    else:  # Intermediate
        primary_activity = f"Core Theory & Problem Solving: {weak_topic}"
        primary_icon = "🎯"
        review_activity = "Active Recall Quizzing & Sectional Practice Drills"

    # Build schedule slots dynamically based on available hours
    slots: List[Dict[str, Any]] = []

    # Slot 1: Primary focus on weak topic during peak morning focus
    slots.append({
        "time": "09:00 - 10:00",
        "subject": subject,
        "topic": primary_activity,
        "activity": "Deep Focus Session",
        "difficulty": diff_normalized,
        "status": "In Progress",
        "icon": primary_icon
    })

    if hours >= 2.0:
        # Slot 2: Secondary subject reinforcement
        sec_subj, sec_topic, sec_diff, sec_icon = fallbacks[0]
        slots.append({
            "time": "10:15 - 11:15",
            "subject": sec_subj,
            "topic": f"Target Revision: {sec_topic}",
            "activity": "Active Study Block",
            "difficulty": sec_diff,
            "status": "Pending",
            "icon": sec_icon
        })

    if hours >= 3.0:
        # Slot 3: Deep dive problem solving for primary subject
        slots.append({
            "time": "11:30 - 12:30",
            "subject": subject,
            "topic": review_activity,
            "activity": "Exam Practice & Drills",
            "difficulty": diff_normalized,
            "status": "Pending",
            "icon": "📝"
        })

    if hours >= 4.0:
        # Slot 4: Afternoon study block with another curriculum subject
        sec_subj, sec_topic, sec_diff, sec_icon = fallbacks[1]
        slots.append({
            "time": "14:00 - 15:00",
            "subject": sec_subj,
            "topic": f"Concept Consolidation: {sec_topic}",
            "activity": "Problem Solving",
            "difficulty": sec_diff,
            "status": "Pending",
            "icon": sec_icon
        })

    if hours >= 5.0:
        # Slot 5: Third subject coverage or foundational math
        sec_subj, sec_topic, sec_diff, sec_icon = fallbacks[2]
        slots.append({
            "time": "15:15 - 16:15",
            "subject": sec_subj,
            "topic": f"Syllabus Unit Review: {sec_topic}",
            "activity": "Core Practice",
            "difficulty": sec_diff,
            "status": "Pending",
            "icon": sec_icon
        })

    if hours >= 6.0:
        # Slot 6: Evening mock test & timed retrieval
        slots.append({
            "time": "16:45 - 17:45",
            "subject": subject,
            "topic": f"Timed 60-Minute Mock Test on {weak_topic}",
            "activity": "Timed Evaluation",
            "difficulty": diff_normalized,
            "status": "Pending",
            "icon": "⏱️"
        })

    if hours >= 7.0:
        # Slot 7: Flashcard & mistake analysis
        slots.append({
            "time": "18:00 - 19:00",
            "subject": subject,
            "topic": "Error Log Analysis & Rapid Active Recall",
            "activity": "Flashcards & Synthesis",
            "difficulty": "Intermediate",
            "status": "Pending",
            "icon": "💡"
        })

    if hours >= 8.0:
        # Slot 8: Daily wrap-up and formula sheet construction
        slots.append({
            "time": "19:15 - 20:15",
            "subject": "Comprehensive Synthesis",
            "topic": f"Formula & Cheat-Sheet Construction ({subject} & {fallbacks[0][0]})",
            "activity": "Consolidation",
            "difficulty": "All Levels",
            "status": "Pending",
            "icon": "📋"
        })

    # Generate custom algorithmic note
    if days_left <= 3:
        urgency = f"CRITICAL: Only {days_left} day(s) until your {subject} exam! Focus entirely on high-weightage topics and active recall."
    elif days_left <= 7:
        urgency = f"Exam Week Countdown: {days_left} days remaining. Emphasize timed mock problems and formula memorization."
    else:
        urgency = f"Paced Preparation: {days_left} days available until exam day. Structured spacing prevents cognitive fatigue."

    ai_note = (
        f"{urgency} Your schedule dedicates primary focus to '{weak_topic}' ({diff_normalized} Level) "
        f"across {len(slots)} focused study block(s) totaling {hours} hour(s) with mandatory 15-minute breaks."
    )

    return {
        "generated_on": today.strftime("%Y-%m-%d"),
        "exam_date": exam_date.strftime("%Y-%m-%d"),
        "days_until_exam": days_left,
        "available_hours": hours,
        "primary_subject": subject,
        "weak_topic": weak_topic,
        "difficulty": diff_normalized,
        "slots": slots,
        "ai_note": ai_note
    }
