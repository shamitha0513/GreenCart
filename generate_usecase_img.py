import os
from PIL import Image, ImageDraw, ImageFont

# Ensure directory exists
output_dir = r"c:\Users\lenovo\Downloads\GreenCart"

def get_font(size=14, bold=False):
    try:
        if bold:
            return ImageFont.truetype("arialbd.ttf", size)
        return ImageFont.truetype("arial.ttf", size)
    except IOError:
        return ImageFont.load_default()

# Create canvas
img = Image.new('RGB', (1100, 850), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

font_title = get_font(20, bold=True)
font_actor = get_font(15, bold=True)
font_uc = get_font(12, bold=True)
font_inc = get_font(11, bold=True)

# 1. Main Title
draw.rectangle([0, 0, 1100, 60], fill=(27, 94, 32))
draw.text((320, 15), "GreenCart - UML Use Case Diagram", fill=(255, 255, 255), font=font_title)

# 2. System Boundary Box (Middle)
draw.rectangle([280, 90, 820, 800], outline=(46, 125, 50), width=3, fill=(245, 250, 245))
draw.text((380, 105), "[ SYSTEM BOUNDARY: GreenCart Platform ]", fill=(27, 94, 32), font=get_font(13, bold=True))

# 3. Actors (Left & Right)
# Left Actor: Customer
draw.rectangle([30, 320, 230, 480], fill=(227, 242, 253), outline=(21, 101, 192), width=3)
draw.text((80, 385), "CUSTOMER", fill=(13, 71, 161), font=font_actor)

# Right Actor 1: Administrator
draw.rectangle([870, 200, 1070, 360], fill=(243, 229, 245), outline=(106, 27, 154), width=3)
draw.text((885, 265), "ADMINISTRATOR", fill=(74, 20, 140), font=font_actor)

# Right Actor 2: Delivery Partner
draw.rectangle([870, 520, 1070, 680], fill=(230, 245, 249), outline=(0, 131, 143), width=3)
draw.text((875, 575), "DELIVERY", fill=(0, 77, 64), font=font_actor)
draw.text((880, 605), "PARTNER", fill=(0, 77, 64), font=font_actor)

# 4. Use Cases Ovals inside System Boundary
use_cases = [
    ("Login / User Auth", (330, 145, 530, 195), (255, 255, 255), (76, 175, 80)),
    ("User Registration", (570, 145, 770, 195), (255, 255, 255), (76, 175, 80)),
    
    ("Browse & Search Plants", (350, 220, 750, 265), (255, 255, 255), (46, 125, 50)),
    ("View Plant Care Specs", (350, 280, 750, 325), (255, 255, 255), (46, 125, 50)),
    ("Manage Shopping Cart", (350, 340, 750, 385), (255, 255, 255), (46, 125, 50)),
    ("Checkout & Payment", (350, 400, 750, 445), (255, 255, 255), (46, 125, 50)),
    ("Live Order Tracking", (350, 460, 750, 505), (255, 255, 255), (46, 125, 50)),
    ("Book Plant Services", (350, 520, 750, 565), (255, 255, 255), (46, 125, 50)),
    
    ("Manage Plants & Stock CRUD", (350, 580, 750, 625), (255, 255, 255), (106, 27, 154)),
    ("Confirm & Assign Delivery", (350, 640, 750, 685), (255, 255, 255), (106, 27, 154)),
    ("Analytics & Export CSV", (350, 700, 745, 745), (255, 255, 255), (106, 27, 154)),
    ("Delivery Status Sync", (350, 750, 750, 790), (255, 255, 255), (0, 131, 143))
]

for name, coords, bg, bdr in use_cases:
    draw.ellipse(coords, fill=bg, outline=bdr, width=2)
    # text placement
    tx = coords[0] + 25
    ty = coords[1] + 12
    draw.text((tx, ty), name, fill=(33, 33, 33), font=font_uc)

# Include arrow between Login and Registration
draw.line([(530, 170), (570, 170)], fill=(198, 40, 40), width=2)
draw.polygon([(565, 165), (565, 175), (572, 170)], fill=(198, 40, 40))
draw.text((515, 130), "<<include>>", fill=(198, 40, 40), font=font_inc)

# Lines from Customer (Left) to Use Cases
cust_point = (230, 400)
for target_y in [170, 242, 302, 362, 422, 482, 542]:
    draw.line([cust_point, (350, target_y)], fill=(30, 136, 229), width=2)

# Lines from Admin (Right 1) to Use Cases
admin_point = (870, 280)
for target_y in [170, 602, 662, 722]:
    draw.line([admin_point, (750, target_y)], fill=(142, 36, 170), width=2)

# Lines from Delivery Partner (Right 2) to Use Cases
dp_point = (870, 600)
for target_y in [170, 662, 770]:
    draw.line([dp_point, (750, target_y)], fill=(0, 150, 136), width=2)

# Save image
out_png = os.path.join(output_dir, "use_case_diagram.png")
img.save(out_png)
print(f"Saved Use Case Diagram PNG: {out_png}")
