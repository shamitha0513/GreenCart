import os
from PIL import Image

base_dir = r"c:\Users\lenovo\Downloads\GreenCart"
plants_dir = os.path.join(base_dir, "app", "static", "images", "plants")
cat_dir = os.path.join(base_dir, "app", "static", "images", "categories")
services_dir = os.path.join(base_dir, "app", "static", "images", "services")

# 12 Categories to real plant photos
CAT_MAP = {
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

for cat_slug, plant_file in CAT_MAP.items():
    src = os.path.join(plants_dir, plant_file)
    if os.path.exists(src):
        img = Image.open(src).convert('RGB')
        
        # Save as .jpg
        jpg_dst = os.path.join(cat_dir, f"{cat_slug}.jpg")
        img.save(jpg_dst, 'JPEG', quality=95)
        
        # ALSO save as .svg replacement so any legacy request to .svg serves the real photo!
        svg_dst = os.path.join(cat_dir, f"{cat_slug}.svg")
        img.save(svg_dst, 'JPEG', quality=95)
        print(f"Replaced category image: {cat_slug}")

# 8 Services to real photos
SERV_MAP = {
    "consultation": "1788813382_Holy_Basil_Tulsi.jpg",
    "maintenance": "1788814755_9._Fiddle_Leaf_Fig.jpg",
    "repotting": "1788814789_13._Monstera_Deliciosa.jpg",
    "delivery": "1788812521_Areca_Palm_Air_Cleanser.jpg",
    "garden": "1788814486_15._Bougainvillea_Pink.jpg",
    "indoor": "1788814746_8._Rubber_Plant.jpg",
    "office": "1788812406_Weeping_Fig_Ficus.jpg",
    "health": "1788813392_Aloe_Vera_Gel_Plant.jpg"
}

for serv_name, plant_file in SERV_MAP.items():
    src = os.path.join(plants_dir, plant_file)
    if os.path.exists(src):
        img = Image.open(src).convert('RGB')
        
        jpg_dst = os.path.join(services_dir, f"{serv_name}.jpg")
        img.save(jpg_dst, 'JPEG', quality=95)
        
        svg_dst = os.path.join(services_dir, f"{serv_name}.svg")
        img.save(svg_dst, 'JPEG', quality=95)
        print(f"Replaced service image: {serv_name}")

print("REPLACED ALL GREEN SVG GRAPHICS WITH REAL NATURAL PLANT PHOTOS!")
