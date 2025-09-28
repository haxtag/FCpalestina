#!/usr/bin/env python3
"""
Script pour optimiser la sélection des images principales
"""

import json
import os
import re
from typing import List, Dict

def analyze_image_filename(filename: str) -> Dict:
    """Analyse un nom de fichier d'image pour déterminer sa qualité"""
    score = 0
    characteristics = {
        'is_main': False,
        'is_square': False,
        'is_medium': False,
        'is_small': False,
        'has_number': False,
        'filename': filename
    }
    
    filename_lower = filename.lower()
    
    # Analyser les caractéristiques du nom de fichier
    if 'main' in filename_lower:
        characteristics['is_main'] = True
        score += 10
    
    if 'square' in filename_lower:
        characteristics['is_square'] = True
        score += 3  # Les images carrées sont souvent des vignettes
    
    if 'medium' in filename_lower:
        characteristics['is_medium'] = True
        score += 8  # Les images medium sont souvent de bonne qualité
    
    if 'small' in filename_lower:
        characteristics['is_small'] = True
        score += 2  # Les images small sont souvent de faible qualité
    
    # Chercher des numéros dans le nom
    if re.search(r'-\d+\.', filename):
        characteristics['has_number'] = True
        score += 1
    
    # Les images sans suffixe spécial sont souvent les meilleures
    if not any(suffix in filename_lower for suffix in ['main', 'square', 'medium', 'small']):
        score += 5
    
    characteristics['score'] = score
    return characteristics

def select_best_thumbnail(images: List[str]) -> str:
    """Sélectionne la meilleure image comme vignette"""
    if not images:
        return ""
    
    if len(images) == 1:
        return images[0]
    
    # Analyser toutes les images
    analyzed_images = [analyze_image_filename(img) for img in images]
    
    # Trier par score (plus haut = meilleur)
    analyzed_images.sort(key=lambda x: x['score'], reverse=True)
    
    # Retourner la meilleure image
    best_image = analyzed_images[0]
    print(f"  Meilleure image sélectionnée: {best_image['filename']} (score: {best_image['score']})")
    
    return best_image['filename']

def optimize_jerseys_thumbnails():
    """Optimise les vignettes de tous les maillots"""
    try:
        # Lire le fichier jerseys.json
        with open('data/jerseys.json', 'r', encoding='utf-8') as f:
            jerseys = json.load(f)
        
        print("Optimisation des vignettes des maillots")
        print("=" * 50)
        
        optimized_count = 0
        
        for jersey in jerseys:
            original_thumbnail = jersey.get('thumbnail', '')
            images = jersey.get('images', [])
            
            if not images:
                continue
            
            # Sélectionner la meilleure image comme vignette
            best_thumbnail = select_best_thumbnail(images)
            
            if best_thumbnail and best_thumbnail != original_thumbnail:
                jersey['thumbnail'] = best_thumbnail
                optimized_count += 1
                print(f"✅ {jersey['title'][:50]}...")
                print(f"   Ancienne: {original_thumbnail}")
                print(f"   Nouvelle: {best_thumbnail}")
                print()
        
        # Sauvegarder les modifications
        with open('data/jerseys.json', 'w', encoding='utf-8') as f:
            json.dump(jerseys, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {optimized_count} vignettes optimisées !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("Optimisation des vignettes des maillots")
    print("=" * 50)
    
    success = optimize_jerseys_thumbnails()
    
    if success:
        print("\n🎉 Optimisation terminée !")
        print("Les vignettes ont été sélectionnées pour montrer le meilleur angle de chaque maillot.")
    else:
        print("\n❌ Échec de l'optimisation")

if __name__ == "__main__":
    main()
