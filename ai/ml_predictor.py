"""SmartCampus AI - Machine Learning Predictor Module
Provides high-level inference interface using the trained Decision Tree model.
Calculates performance classification, prediction probabilities/confidence,
and identifies key influencing academic factors.
"""

from typing import Dict, Any
import numpy as np
import pandas as pd
from ai.ml_model import get_or_train_model, FEATURE_COLUMNS


def predict_performance(
    attendance: float,
    study_hours: float,
    assignment_marks: float,
    internal_marks: float,
    previous_marks: float
) -> Dict[str, Any]:
    """Predicts a student's academic performance level using the trained Decision Tree.

Args:
attendance: Attendance percentage (0 - 100)
study_hours: Daily study hours (0 - 24)
assignment_marks: Continuous assessment assignment score (0 - 10)
internal_marks: Internal examination marks (0 - 50)
previous_marks: Previous semester / qualifying marks percentage (0 - 100)

Returns:
Dict containing:
- predicted_level: 'Excellent' | 'Good' | 'Average' | 'Needs Improvement'
- confidence: float (0 - 100 percentage)
- probabilities: dict of class -> probability
- input_features: dictionary of inputs
- feature_importance: dict of model feature importances
- top_factor: name of the top influencing feature
"""
    bundle = get_or_train_model()
    model = bundle["model"]
    feature_importance = bundle.get("feature_importance", {})

    # Create input DataFrame with strict column order
    input_data = {
        "attendance": [float(attendance)],
        "study_hours": [float(study_hours)],
        "assignment_marks": [float(assignment_marks)],
        "internal_marks": [float(internal_marks)],
        "previous_marks": [float(previous_marks)]
    }
    input_df = pd.DataFrame(input_data, columns=FEATURE_COLUMNS)

    # Inference
    raw_pred = model.predict(input_df)[0]
    predicted_level = str(raw_pred)

    # Confidence calculation via predict_proba
    confidence = 85.0  # Default fallback
    probabilities: Dict[str, float] = {}
    if hasattr(model, "predict_proba"):
        try:
            probs = model.predict_proba(input_df)[0]
            classes = list(model.classes_)
            for cls_name, prob in zip(classes, probs):
                probabilities[str(cls_name)] = round(float(prob) * 100.0, 1)

            max_prob = float(np.max(probs))
            confidence = round(max_prob * 100.0, 1)
        except Exception:
            probabilities = {predicted_level: 100.0}
            confidence = 100.0

    # Determine top influencing factor from model's actual feature importances
    top_feature_key = "previous_marks"
    if feature_importance:
        # Find the feature with highest importance
        sorted_feats = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        if sorted_feats and sorted_feats[0][1] > 0:
            top_feature_key = sorted_feats[0][0]

    feature_display_names = {
        "attendance": "Attendance",
        "study_hours": "Study Hours",
        "assignment_marks": "Assignment Marks",
        "internal_marks": "Internal Marks",
        "previous_marks": "Previous Marks"
    }
    top_factor = feature_display_names.get(top_feature_key, "Academic Evaluation")

    return {
        "predicted_level": predicted_level,
        "confidence": confidence,
        "probabilities": probabilities,
        "input_features": {
            "attendance": float(attendance),
            "study_hours": float(study_hours),
            "assignment_marks": float(assignment_marks),
            "internal_marks": float(internal_marks),
            "previous_marks": float(previous_marks)
        },
        "feature_importance": feature_importance,
        "top_factor": top_factor
    }
