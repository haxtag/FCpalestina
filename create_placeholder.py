#!/usr/bin/env python3
"""
Crée une image placeholder simple pour les maillots sans image
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder():
    """Crée une image placeholder 400x400"""
    
    # Dimensions
    width, height = 400, 400
    
    # Couleurs (vert Palestine)
    bg_color = (44, 85, 48)  # Vert foncé
    text_color = (255, 255, 255)  # Blanc
    
    # Créer l'image
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Dessiner un cadre
    border_width = 10
    draw.rectangle(
        [(border_width, border_width), (width-border_width, height-border_width)],
        outline=(141, 21, 56),  # Rouge Palestine
        width=border_width
    )
    
    # Ajouter du texte
    text = "FC PALESTINA"
    
    try:
        # Essayer avec une police système
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        # Fallback sur police par défaut
        font = ImageFont.load_default()
    
    # Calculer la position du texte (centré)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Dessiner le texte
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Sauvegarder
    output_path = 'assets/img/placeholder.jpg'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, 'JPEG', quality=85)
    print(f"✅ Placeholder créé: {output_path}")
    
    return output_path

if __name__ == "__main__":
    create_placeholder()
    print("🎉 Terminé!")
