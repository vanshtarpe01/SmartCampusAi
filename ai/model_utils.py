"""SmartCampus AI - Machine Learning Model Utilities
Handles input validation, rule-based + ML fusion logic,
explainable AI diagnostics, and natural language student insights.
"""

from typing import Dict, Any, Tuple, Optional, List


def validate_student_inputs(
    attendance: float,
    study_hours: float,
    assignment_marks: float,
    internal_marks: float,
    previous_marks: float
) -> Tuple[bool, Optional[str]]:
    """Validates student inputs against allowable academic ranges.

Returns:
(is_valid: bool, error_message: Optional[str])
"""
    if not (0.0 <= attendance <= 100.0):
        return False, f"Attendance must be between 0% and 100%. (Provided: {attendance})"

    if not (0.0 <= study_hours <= 24.0):
        return False, f"Study Hours must be between 0 and 24 hrs/day. (Provided: {study_hours})"

    if not (0.0 <= assignment_marks <= 10.0):
        return False, f"Assignment Marks must be between 0 and 10. (Provided: {assignment_marks})"

    if not (0.0 <= internal_marks <= 50.0):
        return False, f"Internal Marks must be between 0 and 50. (Provided: {internal_marks})"

    if not (0.0 <= previous_marks <= 100.0):
        return False, f"Previous Marks must be between 0% and 100%. (Provided: {previous_marks})"

    return True, None


def generate_explainability_reasons(
    inputs: Dict[str, float],
    predicted_level: str
) -> List[Dict[str, str]]:
    """Generates explainable, human-readable reasons justifying the AI assessment."""
    att = inputs.get("attendance", 0.0)
    hrs = inputs.get("study_hours", 0.0)
    asn = inputs.get("assignment_marks", 0.0)
    itm = inputs.get("internal_marks", 0.0)
    prv = inputs.get("previous_marks", 0.0)

    reasons = []

    # Attendance explanation
    if att >= 85.0:
        reasons.append({
            "type": "positive",
            "text": f"Attendance ({att:.1f}%) is well above institutional minimums, providing regular classroom immersion."
        })
    elif att >= 75.0:
        reasons.append({
            "type": "positive",
            "text": f"Attendance ({att:.1f}%) meets university examination eligibility standards (≥75%)."
        })
    else:
        reasons.append({
            "type": "warning",
            "text": f"Attendance ({att:.1f}%) is below the required 75% eligibility threshold, posing risk of exam debarment."
        })

    # Internal marks explanation (scaled out of 50)
    if itm >= 40.0:
        reasons.append({
            "type": "positive",
            "text": f"Internal test score ({itm:.1f}/50) demonstrates strong foundational mastery in technical coursework."
        })
    elif itm >= 30.0:
        reasons.append({
            "type": "neutral",
            "text": f"Internal test score ({itm:.1f}/50) represents satisfactory mid-tier academic performance."
        })
    else:
        reasons.append({
            "type": "warning",
            "text": f"Internal test score ({itm:.1f}/50) indicates urgent need for syllabus revision before finals."
        })

    # Study hours explanation
    if hrs >= 4.0:
        reasons.append({
            "type": "positive",
            "text": f"Daily dedicated study habit ({hrs:.1f} hrs/day) ensures continuous concept reinforcement."
        })
    elif hrs >= 2.5:
        reasons.append({
            "type": "neutral",
            "text": f"Daily study time ({hrs:.1f} hrs/day) is adequate but could be expanded during exam preparations."
        })
    else:
        reasons.append({
            "type": "warning",
            "text": f"Daily study routine ({hrs:.1f} hrs/day) is critically low; recommended target is 3.0+ hours."
        })

    # Previous marks & assignments
    if prv >= 80.0:
        reasons.append({
            "type": "positive",
            "text": f"Historical semester performance ({prv:.1f}%) reflects consistent baseline aptitude."
        })
    elif prv < 55.0:
        reasons.append({
            "type": "warning",
            "text": f"Previous semester score ({prv:.1f}%) indicates cumulative academic vulnerability."
        })

    if asn < 6.0:
        reasons.append({
            "type": "warning",
            "text": f"Assignment submission score ({asn:.1f}/10) reflects missed or incomplete continuous assessment."
        })

    return reasons


def combine_rule_and_ml(
    rule_result: Dict[str, Any],
    ml_result: Dict[str, Any]
) -> Dict[str, Any]:
    """Combines Rule-Based analysis with Machine Learning prediction.

Evaluates whether both systems reach consensus or diverge,
and produces an actionable student summary.
"""
    rule_level = rule_result.get("level", "Average")
    ml_level = ml_result.get("predicted_level", "Average")
    inputs = ml_result.get("input_features", {})

    agrees = (rule_level.strip().lower() == ml_level.strip().lower())

    if agrees:
        consensus_text = f"Both AI systems agree that the student is performing at a {rule_level} level."
        final_assessment = rule_level
    else:
        consensus_text = (
            f"Rule-based analysis indicates {rule_level} performance, "
            f"while the ML Decision Tree model predicts {ml_level} performance. "
            f"This divergence reflects borderline indicators across study habits and continuous assessments."
        )
        # In case of divergence, display both transparently
        final_assessment = f"{ml_level} (ML) / {rule_level} (Rules)"

    # Generate student AI insight
    att = inputs.get("attendance", 75.0)
    hrs = inputs.get("study_hours", 2.5)
    itm = inputs.get("internal_marks", 35.0)
    prv = inputs.get("previous_marks", 65.0)

    strengths = []
    if att >= 80.0:
        strengths.append("attendance")
    if itm >= 38.0:
        strengths.append("internal marks")
    if prv >= 75.0:
        strengths.append("previous marks")
    if hrs >= 3.5:
        strengths.append("consistent study hours")

    improvements = []
    if att < 75.0:
        improvements.append("attendance")
    if hrs < 3.0:
        improvements.append("daily study hours")
    if itm < 32.0:
        improvements.append("internal test preparation")

    strength_clause = f"Your {', '.join(strengths)} {'is' if len(strengths)==1 else 'are'} strong." if strengths else "Your baseline performance is stable."
    imp_clause = f"Increasing your {', '.join(improvements)} may further elevate your standing." if improvements else "Maintaining this consistency will secure top results."

    ai_insight = f"Your predicted academic performance is {ml_level}. {strength_clause} {imp_clause}"

    explainability_reasons = generate_explainability_reasons(inputs, ml_level)

    return {
        "rule_level": rule_level,
        "ml_level": ml_level,
        "agrees": agrees,
        "consensus_text": consensus_text,
        "final_assessment": final_assessment,
        "ai_insight": ai_insight,
        "reasons": explainability_reasons
    }
