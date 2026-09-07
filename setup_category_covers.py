import os
from PIL import Image, ImageDraw, ImageFont

# Set paths
base_dir = r"c:\Users\lenovo\Downloads\GreenCart"
plants_dir = os.path.join(base_dir, "app", "static", "images", "plants")
cat_dir = os.path.join(base_dir, "app", "static", "images", "categories")
os.makedirs(cat_dir, exist_ok=True)

# Map category slugs to representative JPG images from plants folder
CATEGORY_IMAGE_MAP = {
    "indoor-plants": "1788814789_13._Monstera_Deliciosa.jpg",
    "outdoor-plants": "1788814486_15._Bougainvillea_Pink.jpg",
    "flowering-plants": "1788814037_15._Red_Rose_Bush.jpg",
    "herbal-plants": "1788813617_15._Sweet_Basil.jpg",
    "medicinal-plants": "1788813392_Aloe_Vera_Gel_Plant.jpg",
    "succulents": "1788812960_Jade_Plant.jpg",
    "air-purifying-plants": "1788812552_Snake_Plant_Laurentii.jpg",
    "ornamental-plants": "1788811916_Philodendron_Pink_Princess.jpg",
    "fruit-plants": "1788811313_Pomegranate_Bhagwa.jpg",
    "vegetable-plants": "1788810717_Tomato_Cherry_Red.jpg",
    "cactus-plants": "1788810129_Golden_Barrel_Cactus.jpg",
    "bonsai-plants": "1788808867_Japanese_Red_Maple_Bonsai.jpg"
}

for cat_slug, plant_img_filename in CATEGORY_IMAGE_MAP.items():
    src_path = os.path.join(plants_dir, plant_img_filename)
    dst_path = os.path.join(cat_dir, f"{cat_slug}.jpg")
    
    if os.path.exists(src_path):
        # Open, crop to nice 600x400 aspect ratio if needed, and save as category cover
        img = Image.open(src_path)
        img = img.convert('RGB')
        img.save(dst_path, 'JPEG', quality=95)
        print(f"Created category cover: {dst_path}")
    else:
        print(f"Warning: source plant image not found: {src_path}")

print("Category cover images setup complete!")
