#!/usr/bin/env python3
"""
Script d'optimisation des images téléchargées
"""

import os
import json
from PIL import Image
import io

def optimize_jersey_images():
    """Optimise toutes les images de maillots"""
    
    print("🖼️ Optimisation des images de maillots...")
    print("=" * 40)
    
    # Dossier des images
    images_dir = "assets/images/jerseys"
    
    if not os.path.exists(images_dir):
        print(f"❌ Dossier {images_dir} introuvable")
        return False
    
    # Lister toutes les images
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    
    if not image_files:
        print("❌ Aucune image trouvée")
        return False
    
    print(f"📁 {len(image_files)} images trouvées")
    
    optimized_count = 0
    error_count = 0
    
    for image_file in image_files:
        image_path = os.path.join(images_dir, image_file)
        
        try:
            # Ouvrir l'image
            with Image.open(image_path) as img:
                # Convertir en RGB si nécessaire
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionner si trop grande (max 800px de largeur)
                if img.width > 800:
                    ratio = 800 / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((800, new_height), Image.Resampling.LANCZOS)
                
                # Sauvegarder avec optimisation
                output_path = image_path.replace('.png', '.jpg').replace('.webp', '.jpg')
                
                # Sauvegarder en JPEG avec qualité optimisée
                img.save(output_path, 'JPEG', quality=85, optimize=True)
                
                # Supprimer l'ancien fichier si c'était un PNG ou WebP
                if output_path != image_path:
                    os.remove(image_path)
                
                optimized_count += 1
                print(f"   ✅ {image_file} optimisé")
                
        except Exception as e:
            error_count += 1
            print(f"   ❌ Erreur sur {image_file}: {e}")
    
    print(f"\n📊 Résultat:")
    print(f"   • Images optimisées: {optimized_count}")
    print(f"   • Erreurs: {error_count}")
    
    return optimized_count > 0

def create_thumbnails():
    """Crée des miniatures pour la galerie"""
    
    print("\n🖼️ Création des miniatures...")
    print("=" * 30)
    
    # Dossiers
    source_dir = "assets/images/jerseys"
    thumb_dir = "assets/images/thumbnails"
    
    # Créer le dossier thumbnails
    os.makedirs(thumb_dir, exist_ok=True)
    
    # Lister les images
    image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print("❌ Aucune image source trouvée")
        return False
    
    thumbnail_count = 0
    
    for image_file in image_files:
        source_path = os.path.join(source_dir, image_file)
        thumb_path = os.path.join(thumb_dir, image_file)
        
        try:
            with Image.open(source_path) as img:
                # Créer une miniature 300x300
                img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                
                # Sauvegarder
                img.save(thumb_path, 'JPEG', quality=80, optimize=True)
                
                thumbnail_count += 1
                print(f"   ✅ Miniature créée: {image_file}")
                
        except Exception as e:
            print(f"   ❌ Erreur sur {image_file}: {e}")
    
    print(f"\n📊 {thumbnail_count} miniatures créées")
    return thumbnail_count > 0

def main():
    """Fonction principale"""
    
    print("🔧 Optimisation des images")
    print("=" * 25)
    
    # Optimiser les images
    if optimize_jersey_images():
        print("✅ Images optimisées avec succès")
    else:
        print("❌ Échec de l'optimisation")
    
    # Créer les miniatures
    if create_thumbnails():
        print("✅ Miniatures créées avec succès")
    else:
        print("❌ Échec de la création des miniatures")
    
    print("\n🎉 Optimisation terminée !")

if __name__ == "__main__":
    main()
