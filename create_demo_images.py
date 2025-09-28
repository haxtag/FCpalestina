#!/usr/bin/env python3
"""
Créateur d'images de démonstration pour FC Palestina
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_demo_image(text, filename, size=(400, 300), bg_color=(44, 85, 48), text_color=(255, 255, 255)):
    """Créer une image de démonstration"""
    # Créer l'image
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Essayer de charger une police, sinon utiliser la police par défaut
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Centrer le texte
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Dessiner le texte
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Ajouter un cadre
    draw.rectangle([5, 5, size[0]-5, size[1]-5], outline=(255, 255, 255), width=2)
    
    # Sauvegarder
    os.makedirs('assets/images/jerseys', exist_ok=True)
    img.save(f'assets/images/jerseys/{filename}')
    print(f"✅ Image créée: {filename}")

def main():
    print("🎨 Création d'images de démonstration FC Palestina")
    print("=" * 50)
    
    # Couleurs pour différents types de maillots
    colors = [
        ((44, 85, 48), "Maillot Domicile 2024", "jersey-home-2024-1.jpg"),      # Vert FC Palestina
        ((255, 255, 255), "Maillot Extérieur 2024", "jersey-away-2024-1.jpg"),  # Blanc
        ((255, 107, 53), "Maillot Spécial Liberté", "jersey-special-2024-1.jpg"), # Orange
        ((139, 69, 19), "Maillot Vintage 1990", "jersey-vintage-1990-1.jpg"),   # Marron
        ((255, 215, 0), "Maillot Gardien 2024", "jersey-keeper-2024-1.jpg"),    # Or
        ((220, 20, 60), "Maillot Célébration 2023", "jersey-celebration-2023-1.jpg") # Rouge
    ]
    
    for bg_color, text, filename in colors:
        # Choisir la couleur du texte selon la couleur de fond
        if bg_color == (255, 255, 255):  # Fond blanc
            text_color = (44, 85, 48)    # Texte vert
        else:
            text_color = (255, 255, 255) # Texte blanc
        
        create_demo_image(text, filename, bg_color=bg_color, text_color=text_color)
    
    print(f"\n🎯 {len(colors)} images de démonstration créées !")
    print("📁 Dossier: assets/images/jerseys/")
    print("🌐 Rechargez votre site pour voir les maillots")

if __name__ == "__main__":
    main()
