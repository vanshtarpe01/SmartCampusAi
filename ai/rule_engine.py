"""SmartCampus AI - Rule Engine Module
Implements explicit, explainable expert system rules for student academic health analysis.
Evaluates attendance, study hours, assignments, internal tests, and past performance.
Generates strengths, weaknesses, warnings, and diagnostic observations.
"""

from typing import Dict, List, Any


def evaluate_student_rules(
    attendance: float,
    study_hours: float,
    assignment_marks: float,
    internal_marks: float,
    previous_marks: float
) -> Dict[str, List[str]]:
    """Evaluates rule-based expert logic on a student's academic metrics.

Args:
attendance: Float percentage (0 to 100)
study_hours: Daily study hours (e.g. 1.0 to 6.0)
assignment_marks: Assignment score on 0-10 scale
internal_marks: Internal test score on 0-50 scale
previous_marks: Previous semester score on 0-100 scale

Returns:
Dict containing lists of 'strengths', 'weaknesses', 'warnings', and 'observations'.
"""
    strengths: List[str] = []
    weaknesses: List[str] = []
    warnings: List[str] = []
    observations: List[str] = []

    # ------------------------------------------------------------
    # RULE SET 1: ATTENDANCE
    # ------------------------------------------------------------
    if attendance < 60.0:
        weaknesses.append(f"Critically low attendance ({attendance:.1f}%)")
        warnings.append(f"CRITICAL: Attendance is at {attendance:.1f}%, far below the 75% minimum threshold for university exam eligibility.")
    elif attendance < 75.0:
        weaknesses.append(f"Attendance ({attendance:.1f}%) below mandatory 75% requirement")
        warnings.append(f"Warning: Current attendance ({attendance:.1f}%) is below the 75% university eligibility requirement.")
    elif attendance >= 85.0:
        strengths.append(f"Excellent attendance record ({attendance:.1f}%)")
    else:
        # Between 75 and 85
        strengths.append(f"Satisfactory attendance ({attendance:.1f}%), compliant with eligibility rules")

    # ------------------------------------------------------------
    # RULE SET 2: STUDY HOURS
    # ------------------------------------------------------------
    if study_hours < 1.5:
        weaknesses.append(f"Insufficient daily study time ({study_hours:.1f} hrs/day)")
        warnings.append(f"Alert: Daily study time of {study_hours:.1f} hours is insufficient to cover exam syllabus topics effectively.")
    elif study_hours < 2.5:
        weaknesses.append(f"Sub-optimal study consistency ({study_hours:.1f} hrs/day)")
        warnings.append(f"Notice: Daily study commitment ({study_hours:.1f} hrs/day) is below the recommended 3.0+ hour baseline.")
    elif study_hours >= 4.0:
        strengths.append(f"High daily study dedication ({study_hours:.1f} hrs/day)")
    else:
        strengths.append(f"Consistent daily study pattern ({study_hours:.1f} hrs/day)")

    # ------------------------------------------------------------
    # RULE SET 3: ASSIGNMENT MARKS (Scale 0-10)
    # ------------------------------------------------------------
    if assignment_marks < 5.0:
        weaknesses.append(f"Low assignment performance ({assignment_marks:.1f}/10)")
        warnings.append(f"Alert: Assignment scores ({assignment_marks:.1f}/10) indicate incomplete lab coursework or missed deadlines.")
    elif assignment_marks < 6.5:
        weaknesses.append(f"Average assignment marks ({assignment_marks:.1f}/10)")
    elif assignment_marks >= 8.5:
        strengths.append(f"Top-tier assignment & practical lab scores ({assignment_marks:.1f}/10)")
    else:
        strengths.append(f"Good assignment completion rate ({assignment_marks:.1f}/10)")

    # ------------------------------------------------------------
    # RULE SET 4: INTERNAL TEST MARKS (Scale 0-50)
    # ------------------------------------------------------------
    if internal_marks < 25.0:
        weaknesses.append(f"Low internal assessment score ({internal_marks:.1f}/50 - {internal_marks * 2:.0f}%)")
        warnings.append(f"Critical: Internal examination score ({internal_marks:.1f}/50) is below the 50% passing cutoff; remediation required.")
    elif internal_marks < 33.0:
        weaknesses.append(f"Internal assessment ({internal_marks:.1f}/50) needs reinforcement")
        warnings.append(f"Notice: Internal score ({internal_marks:.1f}/50) indicates conceptual revision is needed before finals.")
    elif internal_marks >= 42.0:
        strengths.append(f"Outstanding internal test performance ({internal_marks:.1f}/50 - {internal_marks * 2:.0f}%)")
    else:
        strengths.append(f"Solid internal examination results ({internal_marks:.1f}/50)")

    # ------------------------------------------------------------
    # RULE SET 5: PREVIOUS SEMESTER MARKS (Scale 0-100)
    # ------------------------------------------------------------
    if previous_marks < 45.0:
        weaknesses.append(f"Previous semester grade ({previous_marks:.1f}%) is in critical territory")
        warnings.append(f"Alert: Previous semester mark ({previous_marks:.1f}%) shows past backlog risk and knowledge deficits.")
    elif previous_marks < 60.0:
        weaknesses.append(f"Previous academic foundation ({previous_marks:.1f}%) requires consolidation")
    elif previous_marks >= 80.0:
        strengths.append(f"Strong historical academic foundation ({previous_marks:.1f}%)")
    else:
        strengths.append(f"Steady previous examination record ({previous_marks:.1f}%)")

    # ------------------------------------------------------------
    # SYNTHESIS & DIAGNOSTIC OBSERVATIONS
    # ------------------------------------------------------------
    weakness_count = len(weaknesses)
    strength_count = len(strengths)

    if weakness_count == 0:
        observations.append("Profile demonstrates exemplary academic rigor across all monitored indicators.")
        observations.append("Student is well-positioned for top-bracket academic honors and competitive placements.")
    elif weakness_count == 1:
        observations.append(f"Overall healthy academic profile with a single isolated area for improvement ({weaknesses[0]}).")
        observations.append("Targeted intervention will quickly elevate the student to honor-roll status.")
    elif weakness_count <= 2:
        observations.append("Student exhibits balanced performance, but multi-factor friction is beginning to impede progress.")
        observations.append("Implementing a structured daily timetable will restore academic equilibrium.")
    else:
        observations.append("Multi-factor academic distress detected: attendance, testing, and study hours require immediate advisor intervention.")
        observations.append("High priority: Formulate a customized remedial roadmap to prevent semester failure or exam debarment.")

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "warnings": warnings,
        "observations": observations
    }
