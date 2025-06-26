# Créé par Viple SAS
from PIL import Image, ImageDraw, ImageFont
import os

def create_viple_icon():
    """Crée une icône personnalisée pour Viple"""
    
    # Couleurs Viple
    bg_color = '#2E86C1'  # Bleu Viple
    text_color = 'white'
    
    # Créer une image PNG 64x64 pour l'icône principale
    size = 64
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Dessiner un cercle bleu
    circle_margin = 4
    draw.ellipse([
        circle_margin, circle_margin, 
        size - circle_margin, size - circle_margin
    ], fill=bg_color, outline=text_color, width=2)
    
    # Ajouter la lettre "V" au centre
    try:
        # Essayer d'utiliser une police système
        font_size = 32
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Police par défaut si arial n'est pas disponible
        font = ImageFont.load_default()
    
    # Calculer la position pour centrer le "V"
    text = "V"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 2  # Ajustement visuel
    
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Sauvegarder l'icône PNG
    png_path = "viple_icon.png"
    image.save(png_path, "PNG")
    print(f"✓ Icône PNG créée : {png_path}")
    
    # Créer un fichier ICO avec plusieurs tailles
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    icons = []
    
    for icon_size in icon_sizes:
        icon_image = Image.new('RGBA', icon_size, (0, 0, 0, 0))
        icon_draw = ImageDraw.Draw(icon_image)
        
        # Cercle adapté à la taille
        margin = max(1, icon_size[0] // 16)
        icon_draw.ellipse([
            margin, margin,
            icon_size[0] - margin, icon_size[1] - margin
        ], fill=bg_color, outline=text_color, width=max(1, icon_size[0] // 32))
        
        # Texte adapté à la taille
        try:
            font_size = max(8, icon_size[0] // 2)
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = icon_draw.textbbox((0, 0), "V", font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (icon_size[0] - text_width) // 2
        y = (icon_size[1] - text_height) // 2
        
        icon_draw.text((x, y), "V", fill=text_color, font=font)
        icons.append(icon_image)
    
    # Sauvegarder le fichier ICO
    ico_path = "viple_icon.ico"
    icons[0].save(ico_path, format='ICO', sizes=[(icon.width, icon.height) for icon in icons])
    print(f"✓ Icône ICO créée : {ico_path}")
    
    return png_path, ico_path

if __name__ == "__main__":
    create_viple_icon()