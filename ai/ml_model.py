"""SmartCampus AI - Machine Learning Model Engine
Implements DecisionTreeClassifier for student academic performance prediction.
Handles dataset loading, preprocessing, model training, evaluation,
model persistence (joblib), and feature importance extraction.
"""

import os
from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
import joblib

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "data", "students.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_FILE_PATH = os.path.join(MODEL_DIR, "student_performance_model.pkl")

# ML Configuration
FEATURE_COLUMNS = [
    "attendance",
    "study_hours",
    "assignment_marks",
    "internal_marks",
    "previous_marks"
]
TARGET_COLUMN = "performance_level"
TARGET_CLASSES = ["Excellent", "Good", "Average", "Needs Improvement"]

# In-memory cache for loaded model bundle
_MODEL_BUNDLE_CACHE: Optional[Dict[str, Any]] = None


def load_dataset(csv_path: Optional[str] = None) -> pd.DataFrame:
    """Loads and returns the student dataset from CSV."""
    path = csv_path or DATASET_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Student dataset not found at: {path}")

    df = pd.read_csv(path)
    required_cols = FEATURE_COLUMNS + [TARGET_COLUMN]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column in dataset: '{col}'")

    return df


def preprocess_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Cleans dataset, validates data types, handles nulls, and splits X and y."""
    cleaned = df.copy()

    # Drop rows with nulls in features or target
    cleaned = cleaned.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN])

    # Enforce numeric types for feature columns
    for col in FEATURE_COLUMNS:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    cleaned = cleaned.dropna(subset=FEATURE_COLUMNS)

    # Filter out invalid out-of-bound ranges
    valid_mask = (
        (cleaned["attendance"] >= 0) & (cleaned["attendance"] <= 100) &
        (cleaned["study_hours"] >= 0) & (cleaned["study_hours"] <= 24) &
        (cleaned["assignment_marks"] >= 0) & (cleaned["assignment_marks"] <= 10) &
        (cleaned["internal_marks"] >= 0) & (cleaned["internal_marks"] <= 50) &
        (cleaned["previous_marks"] >= 0) & (cleaned["previous_marks"] <= 100)
    )
    cleaned = cleaned[valid_mask]

    X = cleaned[FEATURE_COLUMNS]
    y = cleaned[TARGET_COLUMN].astype(str)

    return X, y


def evaluate_model(
    model: DecisionTreeClassifier,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> Dict[str, Any]:
    """Calculates accuracy, precision, recall, F1 score, and confusion matrix."""
    y_pred = model.predict(X_test)

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
    rec = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
    f1 = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))

    # Confusion matrix using model classes
    classes = list(model.classes_)
    cm = confusion_matrix(y_test, y_pred, labels=classes).tolist()
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1,
        "confusion_matrix": cm,
        "classes": classes,
        "classification_report": report,
        "test_sample_count": len(y_test)
    }


def save_model(
    model: DecisionTreeClassifier,
    metrics: Dict[str, Any],
    feature_importance: Dict[str, float],
    file_path: Optional[str] = None
) -> str:
    """Saves the trained model and associated metadata to a joblib pickle file."""
    path = file_path or MODEL_FILE_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)

    bundle = {
        "model": model,
        "feature_names": FEATURE_COLUMNS,
        "target_classes": list(model.classes_),
        "metrics": metrics,
        "feature_importance": feature_importance
    }

    joblib.dump(bundle, path)
    return path


def load_model(file_path: Optional[str] = None) -> Dict[str, Any]:
    """Loads the model bundle from disk into memory."""
    global _MODEL_BUNDLE_CACHE
    path = file_path or MODEL_FILE_PATH

    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at: {path}")

    bundle = joblib.load(path)
    _MODEL_BUNDLE_CACHE = bundle
    return bundle


def train_model(
    csv_path: Optional[str] = None,
    test_size: float = 0.20,
    random_state: int = 42
) -> Dict[str, Any]:
    """Trains a DecisionTreeClassifier on students.csv and persists the model."""
    global _MODEL_BUNDLE_CACHE

    df = load_dataset(csv_path)
    X, y = preprocess_data(df)

    # Train / Test split with stratification to preserve class distributions
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    # Initialize and fit DecisionTreeClassifier
    model = DecisionTreeClassifier(
        max_depth=5,
        random_state=random_state
    )
    model.fit(X_train, y_train)

    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test)

    # Extract feature importances
    raw_importances = model.feature_importances_
    total_imp = float(np.sum(raw_importances))
    feature_importance = {}
    for feat, imp in zip(FEATURE_COLUMNS, raw_importances):
        norm_val = float(imp / total_imp) if total_imp > 0 else 0.0
        feature_importance[feat] = round(norm_val, 4)

    # Save to disk
    save_model(model, metrics, feature_importance)

    bundle = {
        "model": model,
        "feature_names": FEATURE_COLUMNS,
        "target_classes": list(model.classes_),
        "metrics": metrics,
        "feature_importance": feature_importance
    }
    _MODEL_BUNDLE_CACHE = bundle
    return bundle


def get_or_train_model() -> Dict[str, Any]:
    """Returns the cached or persisted model bundle, or trains a new one if missing."""
    global _MODEL_BUNDLE_CACHE
    if _MODEL_BUNDLE_CACHE is not None:
        return _MODEL_BUNDLE_CACHE

    if os.path.exists(MODEL_FILE_PATH):
        try:
            return load_model(MODEL_FILE_PATH)
        except Exception:
            pass

    # Model file does not exist or failed to load, train now
    return train_model()


def get_model_metrics() -> Dict[str, Any]:
    """Returns the latest evaluation metrics of the trained ML model."""
    bundle = get_or_train_model()
    return bundle.get("metrics", {})


def get_feature_importance() -> Dict[str, float]:
    """Returns the calculated feature importances from the trained Decision Tree."""
    bundle = get_or_train_model()
    return bundle.get("feature_importance", {})
