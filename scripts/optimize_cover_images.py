#!/usr/bin/env python3
"""
Script pour optimiser la sélection des images de couverture
Sélectionne les images qui montrent le maillot de face plutôt que les détails
"""

import json
import os
import re
from pathlib import Path

def analyze_image_filename(filename):
    """
    Analyse le nom de fichier pour déterminer le type d'image
    Retourne un score (plus élevé = meilleure image de couverture)
    """
    filename_lower = filename.lower()
    score = 0
    
    # Mots-clés qui indiquent une vue complète du maillot
    front_keywords = [
        'front', 'face', 'complet', 'full', 'entier', 'maillot', 'jersey'
    ]
    
    # Mots-clés qui indiquent des détails (à éviter)
    detail_keywords = [
        'blason', 'logo', 'crest', 'detail', 'close', 'proche', 'badge', 'sponsor'
    ]
    
    # Mots-clés pour les vues spécifiques
    view_keywords = {
        'front': 10,      # Vue de face
        'back': 8,        # Vue de dos
        'side': 6,        # Vue de côté
        'main': 9,        # Image principale
        'hero': 10,       # Image héro
        'cover': 10,      # Image de couverture
    }
    
    # Analyser les mots-clés positifs
    for keyword in front_keywords:
        if keyword in filename_lower:
            score += 5
    
    # Analyser les vues spécifiques
    for keyword, points in view_keywords.items():
        if keyword in filename_lower:
            score += points
    
    # Analyser les mots-clés négatifs (détails)
    for keyword in detail_keywords:
        if keyword in filename_lower:
            score -= 8
    
    # Préférer les images avec des numéros plus bas (généralement les principales)
    number_match = re.search(r'(\d+)\.jpg$', filename)
    if number_match:
        number = int(number_match.group(1))
        if number == 0:
            score += 5  # Image 0 est souvent la principale
        elif number <= 2:
            score += 3  # Images 1-2 sont souvent bonnes
        else:
            score += 1  # Images 3+ sont souvent des détails
    
    # Préférer les images plus grandes (indication de qualité)
    if 'hd' in filename_lower:
        score += 2
    
    return score

def select_best_cover_image(images):
    """
    Sélectionne la meilleure image de couverture parmi une liste d'images
    """
    if not images:
        return None
    
    # Analyser toutes les images
    image_scores = []
    for image in images:
        score = analyze_image_filename(image)
        image_scores.append((image, score))
    
    # Trier par score (décroissant)
    image_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Retourner la meilleure image
    best_image = image_scores[0][0]
    print(f"  Meilleure image sélectionnée: {best_image} (score: {image_scores[0][1]})")
    
    return best_image

def optimize_jerseys_cover_images():
    """
    Optimise les images de couverture pour tous les maillots
    """
    print("🔄 Optimisation des images de couverture...")
    
    # Charger les données des maillots
    jerseys_file = Path("data/jerseys.json")
    if not jerseys_file.exists():
        print("❌ Fichier jerseys.json non trouvé")
        return
    
    with open(jerseys_file, 'r', encoding='utf-8') as f:
        jerseys = json.load(f)
    
    print(f"📊 {len(jerseys)} maillots trouvés")
    
    updated_count = 0
    
    for jersey in jerseys:
        jersey_id = jersey.get('id', 'inconnu')
        current_thumbnail = jersey.get('thumbnail', '')
        images = jersey.get('images', [])
        
        print(f"\n🔍 Maillot {jersey_id}:")
        print(f"  Image actuelle: {current_thumbnail}")
        print(f"  Images disponibles: {len(images)}")
        
        if not images:
            print("  ⚠️ Aucune image disponible")
            continue
        
        # Sélectionner la meilleure image de couverture
        best_image = select_best_cover_image(images)
        
        if best_image and best_image != current_thumbnail:
            jersey['thumbnail'] = best_image
            updated_count += 1
            print(f"  ✅ Mise à jour: {current_thumbnail} → {best_image}")
        else:
            print(f"  ✅ Déjà optimisé: {current_thumbnail}")
    
    # Sauvegarder les modifications
    with open(jerseys_file, 'w', encoding='utf-8') as f:
        json.dump(jerseys, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 Optimisation terminée!")
    print(f"📈 {updated_count} maillots mis à jour")
    print(f"💾 Données sauvegardées dans {jerseys_file}")

def preview_optimization():
    """
    Aperçu de l'optimisation sans modification
    """
    print("👀 Aperçu de l'optimisation des images de couverture...")
    
    jerseys_file = Path("data/jerseys.json")
    if not jerseys_file.exists():
        print("❌ Fichier jerseys.json non trouvé")
        return
    
    with open(jerseys_file, 'r', encoding='utf-8') as f:
        jerseys = json.load(f)
    
    print(f"📊 {len(jerseys)} maillots trouvés\n")
    
    for i, jersey in enumerate(jerseys[:5]):  # Afficher seulement les 5 premiers
        jersey_id = jersey.get('id', 'inconnu')
        current_thumbnail = jersey.get('thumbnail', '')
        images = jersey.get('images', [])
        
        print(f"🔍 Maillot {jersey_id}:")
        print(f"  Image actuelle: {current_thumbnail}")
        
        if images:
            best_image = select_best_cover_image(images)
            if best_image != current_thumbnail:
                print(f"  🎯 Recommandation: {best_image}")
            else:
                print(f"  ✅ Déjà optimal")
        else:
            print(f"  ⚠️ Aucune image disponible")
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--preview":
        preview_optimization()
    else:
        optimize_jerseys_cover_images()
