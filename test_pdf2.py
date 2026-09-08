from pages.pdf_report import generate_student_pdf
try:
    pdf_bytes = generate_student_pdf('SC-2026-001')
    if pdf_bytes:
        print("PDF generated successfully! Size:", len(pdf_bytes.getvalue()))
    else:
        print("PDF generation failed.")
except Exception as e:
    print("Error:", e)
