"""Seed real class student data from PRPCEM CSE (AIML) Sem-V MSE-1 Result Sheet.
Cleans up old mock data and populates:
1. Supabase cloud database
2. Local data/students.csv
3. Local data/users.json
"""

import os
import json
import random
import pandas as pd
from supabase import create_client, Client

REAL_STUDENTS_DATA = [
    {"roll": "MLU24F001", "name": "Archita Rajesh Tiwari", "q1": 10, "q2": 10, "total": 20},
    {"roll": "MLU24F002", "name": "Avani Yogesh Sawarkar", "q1": 0, "q2": 0, "total": 0},
    {"roll": "MLU24F003", "name": "Babita Manoj Zunzunwala", "q1": 10, "q2": 8, "total": 18},
    {"roll": "MLU24F004", "name": "Dhanashri Gajanan Tayade", "q1": 4, "q2": 9, "total": 13},
    {"roll": "MLU24F005", "name": "Gauri Arun Bhivagade", "q1": 10, "q2": 9, "total": 19},
    {"roll": "MLU24F006", "name": "Gayatri Santosh Pathare", "q1": 9, "q2": 8, "total": 17},
    {"roll": "MLU24F007", "name": "Gayatri Chandrashekhar Thokal", "q1": 9, "q2": 8, "total": 17},
    {"roll": "MLU24F008", "name": "Kasturi Dilip Tidke", "q1": 9, "q2": 9, "total": 18},
    {"roll": "MLU24F009", "name": "Krutika Vijay Deshmukh", "q1": 0, "q2": 0, "total": 0},
    {"roll": "MLU24F010", "name": "Manasvi Sudhir Wankhade", "q1": 7, "q2": 9, "total": 16},
    {"roll": "MLU24F011", "name": "Namrata Rajesh Pise", "q1": 10, "q2": 9, "total": 19},
    {"roll": "MLU24F012", "name": "Parul Sushil Sahu", "q1": 7, "q2": 9, "total": 16},
    {"roll": "MLU24F013", "name": "Shruti Praful Ambadkar", "q1": 6, "q2": 8, "total": 14},
    {"roll": "MLU24F014", "name": "Rani Pradip Chaudhari", "q1": 9, "q2": 9, "total": 18},
    {"roll": "MLU24F016", "name": "Sakshi Santosh Gajare", "q1": 7, "q2": 8, "total": 15},
    {"roll": "MLU24F018", "name": "Sayali Anil Banait", "q1": 10, "q2": 9, "total": 19},
    {"roll": "MLU24F019", "name": "Shreya Gajananrao Kale", "q1": 9, "q2": 9, "total": 18},
    {"roll": "MLU24F020", "name": "Shreya Pravin Kshirsagar", "q1": 9, "q2": 10, "total": 19},
    {"roll": "MLU24F021", "name": "Sneha Gajanan Manwar", "q1": 10, "q2": 8, "total": 18},
    {"roll": "MLU24F022", "name": "Srushti Sadanand Raut", "q1": 10, "q2": 10, "total": 20},
    {"roll": "MLU24F023", "name": "Taniksha Rajendra Nagpure", "q1": 8, "q2": 10, "total": 18},
    {"roll": "MLU24F024", "name": "Tanuja Sudamdev Chalge", "q1": 9, "q2": 9, "total": 18},
    {"roll": "MLU24F026", "name": "Utkarsha Rajkumar Gedam", "q1": 10, "q2": 8, "total": 18},
    {"roll": "MLU24F027", "name": "Utkarsha Prakash Mahulkar", "q1": 10, "q2": 10, "total": 20},
    {"roll": "MLU24F028", "name": "Vaishnavi Sanjay Ganjiwale", "q1": 6, "q2": 9, "total": 15},
    {"roll": "MLU24F029", "name": "Yashashri Santosh Kawalkar", "q1": 10, "q2": 10, "total": 20},
    {"roll": "MLU24F030", "name": "Aaradhay Nandu Kalmegh", "q1": 10, "q2": 8, "total": 18},
    {"roll": "MLU24F032", "name": "Aditya Bharat Jaybhaye", "q1": 10, "q2": 8, "total": 18},
    {"roll": "MLU24F033", "name": "Aditya Pramod Kakade", "q1": 10, "q2": 8, "total": 18},
    {"roll": "MLU24F034", "name": "Aditya Santosh Kandalkar", "q1": 1, "q2": 9, "total": 10},
    {"roll": "MLU24F035", "name": "Ali Shaban Zafar Ali", "q1": 7, "q2": 9, "total": 16},
    {"roll": "MLU24F036", "name": "Atharva Sureshkumar Rathor", "q1": 0, "q2": 0, "total": 0},
    {"roll": "MLU24F037", "name": "Atharva Vinodrao Sisat", "q1": 10, "q2": 10, "total": 20},
    {"roll": "MLU24F038", "name": "Ayush Navneetrao Nimbhorkar", "q1": 4, "q2": 9, "total": 13},
    {"roll": "MLU24F039", "name": "Bhushan Umesh Darne", "q1": 4, "q2": 7, "total": 11},
    {"roll": "MLU24F040", "name": "Devashish Ganesh Deshmukh", "q1": 6, "q2": 9, "total": 15},
    {"roll": "MLU24F041", "name": "Gitesh Ajitkumar Mishra", "q1": 8, "q2": 9, "total": 17},
    {"roll": "MLU24F042", "name": "Harshal Khushal Dahake", "q1": 0, "q2": 0, "total": 0},
    {"roll": "MLU24F043", "name": "Jeet Sunil Arjune", "q1": 8, "q2": 8, "total": 16},
    {"roll": "MLU24F044", "name": "Ketan Dharmesh Awachar", "q1": 8, "q2": 9, "total": 17},
    {"roll": "MLU24F045", "name": "Ketan Sunil Raut", "q1": 10, "q2": 10, "total": 20},
    {"roll": "MLU24F046", "name": "Krishna Ghanshyam Lekurwale", "q1": 8, "q2": 8, "total": 16},
    {"roll": "MLU24F047", "name": "Lalit Rajesh Bhade", "q1": 9, "q2": 10, "total": 19},
    {"roll": "MLU24F048", "name": "Maaz Hashir Mohammad Irshad", "q1": 8, "q2": 10, "total": 18},
    {"roll": "MLU24F049", "name": "Mohd. Sufiyan M. Riyaz Gigani", "q1": 8, "q2": 10, "total": 18},
    {"roll": "MLU24F050", "name": "Omkar Pradumna Bhakare", "q1": 7, "q2": 8, "total": 15},
    {"roll": "MLU24F051", "name": "Piyush Rajendra Jamodkar", "q1": 6, "q2": 8, "total": 14},
    {"roll": "MLU24F052", "name": "Piyush Umesh Uke", "q1": 2, "q2": 2, "total": 4},
    {"roll": "MLU24F053", "name": "Pranav Prabhakar Borkar", "q1": 7, "q2": 7, "total": 14},
    {"roll": "MLU24F054", "name": "Pranay Sharad Chandurkar", "q1": 10, "q2": 10, "total": 20},
    {"roll": "MLU24F055", "name": "Prem Baliram Dhamodkar", "q1": 8, "q2": 10, "total": 18},
    {"roll": "MLU24F056", "name": "Rushabh Anil Shambharkar", "q1": 6, "q2": 4, "total": 10},
    {"roll": "MLU24F057", "name": "Sahil Sanjay Waghmare", "q1": 6, "q2": 6, "total": 12},
    {"roll": "MLU24F058", "name": "Shamuil Mohd. Shahid Tikki", "q1": 0, "q2": 0, "total": 0},
    {"roll": "MLU24F059", "name": "Shavez Khan Azim Khan", "q1": 0, "q2": 0, "total": 0},
    {"roll": "MLU24F060", "name": "Shivraj Vishwas Adhau", "q1": 10, "q2": 9, "total": 19},
    {"roll": "MLU24F061", "name": "Siddhesh Sunil Thakare", "q1": 7, "q2": 8, "total": 15},
    {"roll": "MLU24F062", "name": "Sumit Gajanan Dubey", "q1": 10, "q2": 10, "total": 20},
    {"roll": "MLU24F063", "name": "Tanuj Sharad Thote", "q1": 8, "q2": 9, "total": 17},
    {"roll": "MLU24F064", "name": "Vaibhav Sakharam Garkar", "q1": 7, "q2": 9, "total": 16},
    {"roll": "MLU24F065", "name": "Vaibhav Mahadeo Hiradeve", "q1": 7, "q2": 3, "total": 10},
    {"roll": "MLU24F066", "name": "Vedant Jayprakash Deshmukh", "q1": 7, "q2": 10, "total": 17},
    {"roll": "MLU24F067", "name": "Vedant Devanand Jambhalikar", "q1": 7, "q2": 9, "total": 16},
    {"roll": "MLU24F068", "name": "Vishal Chunnilal Jambekar", "q1": 9, "q2": 10, "total": 19},
    {"roll": "MLU24F069", "name": "Yash Gajanan Sakharkar", "q1": 10, "q2": 10, "total": 20},
    {"roll": "MLU25S207", "name": "Apurva Anil Jawanjal", "q1": 7, "q2": 9, "total": 16},
    {"roll": "MLU25S208", "name": "Manthan Sanjay Rajas", "q1": 0, "q2": 0, "total": 0},
    {"roll": "MLU25S210", "name": "Himanshu Anil Jajoo", "q1": 10, "q2": 10, "total": 20},
    {"roll": "MLU25S211", "name": "Vansh Vasant Tarpe", "q1": 10, "q2": 10, "total": 20},
    {"roll": "MLU25S212", "name": "Manjusha Laxmikant Naik", "q1": 10, "q2": 10, "total": 20},
    {"roll": "MLU25S213", "name": "Lavanya Laxmikant Gaikwad", "q1": 10, "q2": 9, "total": 19},
    {"roll": "MLU25S214", "name": "Tarang Sunil Chavhan", "q1": 8, "q2": 9, "total": 17},
    {"roll": "MLU25S215", "name": "Tejas Sunil Padole", "q1": 10, "q2": 8, "total": 18},
    {"roll": "MLU25S216", "name": "Sumit Pradip Gajghate", "q1": 6, "q2": 9, "total": 15},
    {"roll": "MLU25S217", "name": "Atharv Rajkumar Kevatkar", "q1": 10, "q2": 9, "total": 19},
    {"roll": "MLU25S218", "name": "Sadhana Devidas Landgekar", "q1": 10, "q2": 10, "total": 20},
]

REAL_TEACHERS = [
    {"id": "NCM", "name": "Dr. N. C. Mhala", "role": "teacher", "subject": "DBMS"},
    {"id": "SSK", "name": "Prof. S. S. Khatri", "role": "teacher", "subject": "AI"},
    {"id": "API", "name": "Prof. A. P. Ingle", "role": "teacher", "subject": "OS"},
    {"id": "RAK", "name": "Prof. R. A. Kalamkar", "role": "teacher", "subject": "MAD"},
    {"id": "VBK", "name": "Dr. V. B. Kute", "role": "teacher", "subject": "DSA"},
    {"id": "ZIK", "name": "Dr. Z. I. Khan", "role": "teacher", "subject": "HOD"},
    {"id": "TCH-001", "name": "Faculty Coordinator", "role": "teacher", "subject": "Academics"},
]

def generate_student_row(item):
    roll = item["roll"]
    name = item["name"]
    total = item["total"]
    
    random.seed(roll)
    
    if total >= 18:
        perf = "Excellent"
        att = round(random.uniform(84.0, 96.0), 1)
        sh = round(random.uniform(3.8, 5.2), 1)
        am = round(random.uniform(8.5, 10.0), 1)
        im = round(min(50.0, 42.0 + (total - 18) * 3.5 + random.uniform(0.0, 2.0)), 1)
        pm = round(random.uniform(80.0, 96.0), 1)
    elif total >= 14:
        perf = "Good"
        att = round(random.uniform(76.0, 88.0), 1)
        sh = round(random.uniform(2.8, 4.0), 1)
        am = round(random.uniform(7.5, 9.0), 1)
        im = round(32.0 + (total - 14) * 2.2 + random.uniform(0.0, 2.0), 1)
        pm = round(random.uniform(68.0, 82.0), 1)
    elif total >= 10:
        perf = "Average"
        att = round(random.uniform(68.0, 80.0), 1)
        sh = round(random.uniform(2.0, 3.2), 1)
        am = round(random.uniform(6.0, 7.5), 1)
        im = round(24.0 + (total - 10) * 1.8 + random.uniform(0.0, 2.0), 1)
        pm = round(random.uniform(55.0, 70.0), 1)
    else:
        perf = "Needs Improvement"
        att = round(random.uniform(45.0, 68.0), 1)
        sh = round(random.uniform(1.0, 2.2), 1)
        am = round(random.uniform(3.0, 5.5), 1)
        im = round(max(8.0, total * 2.0 + random.uniform(2.0, 6.0)), 1)
        pm = round(random.uniform(40.0, 60.0), 1)
        
    return {
        "student_id": roll,
        "name": name,
        "attendance": att,
        "study_hours": sh,
        "assignment_marks": am,
        "internal_marks": im,
        "previous_marks": pm,
        "performance_level": perf
    }

def run_seed():
    print(f"Total real students to seed: {len(REAL_STUDENTS_DATA)}")
    
    # 1. Build DataFrame for students
    student_rows = [generate_student_row(item) for item in REAL_STUDENTS_DATA]
    students_df = pd.DataFrame(student_rows)
    
    # 2. Build users dictionary
    users_dict = {
        "admin": {"password": "admin123", "role": "admin", "name": "Administrator"}
    }
    
    for t in REAL_TEACHERS:
        users_dict[t["id"]] = {
            "password": "teacher123",
            "role": "teacher",
            "name": t["name"]
        }
        
    for s in student_rows:
        users_dict[s["student_id"]] = {
            "password": "student123",
            "role": "student",
            "name": s["name"]
        }
        
    # Save local files
    base_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    csv_path = os.path.join(base_dir, "students.csv")
    json_path = os.path.join(base_dir, "users.json")
    
    students_df.to_csv(csv_path, index=False)
    print(f"Saved local {csv_path} with {len(students_df)} real students.")
    
    with open(json_path, "w") as f:
        json.dump(users_dict, f, indent=2)
    print(f"Saved local {json_path} with {len(users_dict)} accounts.")
    
    # 3. Synchronize with Supabase Cloud DB
    import streamlit as st
    try:
        url = st.secrets["supabase"]["URL"]
        key = st.secrets["supabase"]["KEY"]
    except Exception:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        
    if not url or not key:
        print("Supabase credentials not found. Local seed only.")
        return
        
    print(f"Connecting to Supabase at {url}...")
    supabase: Client = create_client(url, key)
    
    try:
        # Delete dependent tables first
        print("Cleaning old dependent records from Supabase...")
        try: supabase.table("notifications").delete().neq("recipient_id", "KEEP_NOTHING").execute()
        except Exception as e: print("Clean notifs:", e)
        
        try: supabase.table("recommendations").delete().neq("student_id", "KEEP_NOTHING").execute()
        except Exception as e: print("Clean recs:", e)
        
        try: supabase.table("project_inspirations").delete().neq("student_id", "KEEP_NOTHING").execute()
        except Exception as e: print("Clean insp:", e)
        
        try: supabase.table("projects").delete().neq("student_id", "KEEP_NOTHING").execute()
        except Exception as e: print("Clean proj:", e)
        
        try: supabase.table("skills").delete().neq("student_id", "KEEP_NOTHING").execute()
        except Exception as e: print("Clean skills:", e)
        
        try: supabase.table("students").delete().neq("student_id", "KEEP_NOTHING").execute()
        except Exception as e: print("Clean students:", e)
        
        try: supabase.table("users").delete().neq("username", "admin").execute()
        except Exception as e: print("Clean users:", e)
        
        print("Old mock records removed successfully.")
    except Exception as e:
        print(f"Error during table clean: {e}")
        
    # Insert new users in batches
    user_records = []
    for username, uinfo in users_dict.items():
        user_records.append({
            "username": username,
            "password_hash": uinfo["password"],
            "role": uinfo["role"],
            "name": uinfo["name"]
        })
        
    print(f"Upserting {len(user_records)} users into Supabase...")
    batch_size = 50
    for i in range(0, len(user_records), batch_size):
        batch = user_records[i:i + batch_size]
        supabase.table("users").upsert(batch, on_conflict="username").execute()
    print("Users synced.")
    
    # Insert students
    student_records = student_rows
    print(f"Upserting {len(student_records)} students into Supabase...")
    for i in range(0, len(student_records), batch_size):
        batch = student_records[i:i + batch_size]
        supabase.table("students").upsert(batch).execute()
    print("Students synced.")
    
    print("\nSUCCESS: All 76 real class students from CSE (AIML) Sem-V seeded into Supabase and local data!")

if __name__ == "__main__":
    run_seed()
