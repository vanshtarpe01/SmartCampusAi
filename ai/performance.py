"""SmartCampus AI - Performance Engine Module
Calculates normalized multi-factor academic scores, categorizes performance levels,
evaluates risk tiers (LOW, MEDIUM, HIGH), and produces diagnostic insights.
Pure Python and NumPy/Pandas compatibility.
"""

from typing import Dict, Any, List
from ai.rule_engine import evaluate_student_rules


def analyze_student(student: Dict[str, Any]) -> Dict[str, Any]:
    """Analyzes a student's academic record and computes weighted performance,
risk level, diagnostic rules, and subject estimates.

Args:
student: Dict containing attendance, study_hours, assignment_marks,
internal_marks, previous_marks, and optionally name, student_id.

Returns:
Structured analysis dict with all scores, levels, strengths, and warnings.
"""
    # Extract metrics safely with standard fallbacks
    attendance = float(student.get("attendance", 75.0))
    study_hours = float(student.get("study_hours", 2.5))
    assignment_marks = float(student.get("assignment_marks", 7.0))
    internal_marks = float(student.get("internal_marks", 35.0))
    previous_marks = float(student.get("previous_marks", 70.0))

    # ------------------------------------------------------------
    # 1. NORMALIZATION TO 0 - 100 SCALE
    # ------------------------------------------------------------
    # Attendance is already 0 - 100
    norm_attendance = min(100.0, max(0.0, attendance))
    
    # Study hours: calibrated to 4.0 hrs/day benchmark for realistic academic schedules
    norm_study = min(100.0, max(0.0, (study_hours / 4.0) * 100.0))
    
    # Assignment marks: calibrated to 10-point scale
    norm_assignment = min(100.0, max(0.0, (assignment_marks / 10.0) * 100.0))
    
    # Internal marks: calibrated to 50-point scale
    norm_internal = min(100.0, max(0.0, (internal_marks / 50.0) * 100.0))
    
    # Previous marks: already 0 - 100 scale
    norm_previous = min(100.0, max(0.0, previous_marks))

    # ------------------------------------------------------------
    # 2. WEIGHTED PERFORMANCE SCORE CALCULATION
    # Attendance: 20%, Study Hours: 15%, Assignments: 15%,
    # Internal Marks: 25%, Previous Marks: 25%
    # ------------------------------------------------------------
    weighted_score = (
        norm_attendance * 0.20 +
        norm_study * 0.15 +
        norm_assignment * 0.15 +
        norm_internal * 0.25 +
        norm_previous * 0.25
    )
    performance_score = round(weighted_score, 1)

    # ------------------------------------------------------------
    # 3. PERFORMANCE LEVEL CATEGORIZATION
    # ------------------------------------------------------------
    if performance_score >= 90.0:
        performance_level = "Excellent"
    elif performance_score >= 75.0:
        performance_level = "Good"
    elif performance_score >= 60.0:
        performance_level = "Average"
    else:
        performance_level = "Needs Improvement"

    # ------------------------------------------------------------
    # 4. RISK LEVEL DETERMINATION
    # LOW: Good academic indicators, score >= 75
    # MEDIUM: Moderate friction (60 <= score < 75 or single weakness)
    # HIGH: Severe risk (score < 60 or attendance < 65 or low internal + study)
    # ------------------------------------------------------------
    if (
        performance_score < 60.0
        or attendance < 65.0
        or (internal_marks < 25.0 and study_hours < 2.0)
        or (previous_marks < 45.0 and attendance < 70.0)
    ):
        risk_level = "HIGH"
    elif (
        performance_score < 75.0
        or attendance < 75.0
        or study_hours < 2.5
        or internal_marks < 33.0
        or previous_marks < 60.0
    ):
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # ------------------------------------------------------------
    # 5. RULE-BASED EXPERT REASONING
    # ------------------------------------------------------------
    rule_results = evaluate_student_rules(
        attendance=attendance,
        study_hours=study_hours,
        assignment_marks=assignment_marks,
        internal_marks=internal_marks,
        previous_marks=previous_marks
    )

    # ------------------------------------------------------------
    # 6. ACADEMIC WELLNESS METRICS
    # ------------------------------------------------------------
    wellness = {
        "Conceptual Knowledge": min(100, int(norm_internal * 0.6 + norm_previous * 0.4)),
        "Study Consistency": min(100, int(norm_study * 0.7 + norm_attendance * 0.3)),
        "Understanding": min(100, int(norm_internal * 0.5 + norm_assignment * 0.5)),
        "Practical Application": min(100, int(norm_assignment * 0.7 + norm_study * 0.3)),
        "Problem Solving": min(100, int(norm_previous * 0.5 + norm_internal * 0.5))
    }
    wellness_score = round(sum(wellness.values()) / len(wellness), 1)

    # ------------------------------------------------------------
    # 7. DERIVED SUBJECT SCORES & DETAILS
    # Estimates aligned with the student's actual metrics
    # ------------------------------------------------------------
    math_score = int(min(100, max(30, norm_previous * 0.6 + norm_internal * 0.4)))
    ai_score = int(min(100, max(30, norm_assignment * 0.4 + norm_internal * 0.4 + norm_study * 0.2)))
    dbms_score = int(min(100, max(30, norm_internal * 0.5 + norm_assignment * 0.3 + norm_attendance * 0.2)))
    net_score = int(min(100, max(30, norm_previous * 0.4 + norm_study * 0.3 + norm_internal * 0.3)))

    subject_scores = {
        "Mathematics": math_score,
        "Artificial Intelligence": ai_score,
        "DBMS": dbms_score,
        "Networking": net_score
    }

    subject_details = {
        "Mathematics": {
            "score": math_score,
            "trend": "up" if math_score >= 75 else ("stable" if math_score >= 60 else "down"),
            "status": "Excellent" if math_score >= 80 else ("Good" if math_score >= 70 else "Needs Attention"),
            "credits": 4,
            "assignments": min(100, int(norm_assignment * 1.05)),
            "quizzes": min(100, int(norm_internal * 0.95)),
            "midterm": math_score,
            "color": "#00b4d8"
        },
        "Artificial Intelligence": {
            "score": ai_score,
            "trend": "up" if ai_score >= 75 else ("stable" if ai_score >= 65 else "down"),
            "status": "Excellent" if ai_score >= 80 else ("Good" if ai_score >= 70 else "Needs Attention"),
            "credits": 4,
            "assignments": min(100, int(norm_assignment)),
            "quizzes": min(100, int(norm_internal * 0.9)),
            "midterm": ai_score,
            "color": "#7b2cbf"
        },
        "DBMS": {
            "score": dbms_score,
            "trend": "up" if dbms_score >= 75 else ("stable" if dbms_score >= 65 else "down"),
            "status": "Excellent" if dbms_score >= 80 else ("Good" if dbms_score >= 70 else "Needs Attention"),
            "credits": 3,
            "assignments": min(100, int(norm_assignment * 0.98)),
            "quizzes": min(100, int(norm_internal * 0.95)),
            "midterm": dbms_score,
            "color": "#38b000"
        },
        "Networking": {
            "score": net_score,
            "trend": "up" if net_score >= 75 else ("stable" if net_score >= 65 else "down"),
            "status": "Excellent" if net_score >= 80 else ("Good" if net_score >= 70 else "Needs Attention"),
            "credits": 3,
            "assignments": min(100, int(norm_assignment * 0.92)),
            "quizzes": min(100, int(norm_internal * 0.88)),
            "midterm": net_score,
            "color": "#f4a261"
        }
    }

    # Weekly timeline progression estimate
    base_score = performance_score
    timeline = [
        {"week": "Week 1", "score": max(35, round(base_score - 8.0, 1)), "attendance": max(50, round(attendance - 3.0, 1)), "hours": max(1.0, round(study_hours - 0.6, 1))},
        {"week": "Week 2", "score": max(36, round(base_score - 5.0, 1)), "attendance": max(52, round(attendance - 2.0, 1)), "hours": max(1.1, round(study_hours - 0.4, 1))},
        {"week": "Week 3", "score": max(38, round(base_score - 6.0, 1)), "attendance": max(51, round(attendance - 2.5, 1)), "hours": max(1.0, round(study_hours - 0.3, 1))},
        {"week": "Week 4", "score": max(40, round(base_score - 2.0, 1)), "attendance": max(54, round(attendance + 1.0, 1)), "hours": max(1.2, round(study_hours - 0.1, 1))},
        {"week": "Week 5", "score": max(42, round(base_score - 3.0, 1)), "attendance": max(53, round(attendance, 1)), "hours": max(1.2, round(study_hours - 0.2, 1))},
        {"week": "Week 6", "score": round(base_score, 1), "attendance": round(attendance, 1), "hours": round(study_hours, 1)}
    ]

    analysis = {
        "student_id": student.get("student_id", "SC-2026-001"),
        "name": student.get("name", "Student"),
        "full_name": student.get("name", "Student"),
        "program": "B.Tech Computer Science & AI",
        "semester": "Semester 6",
        "attendance": attendance,
        "study_hours": study_hours,
        "assignment_marks": assignment_marks,
        "internal_marks": internal_marks,
        "previous_marks": previous_marks,
        "performance": performance_score,
        "overall": performance_score,
        "level": performance_level,
        "risk": risk_level,
        "wellness_score": wellness_score,
        "normalized": {
            "attendance": round(norm_attendance, 1),
            "study_hours": round(norm_study, 1),
            "assignments": round(norm_assignment, 1),
            "internal_marks": round(norm_internal, 1),
            "previous_marks": round(norm_previous, 1)
        },
        "strengths": rule_results["strengths"],
        "improvements": rule_results["weaknesses"],
        "weaknesses": rule_results["weaknesses"],
        "warnings": rule_results["warnings"],
        "observations": rule_results["observations"],
        "wellness": wellness,
        "subjects": subject_scores,
        "subject_details": subject_details,
        "timeline": timeline,
        "achievements": generate_achievements(performance_score, attendance, study_hours, assignment_marks)
    }

    analysis["ai_insight"] = generate_ai_insight(analysis)
    return analysis


def generate_achievements(score: float, attendance: float, study_hours: float, assignments: float) -> List[str]:
    """Generates milestone badges achieved by the student."""
    achievements = []
    if score >= 85:
        achievements.append("Honor Roll Scholar (Top 10%) 🏆")
    elif score >= 75:
        achievements.append("Consistent Performer (Top 25%) ⭐")
    
    if attendance >= 85:
        achievements.append("85%+ Attendance League 🎖️")
    elif attendance >= 75:
        achievements.append("Compliant Attendance Status 📋")
        
    if study_hours >= 4.0:
        achievements.append("Master of Focus (4+ hrs/day) ⏳")
        
    if assignments >= 8.5:
        achievements.append("Lab Excellence Award 🔬")

    if not achievements:
        achievements.append("Academic Journey in Progress 🚀")

    return achievements


def generate_ai_insight(analysis: Dict[str, Any]) -> str:
    """Generates an explainable natural-language performance summary."""
    name = analysis.get("name", "Student")
    score = analysis["performance"]
    level = analysis["level"]
    risk = analysis["risk"]
    strengths = analysis.get("strengths", [])
    weaknesses = analysis.get("weaknesses", [])

    insight_parts = [
        f"{name}'s academic index is {score}% ({level} Standing) with a {risk} Risk classification."
    ]

    if strengths:
        insight_parts.append(f"Primary asset: {strengths[0]}.")

    if weaknesses:
        insight_parts.append(f"Primary focus needed: {weaknesses[0]}.")
    else:
        insight_parts.append("Maintain the present study routine to sustain honors trajectory.")

    return " ".join(insight_parts)
