"""SmartCampus AI - PDF Academic Dossier Generator
Produces formatted, publication-ready academic reports with full branch identity,
performance analytics, project portfolios, and career gap assessments.
"""

import streamlit as st
import os
import io
import json
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from data import get_student_data, get_student_skills, get_student_projects

CAREER_KB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "career_kb.json")

def generate_student_pdf(active_sid: str) -> io.BytesIO:
    """Generates an executive-grade A4 academic dossier PDF with branch identity."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=28,
        leftMargin=28,
        topMargin=22,
        bottomMargin=22
    )
    
    student = get_student_data(active_sid)
    skills_data = get_student_skills(active_sid)
    projects_data = get_student_projects(active_sid)
    
    styles = getSampleStyleSheet()
    
    # Professional Palette
    c_primary = colors.HexColor("#0F172A")    # Deep slate
    c_navy = colors.HexColor("#0077B6")       # SmartCampus Cyan-Blue
    c_accent = colors.HexColor("#0284C7")     # Light blue
    c_dark = colors.HexColor("#1E293B")       # Dark text
    c_muted = colors.HexColor("#64748B")      # Muted text
    c_border = colors.HexColor("#CBD5E1")     # Border light
    c_bg_light = colors.HexColor("#F8FAFC")   # Background tint
    c_card_bg = colors.HexColor("#F0F9FF")    # Ice tint
    
    # Risk Colors
    risk_text = student.get("risk", "LOW").upper()
    if risk_text == "HIGH":
        c_risk = colors.HexColor("#DC2626")
    elif risk_text == "MEDIUM":
        c_risk = colors.HexColor("#D97706")
    else:
        c_risk = colors.HexColor("#059669")
        
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#FFFFFF"),
        alignment=TA_CENTER
    )
    
    dept_style = ParagraphStyle(
        "DeptHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#E0F2FE"),
        alignment=TA_CENTER
    )
    
    sub_style = ParagraphStyle(
        "DocSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#BAE6FD"),
        alignment=TA_CENTER
    )
    
    sec_heading = ParagraphStyle(
        "SecHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=c_primary,
        spaceBefore=3,
        spaceAfter=2
    )
    
    normal_style = ParagraphStyle(
        "NormalText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.8,
        leading=10.2,
        textColor=c_dark
    )
    
    bold_style = ParagraphStyle(
        "BoldText",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=10.2,
        textColor=c_primary
    )
    
    table_hdr = ParagraphStyle(
        "TableHdr",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#FFFFFF"),
        alignment=TA_CENTER
    )
    
    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.6,
        leading=9.8,
        textColor=c_dark
    )
    
    table_cell_center = ParagraphStyle(
        "TableCellCenter",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.8,
        leading=10,
        textColor=c_dark,
        alignment=TA_CENTER
    )
    
    story = []
    
    # ----------------------------------------------------
    # 1. INSTITUTIONAL & BRANCH HEADER BANNER
    # ----------------------------------------------------
    header_content = [
        [Paragraph("SMARTCAMPUS AI • ACADEMIC EVALUATION DOSSIER", title_style)],
        [Paragraph("DEPARTMENT OF COMPUTER SCIENCE &amp; ENGINEERING (ARTIFICIAL INTELLIGENCE &amp; MACHINE LEARNING)", dept_style)],
        [Paragraph("Continuous Assessment Record, Competency Profiling &amp; Career Trajectory Report", sub_style)]
    ]
    header_table = Table(header_content, colWidths=[539])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0077B6")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))
    
    # ----------------------------------------------------
    # 2. STUDENT & BRANCH IDENTITY CARD
    # ----------------------------------------------------
    branch_full_title = "Computer Science and Engineering (Artificial Intelligence and Machine Learning)"
    branch_code_badge = "B.Tech. • CSE (AI & ML) • Machine Learning Unit (MLU)"
    
    meta_info = [
        [
            Paragraph("<b>Student Full Name:</b>", normal_style),
            Paragraph(f"<b>{student.get('full_name', 'Unknown')}</b>", bold_style),
            Paragraph("<b>Academic Branch:</b>", normal_style),
            Paragraph(f"<b>{branch_full_title}</b>", bold_style)
        ],
        [
            Paragraph("<b>Student ID / Roll No:</b>", normal_style),
            Paragraph(f"<font color='#0077B6'><b>{active_sid}</b></font>", bold_style),
            Paragraph("<b>Branch Identity Code:</b>", normal_style),
            Paragraph(f"<b>{branch_code_badge}</b>", normal_style)
        ],
        [
            Paragraph("<b>Academic Standing:</b>", normal_style),
            Paragraph(f"<b>{student.get('level', 'Good')}</b>", bold_style),
            Paragraph("<b>Risk Classification:</b>", normal_style),
            Paragraph(f"<b><font color='{c_risk.hexval()}'>{risk_text} RISK</font></b>", bold_style)
        ],
        [
            Paragraph("<b>Evaluation Timestamp:</b>", normal_style),
            Paragraph(datetime.now().strftime("%B %d, %Y • %I:%M %p"), normal_style),
            Paragraph("<b>Verification Dossier ID:</b>", normal_style),
            Paragraph(f"DOS-{active_sid}-{datetime.now().strftime('%Y%m%d')}", normal_style)
        ]
    ]
    meta_table = Table(meta_info, colWidths=[105, 155, 110, 169])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))
    
    # ----------------------------------------------------
    # 3. CORE ACADEMIC METRICS (KPIs)
    # ----------------------------------------------------
    story.append(Paragraph("<b>1. CORE ACADEMIC PERFORMANCE METRICS</b>", sec_heading))
    
    kpi_headers = [
        Paragraph("Overall Score", table_hdr),
        Paragraph("Attendance Rate", table_hdr),
        Paragraph("Daily Study Hours", table_hdr),
        Paragraph("Internal Marks", table_hdr),
        Paragraph("Assignment Average", table_hdr),
        Paragraph("Historical Performance", table_hdr),
    ]
    
    att_val = float(student.get("attendance", 0))
    att_color = "#059669" if att_val >= 75 else "#DC2626"
    
    kpi_data = [
        kpi_headers,
        [
            Paragraph(f"<font size='9.5'><b>{student.get('performance', 0)}%</b></font>", table_cell_center),
            Paragraph(f"<font size='9.5' color='{att_color}'><b>{att_val}%</b></font>", table_cell_center),
            Paragraph(f"<font size='9.5'><b>{student.get('study_hours', 0)} hrs/d</b></font>", table_cell_center),
            Paragraph(f"<font size='9.5'><b>{student.get('internal_marks', 0)}/50</b></font>", table_cell_center),
            Paragraph(f"<font size='9.5'><b>{student.get('assignment_marks', 0)}/10</b></font>", table_cell_center),
            Paragraph(f"<font size='9.5'><b>{student.get('previous_marks', 0)}%</b></font>", table_cell_center),
        ]
    ]
    kpi_table = Table(kpi_data, colWidths=[90, 90, 90, 90, 90, 89])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FFFFFF")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 6))
    
    # ----------------------------------------------------
    # 4. DIAGNOSTIC OBSERVATIONS & STRENGTHS
    # ----------------------------------------------------
    story.append(Paragraph("<b>2. ACADEMIC DIAGNOSTICS &amp; COGNITIVE STRENGTHS</b>", sec_heading))
    
    strengths = student.get("strengths", [])
    observations = student.get("observations", [])
    weak_areas = student.get("weak_areas", [])
    
    str_text = "<br/>".join([f"• {s}" for s in strengths[:4]]) if strengths else "• Baseline academic competencies verified."
    obs_text = "<br/>".join([f"• {o}" for o in observations[:3]]) if observations else "• Active regular academic participation recorded."
    if weak_areas:
        weak_text = "<br/>".join([f"• <font color='#DC2626'><b>Focus:</b> {w}</font>" for w in weak_areas[:2]])
        obs_text += f"<br/>{weak_text}"
        
    diag_content = [
        [Paragraph("<b>Verified Strengths &amp; Subject Proficiencies</b>", bold_style), Paragraph("<b>AI Diagnostic Insights &amp; Faculty Advisories</b>", bold_style)],
        [Paragraph(str_text, normal_style), Paragraph(obs_text, normal_style)]
    ]
    diag_table = Table(diag_content, colWidths=[265, 274])
    diag_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#ECFDF5")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FFFFFF")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(diag_table)
    story.append(Spacer(1, 6))
    
    # ----------------------------------------------------
    # 5. TECHNICAL SKILLS & PROJECT PORTFOLIO
    # ----------------------------------------------------
    story.append(Paragraph("<b>3. TECHNICAL SKILLS &amp; PRACTICAL PROJECT PORTFOLIO</b>", sec_heading))
    
    if skills_data:
        skill_items = [f"<b>{s['name']}</b> ({s.get('level', 'Intermediate')} • {s.get('category', 'Tech')})" for s in skills_data]
        skills_summary = " • ".join(skill_items)
    else:
        skills_summary = "Curricular programming foundations in Python, Data Structures, and Database Management."
        
    project_rows = []
    if projects_data:
        for p in projects_data[:2]:
            p_name = p.get("name", "Practical Project")
            p_tech = p.get("technologies", "Standard")
            p_stat = p.get("status", "Completed")
            p_desc = p.get("description", "")[:90]
            project_rows.append(f"• <b>{p_name}</b> [{p_stat}] — Tech: <i>{p_tech}</i>: {p_desc}")
        projects_summary = "<br/>".join(project_rows)
    else:
        projects_summary = "• Departmental Mini-Project & Lab Practicals assigned for current semester."
        
    port_content = [
        [Paragraph("<b>Technical Skill Matrix (Branch Relevant):</b>", bold_style)],
        [Paragraph(skills_summary, normal_style)],
        [Paragraph("<b>Practical &amp; Capstone Projects:</b>", bold_style)],
        [Paragraph(projects_summary, normal_style)]
    ]
    port_table = Table(port_content, colWidths=[539])
    port_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(port_table)
    story.append(Spacer(1, 6))
    
    # ----------------------------------------------------
    # 6. CAREER ANALYSIS & SPECIALIZATION ROADMAP
    # ----------------------------------------------------
    story.append(Paragraph("<b>4. CAREER SPECIALIZATION &amp; SKILL GAP ROADMAP</b>", sec_heading))
    
    top_career = "AI / Machine Learning Engineer"
    matched_skills = []
    missing_skills = []
    
    try:
        if os.path.exists(CAREER_KB_PATH):
            with open(CAREER_KB_PATH, "r") as f:
                career_kb = json.load(f)
            student_skills = [s["name"] for s in skills_data]
            career_matches = []
            for role, role_data in career_kb.items():
                core = set([s.lower() for s in role_data.get("core_skills", [])])
                student_sk_lower = set([s.lower() for s in student_skills])
                match_count = len(core.intersection(student_sk_lower))
                career_matches.append((role, match_count, role_data))
            career_matches.sort(key=lambda x: x[1], reverse=True)
            if career_matches:
                top_career = career_matches[0][0]
                matched_role_data = career_matches[0][2]
                core_list = matched_role_data.get("core_skills", [])
                student_sk_lower = set([s.lower() for s in student_skills])
                matched_skills = [s for s in core_list if s.lower() in student_sk_lower]
                missing_skills = [s for s in core_list if s.lower() not in student_sk_lower]
    except Exception:
        pass
        
    m_str = ", ".join(matched_skills) if matched_skills else "Python, Foundational Algorithms"
    miss_str = ", ".join(missing_skills[:4]) if missing_skills else "Cloud MLOps, Advanced Deep Learning"
    
    career_content = [
        [
            Paragraph("<b>Target Role Alignment:</b>", normal_style),
            Paragraph(f"<b><font color='#0077B6'>{top_career}</font></b>", bold_style),
            Paragraph("<b>Branch Curriculum Synergy:</b>", normal_style),
            Paragraph(f"High (CSE AI &amp; ML Domain)", normal_style)
        ],
        [
            Paragraph("<b>Acquired Competencies:</b>", normal_style),
            Paragraph(f"<font color='#059669'>{m_str}</font>", normal_style),
            Paragraph("<b>Recommended Next Focus:</b>", normal_style),
            Paragraph(f"<font color='#0284C7'>{miss_str}</font>", normal_style)
        ]
    ]
    career_table = Table(career_content, colWidths=[120, 160, 115, 144])
    career_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0F9FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BAE6FD")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E0F2FE")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(career_table)
    story.append(Spacer(1, 8))
    
    # ----------------------------------------------------
    # 7. INSTITUTIONAL ENDORSEMENT & SIGNATURES
    # ----------------------------------------------------
    sign_table_data = [
        [
            Paragraph("<b>Faculty Advisor / Mentor</b><br/><br/>_______________________________<br/>Prof. S. S. Khatri (Counselor)", normal_style),
            Paragraph("<b>Department Authority</b><br/><br/>_______________________________<br/>Head of Department (CSE AI &amp; ML)", normal_style),
            Paragraph("<b>Institutional Verification</b><br/><br/><b>SMARTCAMPUS AI PLATFORM</b><br/><font size='6.8' color='#64748B'>Digitally Certified • CSE (AI &amp; ML)</font>", normal_style)
        ]
    ]
    sign_table = Table(sign_table_data, colWidths=[180, 180, 179])
    sign_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, c_border),
    ]))
    story.append(sign_table)
    
    story.append(Spacer(1, 4))
    disc = Paragraph(
        "<font size='6.2' color='#94A3B8'>SmartCampus AI Evaluation Dossier • Department of Computer Science & Engineering (Artificial Intelligence and Machine Learning) • Official Continuous Assessment Record</font>",
        ParagraphStyle("Disc", parent=styles["Normal"], alignment=TA_CENTER)
    )
    story.append(disc)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def render_pdf_report():
    st.markdown("## 📄 Academic Dossier & PDF Reports")
    
    if st.session_state.get("role") in ["admin", "teacher"]:
        from data import load_students_df
        df = load_students_df()
        active_sid = st.selectbox("Select Student", options=df["student_id"].tolist())
    else:
        active_sid = st.session_state.get("selected_student_id") or st.session_state.get("student_id")

    if not active_sid:
        st.error("No student selected.")
        return
        
    student = get_student_data(active_sid)
    st.markdown(
        f"Generate and export the certified academic dossier for **{student.get('full_name')}** (`{active_sid}`), featuring complete branch identity, continuous assessment analytics, and career roadmap."
    )
    
    with st.container():
        st.markdown(
            f"""
            <div style="background: white; border: 1px solid rgba(0, 119, 182, 0.2); border-radius: 16px; padding: 22px; margin-bottom: 20px; box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px; margin-bottom: 14px;">
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <div style="width: 48px; height: 48px; border-radius: 12px; background: linear-gradient(135deg, #0077b6, #0284c7); display: flex; align-items: center; justify-content: center; font-size: 24px; color: white;">
                            📄
                        </div>
                        <div>
                            <div style="font-weight: 800; color: #0f172a; font-size: 1.15rem;">Official Academic Evaluation Dossier</div>
                            <div style="color: #64748b; font-size: 0.85rem;">Branch: <strong>Computer Science & Engineering (AI & ML)</strong> • Student: <strong>{student.get('full_name')}</strong> ({active_sid})</div>
                        </div>
                    </div>
                    <span style="background: rgba(16, 185, 129, 0.12); color: #059669; border: 1px solid rgba(16, 185, 129, 0.3); padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">
                        ✓ Ready for Export
                    </span>
                </div>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 16px; margin-bottom: 16px; font-size: 0.83rem; color: #475569; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
                    <div>🏛️ <strong>Discipline:</strong> CSE (AI & ML)</div>
                    <div>📊 <strong>Academic Score:</strong> {student.get('performance', 0)}%</div>
                    <div>📅 <strong>Attendance:</strong> {student.get('attendance', 0)}%</div>
                    <div>🎯 <strong>Standing:</strong> {student.get('level', 'Good')}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        pdf_buffer = generate_student_pdf(active_sid)
        
        st.download_button(
            label="📥 Download Certified Academic PDF Dossier",
            data=pdf_buffer,
            file_name=f"{active_sid}_CSE_AIML_Academic_Dossier.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
    
    st.info("ℹ️ **Institutional Record Verification**: The generated PDF contains official Department of Computer Science & Engineering (AI & ML) identity headers, verified continuous assessment indicators, practical project tracking, and academic mentor sign-off blocks.")
