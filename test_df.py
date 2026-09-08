from data import load_students_df
df = load_students_df()
print("Total rows:", len(df))
if not df.empty:
    print(df["student_id"].tolist())
    print("Nulls in student_id:", df["student_id"].isnull().sum())
    print("NaT/NaNs:", [x for x in df["student_id"].tolist() if not isinstance(x, str)])
