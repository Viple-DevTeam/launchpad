# Créé par Viple SAS
from PIL import Image, ImageDraw, ImageFilter
import os

def create_landscape_background():
    """Crée une image de paysage pour le fond du widget"""
    
    # Dimensions du widget
    width, height = 280, 160
    
    # Créer l'image de base
    image = Image.new('RGB', (width, height), '#87CEEB')  # Bleu ciel
    draw = ImageDraw.Draw(image)
    
    # Dessiner le ciel avec dégradé
    for y in range(height // 2):
        # Dégradé du bleu ciel vers un bleu plus clair
        blue_intensity = 135 + (y * 30 // (height // 2))
        color = (135, 206, min(235 + y//2, 255))
        draw.line([(0, y), (width, y)], fill=color)
    
    # Dessiner des montagnes en arrière-plan
    mountain_points = [
        (0, height//2 + 20),
        (50, height//2 - 10),
        (100, height//2 + 5),
        (150, height//2 - 15),
        (200, height//2 + 10),
        (width, height//2 + 15),
        (width, height),
        (0, height)
    ]
    draw.polygon(mountain_points, fill='#4A4A4A')
    
    # Ajouter des montagnes plus proches (plus claires)
    mountain2_points = [
        (0, height//2 + 40),
        (80, height//2 + 10),
        (140, height//2 + 25),
        (200, height//2 + 5),
        (width, height//2 + 30),
        (width, height),
        (0, height)
    ]
    draw.polygon(mountain2_points, fill='#6B6B6B')
    
    # Dessiner de l'herbe/prairie au premier plan
    grass_points = [
        (0, height - 30),
        (width, height - 25),
        (width, height),
        (0, height)
    ]
    draw.polygon(grass_points, fill='#228B22')
    
    # Ajouter quelques nuages simples
    cloud_color = (255, 255, 255, 180)
    
    # Nuage 1
    cloud1_x, cloud1_y = 40, 25
    for i in range(5):
        x = cloud1_x + i * 8
        y = cloud1_y + (i % 2) * 3
        draw.ellipse([x, y, x + 20, y + 12], fill=(255, 255, 255))
    
    # Nuage 2
    cloud2_x, cloud2_y = 180, 35
    for i in range(4):
        x = cloud2_x + i * 10
        y = cloud2_y + (i % 2) * 2
        draw.ellipse([x, y, x + 18, y + 10], fill=(255, 255, 255))
    
    # Ajouter un léger effet de texture
    image = image.filter(ImageFilter.SMOOTH)
    
    # Sauvegarder l'image
    bg_path = "viple_background.png"
    image.save(bg_path, "PNG")
    print(f"✓ Image de fond créée : {bg_path}")
    
    return bg_path

def create_abstract_background():
    """Crée un fond abstrait alternatif"""
    width, height = 280, 160
    
    image = Image.new('RGB', (width, height), '#1E3A8A')  # Bleu foncé
    draw = ImageDraw.Draw(image)
    
    # Dégradé diagonal
    for x in range(width):
        for y in range(height):
            # Calcul de couleur basé sur la position
            r = min(30 + (x * 100 // width), 100)
            g = min(60 + (y * 150 // height), 180)
            b = min(140 + ((x + y) * 80 // (width + height)), 220)
            
            if (x + y) % 20 < 10:  # Effet de texture
                draw.point((x, y), (r, g, b))
            else:
                draw.point((x, y), (r-10, g-10, b-10))
    
    # Ajouter des formes géométriques
    draw.ellipse([width//4, height//4, 3*width//4, 3*height//4], 
                outline=(255, 255, 255, 100), width=2)
    
    bg_path = "viple_background_abstract.png"
    image.save(bg_path, "PNG")
    print(f"✓ Image de fond abstraite créée : {bg_path}")
    
    return bg_path

if __name__ == "__main__":
    create_landscape_background()
    create_abstract_background()