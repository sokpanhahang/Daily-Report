import streamlit as st
import io

# --- PAGE SETUP ---
st.set_page_config(page_title="Daily Construction Report", layout="wide", page_icon="️")
st.title("🏗️ Construction Daily Report Generator")
st.markdown("Fill out the form below to generate a beautiful, modern report.")

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
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: apex_manpower = st.number_input("Apex Manpower", value=28)
    with col2: total_manpower = st.number_input("Total Manpower", value=142)
    with col3: subs_present = st.number_input("Subcontractors", value=7)
    with col4: dyno_manpower = st.number_input("Dyno Manpower", value=15)
    with col5: progress = st.number_input("Progress (%)", value=61)

    st.subheader("3. Subcontractor Site Log")
    sub_log = st.text_area("Subcontractor Log", "Apex Concrete | Structural | 28 | 07:00-17:00 | Foundation pour Grid A\nDyno Electrical | MEP | 15 | 07:00-17:00 | Cable tray installation")

    st.subheader("4. Critical Issues")
    issues = st.text_area("Issues", "Rebar inspection delayed | High\nMaterial delivery delayed | High\nBFI #104 pending review | Medium")
    issues_resolved = st.number_input("Issues Resolved Count", value=3)

    st.subheader("5. Materials & Equipment")
    materials = st.text_area("Materials Received", "Rebar | 1 tons\nConcrete | 2 cubic meters")
    equipment = st.text_area("Equipment Utilization", "Crane | 1 hours\nExcavator | 2 issues")

    st.subheader("6. Safety Report Summary")
    safety = st.text_area("Safety Checks", "Safety Check for PPE compliance\nSafety Check on tools and harness\nNo incidents reported today.")

    st.subheader("7. Site Photos")
    photos = st.file_uploader("Upload Site Photos (Up to 15 total)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    submitted = st.form_submit_button("Generate Beautiful Report", type="primary")

# --- HTML GENERATION LOGIC ---
if submitted:
    # Helper to parse text
    def parse_lines(text):
        return [line.strip() for line in text.split('\n') if line.strip()]

    # Process photos to base64 so they embed in the HTML
    photo_html_page1 = ""
    photo_html_page2 = ""
    
    if photos:
        for i, photo in enumerate(photos[:15]):
            img_bytes = photo.read()
            import base64
            img_b64 = base64.b64encode(img_bytes).decode()
            caption = f"{i+1}. {photo.name[:20]}"
            
            photo_card = f'''
            <div class="photo-card">
                <img src="data:image/jpeg;base64,{img_b64}" alt="Site Photo">
                <div class="photo-caption">{caption}</div>
            </div>'''
            
            if i < 5:
                photo_html_page1 += photo_card
            else:
                photo_html_page2 += photo_card

    # Process tables
    def make_table_rows(text):
        rows = ""
        for line in parse_lines(text):
            parts = [p.strip() for p in line.split('|')]
            cells = "".join([f"<td>{p}</td>" for p in parts])
            rows += f"<tr>{cells}</tr>"
        return rows

    sub_rows = make_table_rows(sub_log)
    mat_rows = make_table_rows(materials)
    eq_rows = make_table_rows(equipment)
    
    # Process Issues
    issue_cards = ""
    for i, line in enumerate(parse_lines(issues)[:3]):
        parts = [p.strip() for p in line.split('|')]
        desc = parts[0]
        priority = parts[1] if len(parts) > 1 else "Medium"
        color = "#e74c3c" if priority.lower() == 'high' else "#f39c12"
        issue_cards += f'''
        <div class="issue-card">
            <div class="issue-title">Issue {i+1}: {desc[:25]}...</div>
            <div class="issue-desc">{desc}</div>
            <div class="issue-priority" style="color: {color};">Priority: {priority}</div>
        </div>'''

    # THE BEAUTIFUL HTML TEMPLATE
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @page {{ size: A4; margin: 10mm; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #172B4D; margin: 0; padding: 20px; background: #fff; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #DEEBFF; padding-bottom: 10px; margin-bottom: 20px; }}
        .logo {{ color: #0052CC; font-weight: bold; font-size: 18px; display: flex; align-items: center; }}
        .logo span {{ background: #0052CC; color: white; padding: 2px 6px; border-radius: 4px; margin-right: 8px; }}
        .title {{ font-size: 24px; font-weight: 600; margin: 10px 0 20px 0; }}
        
        /* Cards */
        .cards-container {{ display: flex; gap: 10px; margin-bottom: 25px; }}
        .card {{ flex: 1; padding: 12px; border-radius: 6px; border: 1px solid #DFE1E6; background: #FAFBFC; }}
        .card.green {{ background: #E3FCEF; border-color: #57D9A3; }}
        .card-title {{ font-size: 11px; color: #5E6C84; font-weight: 600; text-transform: uppercase; }}
        .card-value {{ font-size: 24px; font-weight: bold; margin: 5px 0; }}
        .card-sub {{ font-size: 10px; color: #5E6C84; }}
        
        /* Tables */
        .section-title {{ font-size: 16px; font-weight: 600; margin: 20px 0 10px 0; border-bottom: 1px solid #DFE1E6; padding-bottom: 5px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 20px; }}
        th {{ background: #F4F5F7; text-align: left; padding: 8px; border: 1px solid #DFE1E6; font-weight: 600; }}
        td {{ padding: 8px; border: 1px solid #DFE1E6; }}
        
        /* Issues */
        .issues-grid {{ display: flex; gap: 10px; margin-bottom: 20px; }}
        .issue-card {{ flex: 1; background: #FAFBFC; border: 1px solid #DFE1E6; border-radius: 6px; padding: 10px; }}
        .issue-title {{ font-weight: bold; font-size: 12px; margin-bottom: 5px; }}
        .issue-desc {{ font-size: 11px; color: #5E6C84; margin-bottom: 8px; }}
        .issue-priority {{ font-size: 11px; font-weight: bold; }}
        
        /* Photos */
        .photo-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 20px; }}
        .photo-card {{ border: 1px solid #DFE1E6; border-radius: 6px; overflow: hidden; }}
        .photo-card img {{ width: 100%; height: 100px; object-fit: cover; }}
        .photo-caption {{ font-size: 10px; padding: 5px; text-align: center; background: #FAFBFC; }}
        
        /* Two Column Layout */
        .two-col {{ display: flex; gap: 20px; }}
        .col {{ flex: 1; }}
        
        /* Print Button */
        .print-btn {{ position: fixed; top: 20px; right: 20px; background: #0052CC; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-size: 14px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .print-btn:hover {{ background: #0747A6; }}
        
        @media print {{
            .print-btn {{ display: none; }}
            body {{ padding: 0; }}
            .page-break {{ page-break-before: always; }}
        }}
    </style>
    </head>
    <body>
        <button class="print-btn" onclick="window.print()">🖨️ Save as PDF</button>
        
        <!-- PAGE 1 -->
        <div class="header">
            <div class="logo"><span>▲</span> ATLASSIAN</div>
            <div style="text-align: right; font-size: 12px; color: #5E6C84;">
                ABC Construction - Daily Site Report<br>
                Page 1/2
            </div>
        </div>
        
        <div class="title">Daily Site Report</div>
        
        <div class="cards-container">
            <div class="card green">
                <div class="card-title">Manpower - Apex</div>
                <div class="card-value">{apex_manpower}</div>
                <div class="card-sub">Next: Concrete Pour</div>
            </div>
            <div class="card">
                <div class="card-title">Total Site Manpower</div>
                <div class="card-value">{total_manpower}</div>
            </div>
            <div class="card">
                <div class="card-title">Subcontractors Present</div>
                <div class="card-value">{subs_present}</div>
            </div>
            <div class="card">
                <div class="card-title">Manpower - Dyno</div>
                <div class="card-value">{dyno_manpower}</div>
                <div class="card-sub">Dyno Electrical</div>
            </div>
            <div class="card">
                <div class="card-title">Project Progress</div>
                <div class="card-value" style="color: #00875A;">{progress}%</div>
                <div class="card-sub">Daily Progress</div>
            </div>
        </div>

        <div class="section-title">Subcontractor Manpower and Site Log</div>
        <table>
            <thead><tr><th>Subcontractor</th><th>Trade</th><th>Headcount</th><th>Start/End Time</th><th>Work Description</th></tr></thead>
            <tbody>{sub_rows}</tbody>
        </table>

        <div class="section-title">Critical Site Issues & Hold Points <span style="float: right; font-size: 12px; font-weight: normal;">Issues Resolved: {issues_resolved}</span></div>
        <div class="issues-grid">
            {issue_cards}
        </div>

        <div class="section-title">Daily Site Photos & Descriptions</div>
        <div class="photo-grid">
            {photo_html_page1}
        </div>

        <!-- PAGE 2 -->
        <div class="page-break"></div>
        
        <div class="header">
            <div class="logo"><span>▲</span> ATLASSIAN</div>
            <div style="text-align: right; font-size: 12px; color: #5E6C84;">
                ABC Construction - Daily Site Report<br>
                Page 2/2
            </div>
        </div>
        
        <div class="title">Daily Site Report</div>

        <div class="section-title">ADDITIONAL SITE PHOTOS & FIELD OBSERVATIONS</div>
        <div class="photo-grid">
            {photo_html_page2 if photo_html_page2 else '<div style="color: #999; grid-column: span 5; text-align: center; padding: 20px;">No additional photos uploaded.</div>'}
        </div>

        <div class="two-col">
            <div class="col">
                <div class="section-title">MATERIALS & EQUIPMENT STATUS</div>
                <table>
                    <thead><tr><th colspan="2">Major Materials Received</th></tr></thead>
                    <tbody>{mat_rows}</tbody>
                </table>
                <table>
                    <thead><tr><th colspan="2">Key Equipment Utilization</th></tr></thead>
                    <tbody>{eq_rows}</tbody>
                </table>
            </div>
            <div class="col">
                <div class="section-title">SAFETY REPORT SUMMARY</div>
                <table>
                    <thead><tr><th>Safety Check Summary</th></tr></thead>
                    <tbody>
                        {"".join([f"<tr><td>✓ {line}</td></tr>" for line in parse_lines(safety)])}
                    </tbody>
                </table>
            </div>
        </div>
        
        <div style="margin-top: 40px; border-top: 1px solid #DFE1E6; padding-top: 10px; font-size: 10px; color: #999; text-align: center;">
            A4 Document | Construction Daily Report | Date: {report_date.strftime('%B %d, %Y')} | Prepared by {prepared_by}
        </div>
    </body>
    </html>
    '''

    # Save HTML to memory
    html_bytes = html_content.encode('utf-8')
    st.session_state["html_bytes"] = html_bytes
    st.session_state["html_name"] = f"Report_{project_name}_{report_date}.html"

# --- SHOW DOWNLOAD BUTTON ---
if "html_bytes" in st.session_state:
    st.success("✅ Beautiful Report Generated!")
    st.info("👇 **How to get your PDF:** Download the HTML file below, open it in Chrome/Edge, and click the blue **'Save as PDF'** button at the top right!")
    
    st.download_button(
        label="⬇️ Download Report File",
        data=st.session_state["html_bytes"],
        file_name=st.session_state["html_name"],
        mime="text/html",
        type="primary"
    )
