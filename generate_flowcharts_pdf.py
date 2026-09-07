import os
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

# Ensure output directory exists
pdf_dir = r"C:\Users\lenovo\.gemini\antigravity\brain\53786b3d-3ff8-4200-88e1-3e7e0e2364aa"
os.makedirs(pdf_dir, exist_ok=True)

# Helper function to get font
def get_font(size=14, bold=False):
    try:
        if bold:
            return ImageFont.truetype("arialbd.ttf", size)
        return ImageFont.truetype("arial.ttf", size)
    except IOError:
        return ImageFont.load_default()

# -------------------------------------------------------------
# 1. DRAW SYSTEM BLOCK DIAGRAM
# -------------------------------------------------------------
def draw_block_diagram(filename):
    img = Image.new('RGB', (1000, 750), color=(250, 252, 250))
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(20, bold=True)
    font_header = get_font(16, bold=True)
    font_box = get_font(13, bold=False)
    font_arrow = get_font(11, bold=True)
    
    # Header Title
    draw.rectangle([0, 0, 1000, 60], fill=(27, 94, 32))
    draw.text((300, 15), "GreenCart - 3-Tier System Block Diagram", fill=(255, 255, 255), font=font_title)
    
    # Layer 1: Presentation Layer
    draw.rectangle([40, 90, 960, 250], outline=(46, 125, 50), width=3, fill=(232, 245, 233))
    draw.text((60, 100), "PRESENTATION LAYER (Frontend)", fill=(27, 94, 32), font=font_header)
    
    boxes_l1 = [
        ("HTML5 / CSS3 / JavaScript", (70, 140, 270, 210)),
        ("Bootstrap 5 UI Components", (295, 140, 495, 210)),
        ("Chart.js Visual Analytics", (520, 140, 720, 210)),
        ("AJAX Live Polling Engine", (745, 140, 930, 210))
    ]
    for text, coords in boxes_l1:
        draw.rectangle(coords, fill=(255, 255, 255), outline=(76, 175, 80), width=2)
        lines = text.split('\n')
        y_off = coords[1] + 20
        draw.text((coords[0] + 10, y_off), text, fill=(33, 33, 33), font=font_box)

    # Layer 2: Application Layer
    draw.rectangle([40, 310, 960, 510], outline=(21, 101, 192), width=3, fill=(227, 242, 253))
    draw.text((60, 320), "APPLICATION LAYER (Python Flask Core)", fill=(13, 71, 161), font=font_header)
    
    boxes_l2 = [
        ("Flask Core App", (70, 360, 220, 420)),
        ("Auth & RBAC", (240, 360, 370, 420)),
        ("Customer Routes", (390, 360, 540, 420)),
        ("Admin Routes", (560, 360, 700, 420)),
        ("Delivery Routes", (720, 360, 850, 420)),
        ("REST APIs & Live Status", (70, 435, 450, 490)),
        ("SQLAlchemy ORM Engine", (480, 435, 930, 490))
    ]
    for text, coords in boxes_l2:
        draw.rectangle(coords, fill=(255, 255, 255), outline=(30, 136, 229), width=2)
        draw.text((coords[0] + 10, coords[1] + 15), text, fill=(33, 33, 33), font=font_box)

    # Layer 3: Data Layer
    draw.rectangle([40, 570, 960, 710], outline=(230, 81, 0), width=3, fill=(255, 243, 224))
    draw.text((60, 580), "DATA LAYER (Database & Asset Storage)", fill=(230, 81, 0), font=font_header)
    
    boxes_l3 = [
        ("Relational Database: SQLite / MySQL (180+ Plants, Users, Orders)", (70, 620, 580, 680)),
        ("Media Assets (180 Plant JPG Photos)", (610, 620, 930, 680))
    ]
    for text, coords in boxes_l3:
        draw.rectangle(coords, fill=(255, 255, 255), outline=(251, 140, 0), width=2)
        draw.text((coords[0] + 10, coords[1] + 15), text, fill=(33, 33, 33), font=font_box)

    # Connecting Arrows
    draw.line([(500, 250), (500, 310)], fill=(33, 33, 33), width=3)
    draw.polygon([(495, 305), (505, 305), (500, 312)], fill=(33, 33, 33))
    draw.text((515, 270), "HTTP/HTTPS Requests", fill=(33, 33, 33), font=font_arrow)

    draw.line([(500, 510), (500, 570)], fill=(33, 33, 33), width=3)
    draw.polygon([(495, 565), (505, 565), (500, 572)], fill=(33, 33, 33))
    draw.text((515, 530), "SQL Queries / ORM Data Sync", fill=(33, 33, 33), font=font_arrow)

    img.save(filename)
    print(f"Saved: {filename}")

# -------------------------------------------------------------
# 2. DRAW ORDER FLOWCHART
# -------------------------------------------------------------
def draw_order_flowchart(filename):
    img = Image.new('RGB', (1000, 1150), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(20, bold=True)
    font_box = get_font(12, bold=True)
    font_sub = get_font(10, bold=False)
    
    # Header Title
    draw.rectangle([0, 0, 1000, 60], fill=(27, 94, 32))
    draw.text((220, 15), "GreenCart - End-to-End Order Lifecycle Flowchart", fill=(255, 255, 255), font=font_title)
    
    steps = [
        ("1. Customer Browses Catalog & Adds Plants to Cart", "Selects from 180+ plants across 12 categories", (200, 80, 800, 140), (232, 245, 233), (46, 125, 50)),
        ("2. Real-Time Stock Availability Check", "Verifies stock > 0 in database before checkout", (200, 170, 800, 230), (255, 243, 224), (230, 81, 0)),
        ("3. Checkout & Payment Simulation", "Enters delivery address & selects UPI / Card / COD", (200, 260, 800, 320), (232, 245, 233), (46, 125, 50)),
        ("4. AUTOMATIC STOCK DEDUCTION in Database", "Inventory decrements instantly upon order submission", (200, 350, 800, 410), (255, 235, 238), (198, 40, 40)),
        ("5. Order Status = 'Placed'", "Order recorded, initial payment entry created", (200, 440, 800, 500), (227, 242, 253), (21, 101, 192)),
        ("6. Admin Reviews & Confirms Order", "Status changes to 'Confirmed'", (200, 530, 800, 590), (243, 229, 245), (106, 27, 154)),
        ("7. Admin Assigns Delivery Partner", "Order assigned to specific active logistics agent", (200, 620, 800, 680), (243, 229, 245), (106, 27, 154)),
        ("8. Delivery Partner Accepts Order", "DP clicks 'Accept' -> Status: 'Accepted'", (200, 710, 800, 770), (230, 245, 249), (0, 131, 143)),
        ("9. Delivery Partner Starts Delivery", "DP clicks 'Start' -> Status: 'Out for Delivery'", (200, 800, 800, 860), (230, 245, 249), (0, 131, 143)),
        ("10. Customer Receives Package & Order Marked Delivered", "Status: 'Delivered' & Payment Status: 'Successful'", (200, 890, 800, 950), (232, 245, 233), (46, 125, 50)),
    ]
    
    for i, (title, sub, coords, bg, border) in enumerate(steps):
        draw.rectangle(coords, fill=bg, outline=border, width=2)
        draw.text((coords[0] + 20, coords[1] + 12), title, fill=(33, 33, 33), font=font_box)
        draw.text((coords[0] + 20, coords[1] + 35), sub, fill=(100, 100, 100), font=font_sub)
        
        # Connectors
        if i < len(steps) - 1:
            next_y1 = coords[3]
            next_y2 = steps[i+1][2][1]
            draw.line([(500, next_y1), (500, next_y2)], fill=(66, 66, 66), width=2)
            draw.polygon([(495, next_y2 - 5), (505, next_y2 - 5), (500, next_y2)], fill=(66, 66, 66))

    # Live Tracking Side Note
    draw.rectangle([50, 980, 950, 1100], fill=(255, 248, 225), outline=(255, 179, 0), width=2)
    draw.text((70, 995), "LIVE AJAX ORDER TRACKING ENGINE:", fill=(230, 81, 0), font=font_box)
    draw.text((70, 1025), "Throughout Steps 5 to 10, the Customer Tracking Page executes asynchronous background AJAX requests", fill=(33, 33, 33), font=font_sub)
    draw.text((70, 1050), "to /api/order-status/<id>, updating the live progress bar instantly without full page reloads.", fill=(33, 33, 33), font=font_sub)

    img.save(filename)
    print(f"Saved: {filename}")

# -------------------------------------------------------------
# 3. DRAW SERVICES & DFD DIAGRAM
# -------------------------------------------------------------
def draw_services_dfd_diagram(filename):
    img = Image.new('RGB', (1000, 850), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(20, bold=True)
    font_header = get_font(15, bold=True)
    font_box = get_font(12, bold=True)
    font_sub = get_font(10, bold=False)
    
    # Header Title
    draw.rectangle([0, 0, 1000, 60], fill=(27, 94, 32))
    draw.text((180, 15), "GreenCart - Plant Services Booking & DFD Flowchart", fill=(255, 255, 255), font=font_title)
    
    # Section A: Services Workflow
    draw.text((50, 80), "A. Plant Services Booking Workflow", fill=(27, 94, 32), font=font_header)
    
    service_steps = [
        ("1. Select Care Service", "Repotting, Pruning, Pest Control", (50, 120, 260, 200)),
        ("2. Fill Schedule Form", "Select Date, Time & Address", (280, 120, 490, 200)),
        ("3. Admin Review & Assign", "Approve booking & assign gardener", (510, 120, 720, 200)),
        ("4. Service Completed", "Gardener completes service on site", (740, 120, 950, 200))
    ]
    for i, (t, s, coords) in enumerate(service_steps):
        draw.rectangle(coords, fill=(232, 245, 233), outline=(46, 125, 50), width=2)
        draw.text((coords[0] + 10, coords[1] + 15), t, fill=(33, 33, 33), font=font_box)
        draw.text((coords[0] + 10, coords[1] + 45), s, fill=(100, 100, 100), font=font_sub)
        if i < 3:
            draw.line([(coords[2], 160), (service_steps[i+1][2][0], 160)], fill=(46, 125, 50), width=3)
            draw.polygon([(service_steps[i+1][2][0]-5, 155), (service_steps[i+1][2][0]-5, 165), (service_steps[i+1][2][0], 160)], fill=(46, 125, 50))

    # Section B: Data Flow Diagram (DFD Level 1)
    draw.text((50, 240), "B. Data Flow Diagram (DFD Level 1 Architecture)", fill=(21, 101, 192), font=font_header)
    
    # External Entities
    entities = [
        ("CUSTOMER", (50, 300, 200, 380), (227, 242, 253), (21, 101, 192)),
        ("ADMINISTRATOR", (50, 480, 200, 560), (243, 229, 245), (106, 27, 154)),
        ("DELIVERY PARTNER", (50, 660, 200, 740), (230, 245, 249), (0, 131, 143))
    ]
    for name, coords, bg, bdr in entities:
        draw.rectangle(coords, fill=bg, outline=bdr, width=3)
        draw.text((coords[0] + 15, coords[1] + 30), name, fill=(33, 33, 33), font=font_box)

    # Processes
    processes = [
        ("1.0 Auth & Session", (300, 300, 500, 380)),
        ("2.0 Catalog & Search", (300, 420, 500, 500)),
        ("3.0 Order & Stock Engine", (300, 540, 500, 620)),
        ("4.0 Delivery Execution", (300, 660, 500, 740))
    ]
    for name, coords in processes:
        draw.ellipse(coords, fill=(255, 248, 225), outline=(255, 179, 0), width=3)
        draw.text((coords[0] + 25, coords[1] + 30), name, fill=(33, 33, 33), font=font_box)

    # Data Stores
    stores = [
        ("D1: Users Table", (600, 300, 930, 360)),
        ("D2: Plants & Categories Table", (600, 420, 930, 480)),
        ("D3: Orders & OrderItems Table", (600, 540, 930, 600)),
        ("D4: Payments & Services Table", (600, 660, 930, 720))
    ]
    for name, coords in stores:
        draw.rectangle(coords, fill=(245, 245, 245), outline=(117, 117, 117), width=2)
        draw.text((coords[0] + 20, coords[1] + 20), name, fill=(33, 33, 33), font=font_box)

    # Lines connecting DFD
    for y in [340, 460, 580, 700]:
        draw.line([(200, y), (300, y)], fill=(66, 66, 66), width=2)
        draw.line([(500, y), (600, y)], fill=(66, 66, 66), width=2)

    # Credit Footer
    draw.rectangle([0, 790, 1000, 850], fill=(27, 94, 32))
    draw.text((340, 810), "Project Done By Shamitha - GreenCart Platform", fill=(255, 255, 255), font=font_header)

    img.save(filename)
    print(f"Saved: {filename}")

# Generate Images
img1 = os.path.join(pdf_dir, "diagram_block.png")
img2 = os.path.join(pdf_dir, "diagram_order.png")
img3 = os.path.join(pdf_dir, "diagram_services_dfd.png")

draw_block_diagram(img1)
draw_order_flowchart(img2)
draw_services_dfd_diagram(img3)

# -------------------------------------------------------------
# CREATE PDF DOCUMENT USING FPDF
# -------------------------------------------------------------
pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=True, margin=15)

# Page 1: Title Page & Block Diagram
pdf.add_page()
pdf.set_font("Helvetica", "B", 18)
pdf.set_text_color(27, 94, 32)
pdf.cell(0, 10, "GreenCart - Software Flowcharts & System Architecture", ln=True, align="C")
pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, "Project Done By Shamitha", ln=True, align="C")
pdf.ln(5)

pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(33, 33, 33)
pdf.cell(0, 8, "1. 3-Tier System Block Diagram", ln=True)
pdf.image(img1, x=10, y=40, w=190)

# Page 2: End-to-End Order Flowchart
pdf.add_page()
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 8, "2. End-to-End Order Lifecycle & Live Tracking Flowchart", ln=True)
pdf.image(img2, x=10, y=25, w=190)

# Page 3: Services & DFD
pdf.add_page()
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 8, "3. Plant Services Booking & Data Flow Diagram (DFD Level 1)", ln=True)
pdf.image(img3, x=10, y=25, w=190)

# Output PDF Paths
out_pdf_brain = os.path.join(pdf_dir, "GreenCart_Flowcharts_and_Diagrams.pdf")
out_pdf_local = r"c:\Users\lenovo\Downloads\GreenCart\GreenCart_Flowcharts_and_Diagrams.pdf"

pdf.output(out_pdf_brain)
pdf.output(out_pdf_local)

print(f"PDF Successfully Generated at:\n1. {out_pdf_brain}\n2. {out_pdf_local}")
