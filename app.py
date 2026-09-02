import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# --- PAGE SETUP ---
st.set_page_config(page_title="Daily Construction Report", layout="wide", page_icon="🏗️")
st.title("🏗️ Construction Daily Report Generator")
st.markdown("Fill out the form below to generate a professional 2-page PDF report matching your design.")

# --- THE FORM ---
with st.form("report_form"):
    st.subheader("1. Project Information")
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name", "Riverside Office Tower")
        report_no = st.text_input("Report Number", "047")
    with col2:
        report_date = st.date_input("Report Date")
        prepared_by = st.text_input("Prepared By", "John Smith - Site Supervisor")
    
    st.subheader("2. Manpower Cards Data")
    col1, col2, col3, col4 = st.columns(4)
    with col1: apex_manpower = st.number_input("Apex Manpower", value=28)
    with col2: total_manpower = st.number_input("Total Site Manpower", value=142)
    with col3: subs_present = st.number_input("Subcontractors Present", value=7)
    with col4: dyno_manpower = st.number_input("Dyno Manpower", value=15)
    progress = st.number_input("Project Progress (%)", value=61)

    st.subheader("3. Subcontractor Site Log")
    st.caption("Format: Company | Trade | Headcount | Time | Work Description (One per line)")
    sub_log = st.text_area("Subcontractor Log", "Apex Concrete | Structural | 28 | 07:00-17:00 | Foundation pour Grid A\nDyno Electrical | MEP | 15 | 07:00-17:00 | Cable tray installation\nApex Concrete | Structural | 12 | 07:00-17:00 | Cable tray installation")

    st.subheader("4. Critical Issues & Hold Points")
    st.caption("Format: Issue Description | Priority (High/Medium/Low)")
    issues = st.text_area("Issues", "Rebar inspection delayed due to rain | High\nMaterial delivery (steel) delayed | High\nBFI #104 pending review | Medium")
    issues_resolved = st.number_input("Issues Resolved Count", value=3)

    st.subheader("5. Materials & Equipment")
    st.caption("Format: Item | Quantity/Status")
    materials = st.text_area("Materials Received", "Rebar | 1 tons\nConcrete | 2 cubic meters\nConcrete | 2 cubic meters")
    equipment = st.text_area("Equipment Utilization", "Crane | 1 hours\nExcavator | 2 issues\nPoenzer | 1 issues")

    st.subheader("6. Safety Report Summary")
    safety = st.text_area("Safety Checks", "Safety Check for sewing recident.\nSafety Check on tiars and umress.\nSafety Check for nahline pasidents.")

    st.subheader("7. Site Photos")
    photos = st.file_uploader("Upload Site Photos (Up to 15 total)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    submitted = st.form_submit_button("Generate 2-Page PDF Report", type="primary")

# --- PDF GENERATION LOGIC ---
if submitted:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False) # We will manually handle pages
    
    # Helper function to parse text area into list
    def parse_lines(text):
        return [line.strip() for line in text.split('\n') if line.strip()]

    # Helper to draw a card
    def draw_card(x, y, w, h, title, subtitle, value, footer, bg_color, text_color=(0,0,0)):
        pdf.set_fill_color(*bg_color)
        pdf.rect(x, y, w, h, 'F')
        pdf.set_xy(x+2, y+2)
        pdf.set_font("Helvetica", "B", 7)
        pdf.set_text_color(*text_color)
        pdf.cell(w-4, 4, title)
        if subtitle:
            pdf.set_xy(x+2, y+7)
            pdf.set_font("Helvetica", "", 6)
            pdf.cell(w-4, 3, subtitle)
        pdf.set_xy(x+2, y+12)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(w-4, 8, str(value))
        if footer:
            pdf.set_xy(x+2, y+h-8)
            pdf.set_font("Helvetica", "", 6)
            pdf.cell(w-4, 4, footer)

    # ================= PAGE 1 =================
    pdf.add_page()
    
    # 1. Header
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 150, 0) # Green for logo approximation
    pdf.cell(10, 10, "/\\") # Simple triangle
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(40, 10, "ATLASSIAN")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 10, f"ABC Construction - Daily Site Report", align="R", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Daily Site Report", ln=True)
    pdf.ln(5)

    # 2. Manpower Cards (5 Cards)
    card_y = pdf.get_y()
    card_h = 25
    draw_card(10, card_y, 36, card_h, "Manpower - Apex", "Manpower: Apex Concrete", str(apex_manpower), "Next: Concrete Pour", (76, 175, 80), (255,255,255))
    draw_card(50, card_y, 36, card_h, "Total Site Manpower", "", str(total_manpower), "", (245, 245, 245))
    draw_card(90, card_y, 36, card_h, "Subcontractors Present", "", str(subs_present), "", (245, 245, 245))
    draw_card(130, card_y, 36, card_h, "Manpower - Dyno", "Manpower: Dyno", str(dyno_manpower), "Dyno Electrical", (245, 245, 245))
    
    # Progress Card (Approximated)
    pdf.set_fill_color(245, 245, 245)
    pdf.rect(170, card_y, 30, card_h, 'F')
    pdf.set_xy(172, card_y+2)
    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(26, 4, "Project Progress")
    pdf.set_xy(172, card_y+8)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(26, 8, f"{progress}%")
    pdf.set_xy(172, card_y+18)
    pdf.set_font("Helvetica", "", 6)
    pdf.cell(26, 4, "Daily Progress")
    
    pdf.set_y(card_y + card_h + 5)

    # 3. Subcontractor Site Log Table
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Subcontractor Manpower and Site Log", ln=True)
    pdf.ln(2)
    
    # Table Header
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(40, 6, "Subcontractor", border=1, fill=True)
    pdf.cell(30, 6, "Trade", border=1, fill=True)
    pdf.cell(20, 6, "Headcount", border=1, fill=True)
    pdf.cell(30, 6, "Start/End Time", border=1, fill=True)
    pdf.cell(70, 6, "Work Description", border=1, ln=True, fill=True)
    
    # Table Rows
    pdf.set_font("Helvetica", "", 8)
    sub_lines = parse_lines(sub_log)
    for line in sub_lines:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 5:
            pdf.cell(40, 6, parts[0], border=1)
            pdf.cell(30, 6, parts[1], border=1)
            pdf.cell(20, 6, parts[2], border=1)
            pdf.cell(30, 6, parts[3], border=1)
            pdf.cell(70, 6, parts[4], border=1, ln=True)

    pdf.ln(5)

    # 4. Critical Issues
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Critical Site Issues & Hold Points", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, f"Issues Resolved: {issues_resolved}", ln=True, align="R")
    pdf.ln(2)
    
    # Priority Bar
    pdf.set_fill_color(255, 0, 0)
    pdf.rect(10, pdf.get_y(), 30, 3, 'F')
    pdf.set_fill_color(255, 165, 0)
    pdf.rect(40, pdf.get_y(), 30, 3, 'F')
    pdf.set_fill_color(0, 0, 255)
    pdf.rect(70, pdf.get_y(), 30, 3, 'F')
    pdf.set_xy(105, pdf.get_y()-3)
    pdf.set_font("Helvetica", "", 7)
    pdf.cell(20, 6, "Priority")
    pdf.ln(5)

    # Issue Boxes (3 boxes side by side)
    issue_lines = parse_lines(issues)
    box_w = 60
    box_h = 25
    start_x = 10
    current_y = pdf.get_y()
    
    for i, line in enumerate(issue_lines[:3]):
        parts = [p.strip() for p in line.split('|')]
        desc = parts[0]
        priority = parts[1] if len(parts) > 1 else "Medium"
        
        x_pos = start_x + (i * (box_w + 5))
        pdf.set_fill_color(245, 245, 245)
        pdf.rect(x_pos, current_y, box_w, box_h, 'F')
        
        pdf.set_xy(x_pos+2, current_y+2)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(box_w-4, 4, f"Issue {i+1}: {desc[:20]}...")
        
        pdf.set_xy(x_pos+2, current_y+10)
        pdf.set_font("Helvetica", "", 7)
        pdf.multi_cell(box_w-4, 3, desc)
        
        pdf.set_xy(x_pos+2, current_y+box_h-6)
        pdf.set_font("Helvetica", "B", 7)
        color = (255, 0, 0) if priority.lower() == 'high' else (255, 165, 0)
        pdf.set_text_color(*color)
        pdf.cell(box_w-4, 4, f"Priority: {priority}")
        pdf.set_text_color(0, 0, 0)
        
    pdf.set_y(current_y + box_h + 5)

    # 5. Daily Site Photos (Page 1 - 5 photos)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Daily Site Photos & Descriptions", ln=True)
    pdf.ln(2)
    
    if photos:
        pdf.set_font("Helvetica", "", 7)
        photo_w = 35
        photo_h = 25
        for i, photo in enumerate(photos[:5]):
            try:
                img = Image.open(photo)
                img = img.resize((100, 70), Image.Resampling.LANCZOS)
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                img_byte_arr.seek(0)
                
                x_pos = 10 + (i * (photo_w + 5))
                pdf.image(img_byte_arr, x=x_pos, y=pdf.get_y(), w=photo_w, h=photo_h)
                pdf.set_xy(x_pos, pdf.get_y() + photo_h + 1)
                pdf.cell(photo_w, 4, f"{i+1}. {photo.name[:15]}...", align="C")
            except: pass
        pdf.set_y(pdf.get_y() + photo_h + 10)

    # Footer Page 1
    pdf.set_y(280)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 5, f"A4 Document | Construction Daily Report | Date: {report_date.strftime('%B %d, %Y')}", align="C")
    pdf.cell(0, 5, "Page 1/1", align="R", ln=True)


    # ================= PAGE 2 =================
    pdf.add_page()
    
    # Header Page 2
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 150, 0)
    pdf.cell(10, 10, "/\\")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(40, 10, "ATLASSIAN")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 10, f"ABC Construction - Daily Site Report", align="R", ln=True)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 10, "Page 2/2", align="R", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Daily Site Report", ln=True)
    pdf.ln(5)

    # 1. Additional Photos (Grid 2x5)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "ADDITIONAL SITE PHOTOS & FIELD OBSERVATIONS", ln=True)
    pdf.ln(2)
    
    if photos and len(photos) > 5:
        pdf.set_font("Helvetica", "", 7)
        photo_w = 35
        photo_h = 25
        for i, photo in enumerate(photos[5:15]): # Next 10 photos
            try:
                img = Image.open(photo)
                img = img.resize((100, 70), Image.Resampling.LANCZOS)
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                img_byte_arr.seek(0)
                
                col = i % 5
                row = i // 5
                x_pos = 10 + (col * (photo_w + 5))
                y_pos = pdf.get_y() + (row * (photo_h + 8))
                
                pdf.image(img_byte_arr, x=x_pos, y=y_pos, w=photo_w, h=photo_h)
                pdf.set_xy(x_pos, y_pos + photo_h + 1)
                pdf.cell(photo_w, 4, f"{i+6}. {photo.name[:10]}...", align="C")
            except: pass
        pdf.set_y(pdf.get_y() + (2 * (photo_h + 8)) + 5)
    else:
        pdf.set_y(pdf.get_y() + 10)

    # 2. Bottom Section: Two Columns
    col_y = pdf.get_y()
    
    # LEFT COLUMN: Materials & Equipment
    pdf.set_x(10)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(90, 8, "MATERIALS & EQUIPMENT STATUS", ln=True)
    pdf.ln(2)
    
    # Materials Table
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(45, 6, "Major Materials Received", border=1, fill=True)
    pdf.cell(45, 6, "Received", border=1, ln=True, fill=True)
    
    pdf.set_font("Helvetica", "", 8)
    mat_lines = parse_lines(materials)
    for line in mat_lines:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 2:
            pdf.cell(45, 6, parts[0], border=1)
            pdf.cell(45, 6, parts[1], border=1, ln=True)
            
    pdf.ln(5)
    
    # Equipment Table
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(45, 6, "Key Equipment Utilization", border=1, fill=True)
    pdf.cell(45, 6, "Utilization", border=1, ln=True, fill=True)
    
    pdf.set_font("Helvetica", "", 8)
    eq_lines = parse_lines(equipment)
    for line in eq_lines:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 2:
            pdf.cell(45, 6, parts[0], border=1)
            pdf.cell(45, 6, parts[1], border=1, ln=True)

    # RIGHT COLUMN: Safety Report
    pdf.set_xy(105, col_y)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(95, 8, "SAFETY REPORT SUMMARY", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(95, 6, "Safety Check Summary", border=1, fill=True, ln=True)
    
    pdf.set_font("Helvetica", "", 8)
    safety_lines = parse_lines(safety)
    for line in safety_lines:
        pdf.cell(5, 6, ">")
        pdf.cell(90, 6, line, ln=True)

    # Footer Page 2
    pdf.set_y(280)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 5, f"A4 Document | Construction Daily Report | Date: {report_date.strftime('%B %d, %Y')}", align="C")
    pdf.cell(0, 5, "Page 2/2", align="R", ln=True)

    # SAVE AND DOWNLOAD
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    
    st.session_state["pdf_bytes"] = pdf_buffer.getvalue()
    st.session_state["pdf_name"] = f"Daily_Report_{project_name}_{report_date}.pdf"

# --- SHOW DOWNLOAD BUTTON ---
if "pdf_bytes" in st.session_state:
    st.success("✅ 2-Page PDF Generated Successfully!")
    st.download_button(
        label="Download Your PDF Report",
        data=st.session_state["pdf_bytes"],
        file_name=st.session_state["pdf_name"],
        mime="application/pdf",
        type="primary"
    )
