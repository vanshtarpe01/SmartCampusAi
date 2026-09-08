import streamlit as st
from data import load_students_df, save_admin_recommendation, get_admin_recommendation

def render_admin_recommendations():
    st.markdown("## 🎯 Academic Recommendations")
    st.markdown("Provide advisory study recommendations to students based on their performance.")
    
    df = load_students_df()
    
    student_id = st.selectbox("Select Student", options=df["student_id"].tolist())
    
    if student_id:
        student_data = df[df["student_id"] == student_id].iloc[0]
        
        st.markdown(f"**Current Data for {student_data['name']} ({student_id})**")
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Study Hours", f"{student_data['study_hours']} hrs/day")
        col2.metric("Performance", student_data["performance_level"])
        col3.metric("Attendance", f"{student_data['attendance']}%")
        
        existing_rec = get_admin_recommendation(student_id)
        default_hours = existing_rec.get("recommended_hours", "e.g., 3-4") if existing_rec else "e.g., 3-4"
        default_weak = existing_rec.get("weak_area", "") if existing_rec else ""
        default_guidance = existing_rec.get("guidance", "") if existing_rec else ""
        
        st.markdown("### 📝 Provide Guidance")
        with st.form("admin_rec_form"):
            recommended_hours = st.text_input("Recommended Study Hours (range)", value=default_hours)
            weak_area = st.text_input("Identified Weak Area", value=default_weak, placeholder="e.g., Data Structures")
            guidance = st.text_area("Academic Guidance & Reasoning", value=default_guidance, placeholder="Provide a reason for the recommendation. Note: This is advisory only.")
            
            submit = st.form_submit_button("Save Recommendation")
            
            if submit:
                rec_data = {
                    "recommended_hours": recommended_hours,
                    "weak_area": weak_area,
                    "guidance": guidance
                }
                save_admin_recommendation(student_id, rec_data)
                st.success(f"Recommendation saved for {student_id}. They will see this on their portal.")
