import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# --- PAGE SETUP ---
st.set_page_config(page_title="Daily Construction Report", layout="wide", page_icon="🏗️")
st.title("️ Construction Daily Report Generator")
st.markdown("Fill out the form below. When you click generate, you will get a professional PDF.")

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
    
    weather = st.selectbox("Weather Conditions", ["Sunny", "Cloudy", "Rainy", "Windy", "Snowy"])

    st.subheader("2. Manpower & Progress")
    total_manpower = st.number_input("Total Site Manpower", min_value=0, value=142)
    progress = st.slider("Overall Project Progress (%)", 0, 100, 61)

    st.subheader("3. Work & Issues")
    work_completed = st.text_area("Work Completed Today", "Installed 120m conduit Zone A\nPoured concrete slab foundation")
    issues = st.text_area("Issues / Delays / Safety Notes", "None today")

    st.subheader("4. Site Photos")
    photos = st.file_uploader("Upload Site Photos (Max 6 for PDF)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    # SUBMIT BUTTON
    submitted = st.form_submit_button("Generate PDF Report", type="primary")

# --- PDF GENERATION LOGIC ---
if submitted:
    pdf = FPDF()
    pdf.add_page()
    
    # 1. HEADER
    pdf.set_fill_color(25, 118, 210) # Professional Blue
    pdf.rect(0, 0, 210, 30, 'F')
    pdf.set_y(5)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, "DAILY CONSTRUCTION REPORT", ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    
    # 2. PROJECT INFO BOX
    pdf.set_y(35)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"Project: {project_name}", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(95, 6, f"Date: {report_date.strftime('%B %d, %Y')}")
    pdf.cell(95, 6, f"Report #: {report_no}", ln=True)
    pdf.cell(95, 6, f"Prepared By: {prepared_by}")
    pdf.cell(95, 6, f"Weather: {weather}", ln=True)
    pdf.ln(5)
    
    # 3. MANPOWER & PROGRESS
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_fill_color(230, 240, 250)
    pdf.cell(0, 8, "  MANPOWER & PROGRESS", ln=True, fill=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(95, 6, f"Total Manpower: {total_manpower} workers")
    pdf.cell(95, 6, f"Project Progress: {progress}%", ln=True)
    pdf.ln(5)

    # 4. WORK COMPLETED
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "  WORK COMPLETED TODAY", ln=True, fill=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, work_completed)
    pdf.ln(3)

    # 5. ISSUES
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "  ISSUES / DELAYS / SAFETY", ln=True, fill=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, issues)
    pdf.ln(5)

    # 6. PHOTOS
    if photos:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_fill_color(230, 240, 250)
        pdf.cell(0, 10, "  SITE PHOTOGRAPHY", ln=True, fill=True)
        pdf.ln(5)
        
        pdf.set_font("Helvetica", "", 10)
        for i, photo in enumerate(photos[:6]): # Limit to 6 photos to keep PDF clean
            try:
                # Read and resize image
                img = Image.open(photo)
                img = img.resize((150, 100), Image.Resampling.LANCZOS)
                
                # Save to memory
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                img_byte_arr.seek(0)
                
                # Add to PDF (2 photos per row)
                if i % 2 == 0 and i > 0:
                    pdf.ln(5)
                
                pdf.image(img_byte_arr, x=10 + (i % 2) * 95, y=pdf.get_y(), w=85, h=56)
                pdf.set_xy(10 + (i % 2) * 95, pdf.get_y() + 58)
                pdf.cell(85, 5, f"Photo {i+1}: {photo.name}", ln=True, align="C")
                
            except Exception as e:
                pdf.cell(0, 6, f"Error loading photo {i+1}", ln=True)

    # SAVE AND DOWNLOAD (FIXED: Using BytesIO to guarantee Streamlit accepts the file)
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    
    st.session_state["pdf_bytes"] = pdf_buffer.getvalue()
    st.session_state["pdf_name"] = f"Daily_Report_{report_date}.pdf"

# --- SHOW DOWNLOAD BUTTON AFTER GENERATION ---
if "pdf_bytes" in st.session_state:
    st.success("PDF Generated Successfully!")
    st.download_button(
        label="Download Your PDF Report",
        data=st.session_state["pdf_bytes"],
        file_name=st.session_state["pdf_name"],
        mime="application/pdf",
        type="primary"
    )
