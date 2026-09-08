import os
import json
import uuid
import pandas as pd
from supabase import create_client, Client
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def migrate():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        print("Missing SUPABASE_URL or SUPABASE_KEY. Cannot migrate.")
        return

    supabase: Client = create_client(url, key)
    print("Connected to Supabase. Starting migration...")

    base_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    
    # 1. Migrate Users
    users_file = os.path.join(base_dir, "users.json")
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            users_data = json.load(f)
            
        for username, uinfo in users_data.items():
            try:
                supabase.table("users").upsert({
                    "username": username,
                    "password_hash": uinfo.get("password"), # Real project should hash
                    "role": uinfo.get("role"),
                    "name": uinfo.get("name")
                }).execute()
            except Exception as e:
                print(f"Error migrating user {username}: {e}")
                
        print(f"Migrated {len(users_data)} users.")

    # 2. Migrate Students & Academic Records
    csv_file = os.path.join(base_dir, "students.csv")
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        count = 0
        for _, row in df.iterrows():
            try:
                # Upsert user if missing
                supabase.table("users").upsert({
                    "username": row["student_id"],
                    "password_hash": "student123", # Default
                    "role": "student",
                    "name": row["name"]
                }).execute()
                
                # Upsert student
                supabase.table("students").upsert({
                    "student_id": row["student_id"],
                    "name": row["name"],
                    "attendance": float(row.get("attendance", 0)),
                    "study_hours": float(row.get("study_hours", 0)),
                    "assignment_marks": float(row.get("assignment_marks", 0)),
                    "internal_marks": float(row.get("internal_marks", 0)),
                    "previous_marks": float(row.get("previous_marks", 0)),
                    "performance_level": row.get("performance_level", "Average")
                }).execute()
                count += 1
            except Exception as e:
                print(f"Error migrating student {row['student_id']}: {e}")
        print(f"Migrated {count} students.")

    # 3. Migrate Skills
    skills_file = os.path.join(base_dir, "skills.json")
    if os.path.exists(skills_file):
        with open(skills_file, "r") as f:
            skills_data = json.load(f)
            
        count = 0
        for student_id, skills in skills_data.items():
            for s in skills:
                try:
                    supabase.table("skills").upsert({
                        "id": s.get("id", str(uuid.uuid4())),
                        "student_id": student_id,
                        "name": s.get("name"),
                        "category": s.get("category"),
                        "level": s.get("level")
                    }).execute()
                    count += 1
                except Exception as e:
                    print(f"Error migrating skill for {student_id}: {e}")
        print(f"Migrated {count} skills.")

    # 4. Migrate Projects
    projects_file = os.path.join(base_dir, "projects.json")
    if os.path.exists(projects_file):
        with open(projects_file, "r") as f:
            projects_data = json.load(f)
            
        count = 0
        insp_count = 0
        for student_id, projects in projects_data.items():
            for p in projects:
                p_id = p.get("id", str(uuid.uuid4()))
                try:
                    supabase.table("projects").upsert({
                        "id": p_id,
                        "student_id": student_id,
                        "name": p.get("name"),
                        "description": p.get("description"),
                        "technologies": p.get("technologies"),
                        "link": p.get("link"),
                        "status": p.get("status"),
                        "visibility": p.get("visibility", "Private")
                    }).execute()
                    count += 1
                    
                    # Inspirations
                    inspirations = p.get("inspirations", [])
                    for i_id in inspirations:
                        try:
                            supabase.table("project_inspirations").upsert({
                                "project_id": p_id,
                                "student_id": i_id
                            }).execute()
                            insp_count += 1
                        except Exception:
                            pass
                except Exception as e:
                    print(f"Error migrating project for {student_id}: {e}")
        print(f"Migrated {count} projects and {insp_count} inspirations.")

    # 5. Migrate Notifications
    notifs_file = os.path.join(base_dir, "notifications.json")
    if os.path.exists(notifs_file):
        with open(notifs_file, "r") as f:
            notifs_data = json.load(f)
            
        count = 0
        for recipient_id, notifs in notifs_data.items():
            for n in notifs:
                try:
                    supabase.table("notifications").upsert({
                        "id": n.get("id", str(uuid.uuid4())),
                        "recipient_id": recipient_id,
                        "project_id": n.get("project_id"),
                        "owner_id": n.get("owner_id"),
                        "project_name": n.get("project_name"),
                        "message": n.get("message"),
                        "timestamp": n.get("timestamp"),
                        "is_read": n.get("read", False)
                    }).execute()
                    count += 1
                except Exception as e:
                    print(f"Error migrating notification for {recipient_id}: {e}")
        print(f"Migrated {count} notifications.")
        
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
