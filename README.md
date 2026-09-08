# SmartCampus AI – Intelligent Student Assistant

## Description
SmartCampus AI is an intelligent student learning and decision-support application built using **Python and Streamlit**. It provides academic analytics, time-blocked study scheduling, personalized recommendations, and curriculum guidance for students in Artificial Intelligence and Computer Science courses.

This application is powered by **Supabase PostgreSQL** for persistent multi-user data storage and uses **Scikit-learn Decision Trees** alongside a **Rule-Based Expert System** to deliver smart academic insights.

---

## Features
- 👥 **Multi-Role Access**: Dedicated panels for Students, Teachers, and Admins.
- 🏠 **Academic Dashboard**: High-level Academic Health Meter displaying overall index, attendance, and risk level.
- 📊 **Interactive Analytics**: Knowledge Radar and Subject Performance graphs.
- 🛠️ **Skills & Projects**: Students can manage their skills, public/private projects, and get motivated via "I'm Inspired".
- 🤖 **AI Study Companion**: Natural chat interface featuring structured explanations for algorithms.
- 📚 **Smart Study Planner**: Time-blocked revision timetable generator.
- 🎯 **Personalized Recommendations**: Priority-filtered intervention cards and Career/Skill-Gap Analysis.
- 📄 **PDF Reports**: Automated generation of comprehensive student analysis reports.

---

## Technology Stack
- **Backend & Frontend**: Python 3.10+, Streamlit
- **Database**: Supabase PostgreSQL
- **Data Manipulation**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, Joblib
- **Visualizations**: Plotly
- **PDF Generation**: ReportLab

---

## Database Architecture
The application uses Supabase PostgreSQL for persistent data. The database schema (see `database/schema.sql`) includes:
- `users`: Core authentication table with roles (admin, teacher, student).
- `students`: Profile and academic performance records.
- `skills`: Student capabilities and proficiencies.
- `projects`: Student portfolios with visibility toggles (Private/Public).
- `project_inspirations`: Tracking for the peer-motivation feature.
- `notifications`: Alerts for new public projects.
- `recommendations`: Custom guidance generated per student.

**Role Permissions**:
- **Admin**: Full access. Can manage users, students, and view global analytics.
- **Teacher**: Can manage assigned students and view their academic/project performance.
- **Student**: Isolated access. Can manage own skills/projects, toggle project visibility, and view public project feeds.

---

## Setup & Installation

### 1. Create Supabase Project
1. Create a free project at [Supabase](https://supabase.com).
2. Go to the SQL Editor and execute the contents of `database/schema.sql` to build the tables.

### 2. Configure Streamlit Secrets
Do NOT put real credentials in your code! The application uses Streamlit Secrets.
Create a `.streamlit/secrets.toml` file in the project root:

```toml
[supabase]
URL = "https://your-project-ref.supabase.co"
KEY = "your-anon-key"
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Seed Demo Data & Migrate (Optional)
If you have existing CSV/JSON demo data from the previous version, run the migration script to populate your new Supabase database:
```bash
python scripts/migrate_data.py
```

### 5. Run Application
```bash
streamlit run app.py
```

---

## Deployment to Streamlit Community Cloud
This application is fully compatible with Streamlit Community Cloud without needing Docker or a separate backend server.
1. Push this repository to GitHub.
2. Link the repository to Streamlit Community Cloud.
3. In the Streamlit Cloud dashboard, go to **App Settings > Secrets** and paste your `secrets.toml` configuration there.
4. Deploy!

---

## Future Scope (ERP Integration)
Currently, academic data is managed manually through the Admin and Teacher panels. In a future implementation, the system is designed to integrate with a college ERP through secure APIs so that attendance, internal marks, and external marks can be fetched and populated automatically into Supabase, driving real-time AI analysis.
