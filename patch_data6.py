with open("data.py", "r") as f:
    content = f.read()

content = content.replace("weekly_activity = {}", '''weekly_activity = {
    "Monday": 3.0,
    "Tuesday": 3.5,
    "Wednesday": 4.0,
    "Thursday": 2.5,
    "Friday": 3.5
}''')

content = content.replace("weekly_activity_detailed = []", '''weekly_activity_detailed = [
    {"day": "Monday", "hours": 3.0, "focus": "AI & Math", "status": "Target Met"},
    {"day": "Tuesday", "hours": 3.5, "focus": "DBMS & Networking", "status": "Target Met"},
    {"day": "Wednesday", "hours": 4.0, "focus": "AI Lab & Algorithms", "status": "Exceeded Target"},
    {"day": "Thursday", "hours": 2.5, "focus": "Networking Revision", "status": "Target Met"},
    {"day": "Friday", "hours": 3.5, "focus": "Mock Test & Quizzes", "status": "Target Met"}
]''')

content = content.replace("performance_timeline = []", '''performance_timeline = [
    {"week": "Week 1", "score": 68, "attendance": 80, "hours": 2.6},
    {"week": "Week 2", "score": 71, "attendance": 81, "hours": 2.8},
    {"week": "Week 3", "score": 70, "attendance": 80, "hours": 2.9},
    {"week": "Week 4", "score": 75, "attendance": 83, "hours": 3.1},
    {"week": "Week 5", "score": 74, "attendance": 82, "hours": 3.0},
    {"week": "Week 6", "score": 78, "attendance": 82, "hours": 3.2}
]''')

content = content.replace("academic_wellness = {}", '''academic_wellness = {
    "Conceptual Knowledge": 80,
    "Study Consistency": 75,
    "Understanding": 82,
    "Practical Application": 70,
    "Problem Solving": 85
}''')

content = content.replace("recent_activities = []", '''recent_activities = [
    {"time": "Today, 10:30 AM", "title": "Completed AI Lab Assignment on BFS/DFS", "type": "assignment", "badge": "Completed"},
    {"time": "Yesterday, 04:00 PM", "title": "Studied 3.0 hours: DBMS Normalization", "type": "study", "badge": "Verified"},
    {"time": "2 days ago", "title": "Networking Quiz 3 submitted (Scored 68%)", "type": "quiz", "badge": "Needs Review"},
    {"time": "3 days ago", "title": "Math Problem Set #5 top percentile score", "type": "achievement", "badge": "Top 5%"}
]''')

with open("data.py", "w") as f:
    f.write(content)
