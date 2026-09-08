import pandas as pd
df = pd.DataFrame([{"student_id": "SC-1", "name": "A"}, {"student_id": None, "name": "B"}])
print(df["student_id"].tolist())
