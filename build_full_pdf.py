import os
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

pdf_dir = r"C:\Users\lenovo\.gemini\antigravity\brain\53786b3d-3ff8-4200-88e1-3e7e0e2364aa"
os.makedirs(pdf_dir, exist_ok=True)

# Run image generator scripts
import generate_flowcharts_pdf
import generate_usecase_img

# Copy PNG to brain folder as well
import shutil
img_uc_src = r"c:\Users\lenovo\Downloads\GreenCart\use_case_diagram.png"
img_uc_brain = os.path.join(pdf_dir, "use_case_diagram.png")
shutil.copy(img_uc_src, img_uc_brain)

# Generate PDF with 4 Pages
pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=True, margin=15)

img1 = os.path.join(pdf_dir, "diagram_block.png")
img2 = os.path.join(pdf_dir, "diagram_order.png")
img3 = os.path.join(pdf_dir, "diagram_services_dfd.png")
img4 = img_uc_brain

# Page 1: Title & Block Diagram
pdf.add_page()
pdf.set_font("Helvetica", "B", 18)
pdf.set_text_color(27, 94, 32)
pdf.cell(0, 10, "GreenCart - Software Flowcharts & System Architecture", align="C")
pdf.ln(10)
pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, "Project Done By Shamitha", align="C")
pdf.ln(12)

pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(33, 33, 33)
pdf.cell(0, 8, "1. 3-Tier System Block Diagram")
pdf.ln(10)
pdf.image(img1, x=10, y=45, w=190)

# Page 2: End-to-End Order Flowchart
pdf.add_page()
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 8, "2. End-to-End Order Lifecycle & Live Tracking Flowchart")
pdf.ln(10)
pdf.image(img2, x=10, y=25, w=190)

# Page 3: Services & DFD
pdf.add_page()
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 8, "3. Plant Services Booking & Data Flow Diagram (DFD Level 1)")
pdf.ln(10)
pdf.image(img3, x=10, y=25, w=190)

# Page 4: UML Use Case Diagram
pdf.add_page()
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 8, "4. Complete UML Use Case Diagram (Actors & System Boundary)")
pdf.ln(10)
pdf.image(img4, x=10, y=25, w=190)

# Save PDF
out_pdf_brain = os.path.join(pdf_dir, "GreenCart_Flowcharts_and_Diagrams.pdf")
out_pdf_local = r"c:\Users\lenovo\Downloads\GreenCart\GreenCart_Flowcharts_and_Diagrams.pdf"

pdf.output(out_pdf_brain)
pdf.output(out_pdf_local)

print(f"Updated 4-Page PDF Successfully Generated at:\n1. {out_pdf_brain}\n2. {out_pdf_local}")
