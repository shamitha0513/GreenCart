import os
from PIL import Image, ImageDraw, ImageFont

output_dir = r"c:\Users\lenovo\Downloads\GreenCart"

def get_font(size=13, bold=False):
    try:
        if bold:
            return ImageFont.truetype("arialbd.ttf", size)
        return ImageFont.truetype("arial.ttf", size)
    except IOError:
        return ImageFont.load_default()

# Canvas setup
img = Image.new('RGB', (1100, 950), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

font_title = get_font(20, bold=True)
font_class = get_font(13, bold=True)
font_attr = get_font(10, bold=False)

# Header
draw.rectangle([0, 0, 1100, 60], fill=(27, 94, 32))
draw.text((360, 15), "GreenCart - UML Class Diagram", fill=(255, 255, 255), font=font_title)

# Draw Class Box helper
def draw_class(name, attrs, coords, header_bg=(46, 125, 50)):
    x1, y1, x2, y2 = coords
    # Main outer box
    draw.rectangle([x1, y1, x2, y2], fill=(250, 250, 250), outline=header_bg, width=2)
    # Header box
    draw.rectangle([x1, y1, x2, y1 + 30], fill=header_bg)
    draw.text((x1 + 10, y1 + 6), name, fill=(255, 255, 255), font=font_class)
    # Attributes
    curr_y = y1 + 35
    for attr in attrs:
        draw.text((x1 + 10, curr_y), attr, fill=(33, 33, 33), font=font_attr)
        curr_y += 18

classes_data = [
    ("User", ["+ int id (PK)", "+ string name", "+ string email", "+ string phone", "+ string password_hash", "+ string role", "+ is_admin()", "+ is_customer()"], (40, 90, 240, 260), (27, 94, 32)),
    ("Address", ["+ int id (PK)", "+ int user_id (FK)", "+ string address", "+ string city", "+ string state", "+ string pincode"], (40, 290, 240, 440), (46, 125, 50)),
    ("Cart", ["+ int id (PK)", "+ int user_id (FK)", "+ datetime created_at"], (40, 470, 240, 560), (46, 125, 50)),
    ("CartItem", ["+ int id (PK)", "+ int cart_id (FK)", "+ int plant_id (FK)", "+ int quantity", "+ float price"], (40, 590, 240, 710), (46, 125, 50)),
    
    ("Category", ["+ int id (PK)", "+ string name", "+ string slug", "+ string description", "+ string image"], (300, 90, 540, 210), (21, 101, 192)),
    ("Plant", ["+ int id (PK)", "+ int category_id (FK)", "+ string name", "+ string scientific_name", "+ float price", "+ float discount", "+ int stock_quantity", "+ string sunlight", "+ string water_req", "+ string image", "+ final_price()"], (300, 240, 540, 480), (21, 101, 192)),
    ("Service", ["+ int id (PK)", "+ string name", "+ string description", "+ float price", "+ string status"], (300, 510, 540, 630), (0, 131, 143)),
    ("ServiceBooking", ["+ int id (PK)", "+ int service_id (FK)", "+ int user_id (FK)", "+ string booking_date", "+ string address", "+ string status"], (300, 660, 540, 800), (0, 131, 143)),

    ("Order", ["+ int id (PK)", "+ int user_id (FK)", "+ float total_amount", "+ float grand_total", "+ string payment_status", "+ string order_status", "+ int deliv_partner_id", "+ string deliv_address", "+ datetime created_at"], (600, 90, 840, 280), (106, 27, 154)),
    ("OrderItem", ["+ int id (PK)", "+ int order_id (FK)", "+ int plant_id (FK)", "+ int quantity", "+ float price", "+ string plant_name"], (600, 310, 840, 450), (106, 27, 154)),
    ("Payment", ["+ int id (PK)", "+ int order_id (FK)", "+ int user_id (FK)", "+ float amount", "+ string payment_method", "+ string transaction_id", "+ string payment_status"], (600, 480, 840, 630), (106, 27, 154)),
    ("DeliveryPartner", ["+ int id (PK)", "+ int user_id (FK)", "+ string avail_status", "+ string current_status", "+ string vehicle_type"], (600, 660, 840, 790), (230, 81, 0))
]

for name, attrs, coords, bg in classes_data:
    draw_class(name, attrs, coords, bg)

# Draw Relationship Lines
def draw_rel(c1, c2, label="1..*"):
    x1 = (c1[0] + c1[2]) // 2
    y1 = (c1[1] + c1[3]) // 2
    x2 = (c2[0] + c2[2]) // 2
    y2 = (c2[1] + c2[3]) // 2
    draw.line([(x1, y1), (x2, y2)], fill=(100, 100, 100), width=2)

# User Relationships
draw.line([(140, 260), (140, 290)], fill=(100, 100, 100), width=2) # User -> Address
draw.line([(140, 440), (140, 470)], fill=(100, 100, 100), width=2) # User -> Cart
draw.line([(240, 175), (600, 185)], fill=(100, 100, 100), width=2) # User -> Order
draw.line([(140, 560), (140, 590)], fill=(100, 100, 100), width=2) # Cart -> CartItem

# Category -> Plant
draw.line([(420, 210), (420, 240)], fill=(100, 100, 100), width=2)

# Order -> OrderItem & Payment
draw.line([(720, 280), (720, 310)], fill=(100, 100, 100), width=2) # Order -> OrderItem
draw.line([(720, 450), (720, 480)], fill=(100, 100, 100), width=2) # Order -> Payment

# Service -> ServiceBooking
draw.line([(420, 630), (420, 660)], fill=(100, 100, 100), width=2)

# Credit Footer
draw.rectangle([0, 890, 1100, 950], fill=(27, 94, 32))
draw.text((400, 910), "Project Done By Shamitha - GreenCart UML Class Diagram", fill=(255, 255, 255), font=get_font(14, bold=True))

# Save image
out_png = os.path.join(output_dir, "class_diagram.png")
img.save(out_png)
print(f"Saved Class Diagram PNG: {out_png}")
