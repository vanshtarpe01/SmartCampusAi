with open("ai/ml_model.py", "r") as f:
    content = f.read()

import re
content = re.sub(
    r"def load_dataset\(csv_path: Optional\[str\] = None\) -> pd\.DataFrame:[\s\S]+?return df",
    """def load_dataset(csv_path: Optional[str] = None) -> pd.DataFrame:
    \"\"\"Loads and returns the student dataset from Supabase (via data.py) or CSV fallback.\"\"\"
    try:
        from data import load_students_df
        df = load_students_df()
        if not df.empty:
            return df
    except ImportError:
        pass
        
    path = csv_path or DATASET_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Student dataset not found at: {path}")
    df = pd.read_csv(path)
    required_cols = FEATURE_COLUMNS + [TARGET_COLUMN]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column in dataset: '{col}'")
    return df""",
    content
)

with open("ai/ml_model.py", "w") as f:
    f.write(content)
