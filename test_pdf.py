import sys
from io import BytesIO
from pages.pdf_report import generate_pdf_report
from data import get_student_data, get_student_skills, get_student_projects
try:
    s_data = get_student_data('SC-2026-001')
    skills = get_student_skills('SC-2026-001')
    projects = get_student_projects('SC-2026-001')
    pdf_bytes = generate_pdf_report('SC-2026-001', s_data, skills, projects)
    if pdf_bytes:
        print("PDF generated successfully! Size:", len(pdf_bytes))
    else:
        print("PDF generation failed.")
except Exception as e:
    print("Error:", e)
