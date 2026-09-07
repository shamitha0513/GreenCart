import os
from PIL import Image, ImageDraw, ImageFont

base_dir = r"c:\Users\lenovo\Downloads\GreenCart"
services_dir = os.path.join(base_dir, "app", "static", "images", "services")
os.makedirs(services_dir, exist_ok=True)

def get_font(size=20, bold=False):
    try:
        if bold:
            return ImageFont.truetype("arialbd.ttf", size)
        return ImageFont.truetype("arial.ttf", size)
    except IOError:
        return ImageFont.load_default()

SERVICES_INFO = [
    ("consultation", "PLANT CONSULTATION", "1-on-1 Health & Soil Diagnosis", (20, 82, 40), (45, 106, 79)),
    ("maintenance", "GARDEN MAINTENANCE", "Pruning, Cleaning & Fertilizing", (45, 106, 79), (82, 183, 136)),
    ("repotting", "PLANT REPOTTING", "Nutrient Soil & Pot Upgrades", (116, 83, 62), (147, 102, 75)),
    ("delivery", "DELIVERY & SETUP", "Safe Transport & Placement", (21, 101, 192), (30, 136, 229)),
    ("garden", "GARDEN DESIGN", "Terrace & Balcony Transformation", (46, 125, 50), (76, 175, 80)),
    ("indoor", "INDOOR STYLING", "Living Room Green Decor", (106, 27, 154), (142, 36, 170)),
    ("office", "OFFICE GREENERY", "Corporate Air Quality Setup", (0, 105, 92), (0, 137, 123)),
    ("health", "PLANT EMERGENCY", "Pest Treatment & Care", (198, 40, 40), (229, 57, 53))
]

font_title = get_font(26, bold=True)
font_sub = get_font(15, bold=False)
font_tag = get_font(13, bold=True)

for slug, title, sub, color1, color2 in SERVICES_INFO:
    # Create 600x400 high resolution cover image
    img = Image.new('RGB', (600, 400), color=color1)
    draw = ImageDraw.Draw(img)
    
    # Draw subtle decorative background pattern
    for y in range(0, 400, 40):
        draw.line([(0, y), (600, y+100)], fill=(color2[0], color2[1], color2[2]), width=2)
        
    # Draw central elegant service card banner
    draw.rectangle([40, 60, 560, 340], fill=(255, 255, 255), outline=(240, 240, 240), width=4)
    
    # Top Tag
    draw.rectangle([80, 80, 520, 115], fill=color1)
    draw.text((160, 88), "GREENCART PLANT SERVICES", fill=(255, 255, 255), font=font_tag)
    
    # Service Title & Subtitle
    draw.text((80, 150), title, fill=(33, 33, 33), font=font_title)
    draw.text((80, 200), sub, fill=(100, 100, 100), font=font_sub)
    
    # Bottom Verified Badge
    draw.rectangle([80, 260, 280, 300], fill=(232, 245, 233), outline=(76, 175, 80), width=2)
    draw.text((95, 272), "✓ Verified Expert Service", fill=(46, 125, 50), font=font_tag)
    
    # Save as both .jpg and .svg so legacy requests load the dedicated service cover photo
    jpg_path = os.path.join(services_dir, f"{slug}.jpg")
    svg_path = os.path.join(services_dir, f"{slug}.svg")
    
    img.save(jpg_path, 'JPEG', quality=95)
    img.save(svg_path, 'JPEG', quality=95)
    print(f"Generated Dedicated Service Cover: {slug}.jpg")

print("All 8 Dedicated Service Cover Photos generated successfully!")
