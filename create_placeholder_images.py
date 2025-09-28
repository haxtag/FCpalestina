#!/usr/bin/env python3
"""
Générateur d'images placeholder pour les maillots de test
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_images():
    """Créer des images placeholder pour les maillots de test"""
    
    # Dossier des images
    images_dir = os.path.join(os.path.dirname(__file__), 'assets', 'images', 'jerseys')
    os.makedirs(images_dir, exist_ok=True)
    
    # Couleurs par catégorie
    category_colors = {
        'home': '#8B1538',      # Rouge FC Palestina
        'away': '#FFFFFF',      # Blanc
        'third': '#000000',     # Noir
        'keeper': '#00FF00',    # Vert gardien
        'special': '#FFD700',   # Or spécial
        'vintage': '#8B4513'    # Marron vintage
    }
    
    categories = ['home', 'away', 'third', 'keeper', 'special', 'vintage']
    
    print("🎨 Création des images placeholder...")
    
    for jersey_num in range(1, 26):  # 25 maillots de test
        # Déterminer la catégorie (cyclique)
        category = categories[(jersey_num - 1) % len(categories)]
        base_color = category_colors[category]
        
        for img_num in range(3):  # 3 images par maillot
            filename = f"test-jersey-{jersey_num:03d}-hd-{img_num}.jpg"
            filepath = os.path.join(images_dir, filename)
            
            # Créer une image 600x600
            img = Image.new('RGB', (600, 600), base_color)
            draw = ImageDraw.Draw(img)
            
            # Dessiner un maillot simple
            if category == 'away' and base_color == '#FFFFFF':
                # Pour les maillots blancs, ajouter un contour
                draw.rectangle([50, 100, 550, 500], fill=base_color, outline='#8B1538', width=5)
            else:
                draw.rectangle([50, 100, 550, 500], fill=base_color)
            
            # Ajouter le numéro du maillot
            try:
                # Essayer d'utiliser une police système
                font = ImageFont.truetype("arial.ttf", 48)
            except:
                # Fallback sur la police par défaut
                font = ImageFont.load_default()
            
            text = f"#{jersey_num}"
            text_color = '#FFFFFF' if base_color != '#FFFFFF' else '#8B1538'
            
            # Centrer le texte
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (600 - text_width) // 2
            text_y = 280
            
            draw.text((text_x, text_y), text, fill=text_color, font=font)
            
            # Ajouter le nom de la catégorie
            cat_text = category.upper()
            cat_bbox = draw.textbbox((0, 0), cat_text, font=font)
            cat_width = cat_bbox[2] - cat_bbox[0]
            cat_x = (600 - cat_width) // 2
            cat_y = 350
            
            draw.text((cat_x, cat_y), cat_text, fill=text_color, font=font)
            
            # Ajouter une variation pour chaque image
            if img_num == 1:
                # Image 1: ajouter des bandes
                for i in range(0, 600, 30):
                    draw.line([(i, 0), (i, 600)], fill=(255,255,255,25), width=2)
            elif img_num == 2:
                # Image 2: ajouter un logo FC Palestine
                draw.ellipse([250, 150, 350, 250], fill=text_color, outline=base_color, width=3)
                # Créer une nouvelle font plus petite pour le logo
                try:
                    logo_font = ImageFont.truetype("arial.ttf", 24)
                except:
                    logo_font = ImageFont.load_default()
                draw.text((285, 185), "FCP", fill=base_color, font=logo_font)
            
            # Sauvegarder l'image
            img.save(filepath, 'JPEG', quality=85)
            
        print(f"✅ Images créées pour maillot {jersey_num:03d} ({category})")
    
    print(f"🎉 {25 * 3} images placeholder créées dans {images_dir}")

if __name__ == "__main__":
    create_placeholder_images()