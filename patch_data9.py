with open("data.py", "r") as f:
    content = f.read()

import re

new_func = """def load_students_df() -> pd.DataFrame:
    \"\"\"Loads and returns the student records dataframe from Supabase.\"\"\"
    global _students_df_cache
    db = get_db()
    if not db:
        if _students_df_cache is not None:
            return _students_df_cache
        return pd.DataFrame(columns=["student_id", "name", "attendance", "study_hours", "assignment_marks", "internal_marks", "previous_marks", "performance_level"])
        
    try:
        response = db.table("students").select("*").execute()
        df = pd.DataFrame(response.data)
        if df.empty:
            df = pd.DataFrame(columns=["student_id", "name", "attendance", "study_hours", "assignment_marks", "internal_marks", "previous_marks", "performance_level"])
            _students_df_cache = df
            return df
            
        df = df.dropna(subset=["student_id"])
        df["student_id"] = df["student_id"].astype(str)
        if "name" in df.columns:
            df["name"] = df["name"].fillna("Unknown").astype(str)
        else:
            df["name"] = "Unknown"
        if "performance_level" in df.columns:
            df["performance_level"] = df["performance_level"].fillna("Unknown").astype(str)
        else:
            df["performance_level"] = "Unknown"
            
        df["attendance"] = df["attendance"].fillna(0).astype(float)
        df["study_hours"] = df["study_hours"].fillna(0).astype(float)
        df["assignment_marks"] = df["assignment_marks"].fillna(0).astype(float)
        df["internal_marks"] = df["internal_marks"].fillna(0).astype(float)
        df["previous_marks"] = df["previous_marks"].fillna(0).astype(float)
        
        _students_df_cache = df
        return df
    except Exception as e:
        print(f"Error loading students from DB: {e}")
        if _students_df_cache is not None:
            return _students_df_cache
        return pd.DataFrame(columns=["student_id", "name", "attendance", "study_hours", "assignment_marks", "internal_marks", "previous_marks", "performance_level"])"""

content = re.sub(r"def load_students_df\(\) -> pd\.DataFrame:[\s\S]+?return pd\.DataFrame\(\)", new_func, content)

with open("data.py", "w") as f:
    f.write(content)
