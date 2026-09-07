import os
from PIL import Image, ImageDraw, ImageFont

base_dir = r"c:\Users\lenovo\Downloads\GreenCart"
plants_dir = os.path.join(base_dir, "app", "static", "images", "plants")
services_dir = os.path.join(base_dir, "app", "static", "images", "services")
os.makedirs(services_dir, exist_ok=True)

# Map service filenames to representative JPG plant images from plant catalog
SERVICE_IMAGE_MAP = {
    "consultation.jpg": "1788813382_Holy_Basil_Tulsi.jpg",
    "maintenance.jpg": "1788814755_9._Fiddle_Leaf_Fig.jpg",
    "repotting.jpg": "1788814789_13._Monstera_Deliciosa.jpg",
    "delivery.jpg": "1788812521_Areca_Palm_Air_Cleanser.jpg",
    "garden.jpg": "1788814486_15._Bougainvillea_Pink.jpg",
    "indoor.jpg": "1788814746_8._Rubber_Plant.jpg",
    "office.jpg": "1788812406_Weeping_Fig_Ficus.jpg",
    "health.jpg": "1788813392_Aloe_Vera_Gel_Plant.jpg"
}

for service_jpg, plant_img_filename in SERVICE_IMAGE_MAP.items():
    src_path = os.path.join(plants_dir, plant_img_filename)
    dst_path = os.path.join(services_dir, service_jpg)
    
    if os.path.exists(src_path):
        img = Image.open(src_path).convert('RGB')
        img.save(dst_path, 'JPEG', quality=95)
        print(f"Created Service Cover: {dst_path}")
    else:
        print(f"Warning: source image not found for {service_jpg}")

print("All 8 Plant Service JPG Cover Photos created successfully!")
