import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# --- PAGE SETUP ---
st.set_page_config(page_title="Daily Construction Report", layout="wide", page_icon="🏗️")
st.title("🏗️ Construction Daily Report Generator")
st.markdown("Fill out the form below to generate a professional 2-page PDF report.")

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
    
    st.subheader("2. Manpower & Progress (For the 4 Cards)")
    col1, col2, col3, col4 = st.columns(4)
    with col1: total_manpower = st.number_input("Total Manpower", value=142)
    with col2: subs_present = st.number_input("Subcontractors Present", value=7)
    with col3: dyno_manpower = st.number_input("Dyno Manpower", value=15)
    with col4: progress = st.number_input("Progress (%)", value=61)

    st.subheader("3. Subcontractor Site Log")
    st.caption("Format: Company | Trade | Headcount | Time | Work Description (One per line)")
    sub_log = st.text_area("Subcontractor Log", "Apex Concrete | Structural | 28 | 07:00-17:00 | Foundation pour Grid A\nDyno Electrical | MEP | 15 | 07:00-17:00 | Cable tray installation")

    st.subheader("4. Critical Issues & Hold Points")
    st.caption("Format: Issue Description | Priority (High/Medium/Low)")
    issues = st.text_area("Issues", "Rebar inspection delayed | High\nMaterial delivery delayed | High")

    st.subheader("5. Materials & Equipment")
    st.caption("Format: Item | Quantity/Status")
    materials = st.text_area("Materials Received", "Rebar | 1 tons\nConcrete | 2 cubic meters")
    equipment = st.text_area("Equipment Utilization", "Crane | 1 hours\nExcavator | Active")

    st.subheader("6. Safety Report Summary")
    safety = st.text_area("Safety Checks & Incidents", "Safety Check for PPE compliance\nSafety Check on tools and harness\nNo incidents reported today.")

    st.subheader("7. Site Photos")
    photos = st.file_uploader("Upload Site Photos (Up to 15 for the grid)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    submitted = st.form_submit_button("Generate 2-Page PDF Report", type="primary")

# --- PDF GENERATION LOGIC ---
if submitted:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Helper function to draw a colored card
    def draw_card(x, y, w, h, title, value, color):
        pdf.set_fill_color(*color)
        pdf.rect(x, y, w, h, 'F')
        pdf.set_xy(x, y + 2)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(w, 5, title, align="C")
        pdf.set_xy(x, y + 8)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(w, 10, str(value), align="C")
        pdf.set_text_color(0, 0, 0)

    # Helper function to parse text area into list
    def parse_lines(text):
        return [line.strip() for line in text.split('\n') if line.strip()]

    # ================= PAGE 1 =================
    pdf.add_page()
    
    # 1. Header
    pdf.set_fill_color(25, 118, 210)
    pdf.rect(0, 0, 210, 20, 'F')
    pdf.set_y(5)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, f"ABC CONSTRUCTION - Daily Site Report: {project_name}", align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(25)

    # 2. Project Info
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(40, 6, "Project:")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(60, 6, project_name)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(30, 6, "Date:")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, report_date.strftime('%B %d, %Y'), ln=True)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(40, 6, "Prepared By:")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, prepared_by, ln=True)
    pdf.ln(5)

    # 3. Manpower Cards (4 Cards)
    draw_card(10, pdf.get_y(), 45, 20, "Total Site Manpower", total_manpower, (76, 175, 80)) # Green
    draw_card(60, pdf.get_y(), 45, 20, "Subcontractors Present", subs_present, (33, 150, 243)) # Blue
    draw_card(110, pdf.get_y(), 45, 20, "Manpower - Dyno", dyno_manpower, (158, 158, 158)) # Grey
    draw_card(160, pdf.get_y(), 45, 20, "Project Progress", f"{progress}%", (255, 152, 0)) # Orange
    pdf.set_y(pdf.get_y() + 25)

    # 4. Subcontractor Site Log Table
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(230, 240, 250)
    pdf.cell(0, 8, "  Subcontractor Manpower and Site Log", ln=True, fill=True)
    pdf.ln(2)
    
    # Table Header
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(200, 200, 200)
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

    # 5. Critical Issues
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(255, 235, 238)
    pdf.cell(0, 8, "  Critical Site Issues & Hold Points", ln=True, fill=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 9)
    issue_lines = parse_lines(issues)
    for line in issue_lines:
        parts = [p.strip() for p in line.split('|')]
        desc = parts[0]
        priority = parts[1] if len(parts) > 1 else "Medium"
        color = (255, 0, 0) if priority.lower() == 'high' else (255, 165, 0)
        pdf.set_text_color(*color)
        pdf.cell(5, 6, "●")
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 6, f" {desc} - Priority: {priority}", ln=True)
    pdf.ln(5)

    # 6. Daily Site Photos (Page 1 - 5 photos)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(230, 240, 250)
    pdf.cell(0, 8, "  Daily Site Photos & Descriptions", ln=True, fill=True)
    pdf.ln(2)
    
    if photos:
        pdf.set_font("Helvetica", "", 8)
        for i, photo in enumerate(photos[:5]):
            try:
                img = Image.open(photo)
                img = img.resize((100, 70), Image.Resampling.LANCZOS)
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                img_byte_arr.seek(0)
                
                x_pos = 10 + (i * 38)
                pdf.image(img_byte_arr, x=x_pos, y=pdf.get_y(), w=35, h=25)
                pdf.set_xy(x_pos, pdf.get_y() + 26)
                pdf.cell(35, 4, f"{i+1}. {photo.name[:15]}...", align="C")
            except: pass
        pdf.set_y(pdf.get_y() + 35)

    # ================= PAGE 2 =================
    pdf.add_page()
    
    # Header Page 2
    pdf.set_fill_color(25, 118, 210)
    pdf.rect(0, 0, 210, 20, 'F')
    pdf.set_y(5)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, f"ABC CONSTRUCTION - Daily Site Report (Page 2)", align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(25)

    # 1. Additional Photos (Grid)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(230, 240, 250)
    pdf.cell(0, 8, "  Additional Site Photos & Field Observations", ln=True, fill=True)
    pdf.ln(2)
    
    if photos and len(photos) > 5:
        pdf.set_font("Helvetica", "", 8)
        for i, photo in enumerate(photos[5:15]): # Next 10 photos
            try:
                img = Image.open(photo)
                img = img.resize((80, 60), Image.Resampling.LANCZOS)
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                img_byte_arr.seek(0)
                
                col = i % 5
                row = i // 5
                x_pos = 10 + (col * 38)
                y_pos = pdf.get_y() + (row * 25)
                
                pdf.image(img_byte_arr, x=x_pos, y=y_pos, w=35, h=20)
                pdf.set_xy(x_pos, y_pos + 21)
                pdf.cell(35, 4, f"{i+6}. {photo.name[:10]}...", align="C")
            except: pass
        pdf.set_y(pdf.get_y() + 55)
    else:
        pdf.set_y(pdf.get_y() + 10)

    # 2. Materials & Equipment (Side by Side)
    col1_y = pdf.get_y()
    
    # Materials Table
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(230, 240, 250)
    pdf.cell(90, 8, "  Materials & Equipment Status", ln=False, fill=True)
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(45, 6, "Major Materials Received", border=1, fill=True)
    pdf.cell(45, 6, "Key Equipment Utilization", border=1, ln=True, fill=True)
    
    pdf.set_font("Helvetica", "", 8)
    mat_lines = parse_lines(materials)
    eq_lines = parse_lines(equipment)
    max_rows = max(len(mat_lines), len(eq_lines))
    
    for i in range(max_rows):
        mat = mat_lines[i] if i < len(mat_lines) else ""
        eq = eq_lines[i] if i < len(eq_lines) else ""
        pdf.cell(45, 6, mat, border=1)
        pdf.cell(45, 6, eq, border=1, ln=True)

    # 3. Safety Report Summary (Right side or below)
    pdf.set_y(col1_y)
    pdf.set_x(105)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(230, 240, 250)
    pdf.cell(95, 8, "  Safety Report Summary", ln=True, fill=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 9)
    safety_lines = parse_lines(safety)
    for line in safety_lines:
        pdf.set_x(105)
        pdf.cell(5, 6, "✓")
        pdf.cell(85, 6, line, ln=True)

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
        label="⬇️ Download Your PDF Report",
        data=st.session_state["pdf_bytes"],
        file_name=st.session_state["pdf_name"],
        mime="application/pdf",
        type="primary"
    )
