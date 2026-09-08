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
        if not df.empty:
            df = df.dropna(subset=["student_id"])
            df["student_id"] = df["student_id"].astype(str)
            if "name" in df.columns:
                df["name"] = df["name"].fillna("Unknown").astype(str)
            df["attendance"] = df["attendance"].astype(float)
            df["study_hours"] = df["study_hours"].astype(float)
            df["assignment_marks"] = df["assignment_marks"].astype(float)
            df["internal_marks"] = df["internal_marks"].astype(float)
            df["previous_marks"] = df["previous_marks"].astype(float)
        _students_df_cache = df
        return df
    except Exception as e:
        print(f"Error loading students from DB: {e}")
        if _students_df_cache is not None:
            return _students_df_cache
        return pd.DataFrame()"""

content = re.sub(r"def load_students_df\(\) -> pd\.DataFrame:[\s\S]+?return pd\.DataFrame\(\)", new_func, content)

with open("data.py", "w") as f:
    f.write(content)
