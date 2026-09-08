import streamlit as st
import pandas as pd
from data import load_students_df, save_students_df

def render_admin_students():
    st.markdown("## 👥 Student Academic Data")
    st.markdown("Search and manage student academic records.")
    
    df = load_students_df()
    
    search_query = st.text_input("Search by Student ID or Name:")
    
    if search_query:
        mask = df["student_id"].str.contains(search_query, case=False) | df["name"].str.contains(search_query, case=False)
        display_df = df[mask]
    else:
        display_df = df
        
    st.dataframe(display_df, use_container_width=True)
    
    st.markdown("### 📝 Edit Academic Data")
    student_to_edit = st.selectbox("Select Student to Edit", options=display_df["student_id"].tolist())
    
    if student_to_edit:
        student_data = df[df["student_id"] == student_to_edit].iloc[0]
        
        with st.form("edit_student_form"):
            st.write(f"Editing data for: {student_data['name']} ({student_to_edit})")
            
            attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=float(student_data["attendance"]))
            study_hours = st.number_input("Study Hours/Day", min_value=0.0, max_value=24.0, value=float(student_data["study_hours"]))
            assignment_marks = st.number_input("Assignment Marks (0-10)", min_value=0.0, max_value=10.0, value=float(student_data["assignment_marks"]))
            internal_marks = st.number_input("Internal Marks (0-50)", min_value=0.0, max_value=50.0, value=float(student_data["internal_marks"]))
            previous_marks = st.number_input("Previous Marks (0-100)", min_value=0.0, max_value=100.0, value=float(student_data["previous_marks"]))
            
            performance_level = st.selectbox("Performance Level", 
                                             options=["Excellent", "Good", "Average", "Needs Improvement"], 
                                             index=["Excellent", "Good", "Average", "Needs Improvement"].index(student_data["performance_level"]))
                                             
            submit = st.form_submit_button("Save Changes")
            
            if submit:
                # Update DataFrame
                idx = df[df["student_id"] == student_to_edit].index[0]
                df.at[idx, "attendance"] = attendance
                df.at[idx, "study_hours"] = study_hours
                df.at[idx, "assignment_marks"] = assignment_marks
                df.at[idx, "internal_marks"] = internal_marks
                df.at[idx, "previous_marks"] = previous_marks
                df.at[idx, "performance_level"] = performance_level
                
                # Save
                save_students_df(df)
                st.success(f"Academic data updated for {student_to_edit}.")
                st.rerun()
