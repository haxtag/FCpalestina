#!/usr/bin/env python3
"""
Script pour vérifier et ajuster manuellement les images de couverture
"""

import json
import os
from pathlib import Path

def check_cover_images():
    """
    Vérifie les images de couverture actuelles et propose des alternatives
    """
    print("🔍 Vérification des images de couverture...")
    
    # Charger les données des maillots
    jerseys_file = Path("data/jerseys.json")
    if not jerseys_file.exists():
        print("❌ Fichier jerseys.json non trouvé")
        return
    
    with open(jerseys_file, 'r', encoding='utf-8') as f:
        jerseys = json.load(f)
    
    print(f"📊 {len(jerseys)} maillots trouvés\n")
    
    for i, jersey in enumerate(jerseys):
        jersey_id = jersey.get('id', 'inconnu')
        title = jersey.get('title', 'Sans titre')
        current_thumbnail = jersey.get('thumbnail', '')
        images = jersey.get('images', [])
        
        print(f"🏆 Maillot {i+1}/{len(jerseys)}: {title}")
        print(f"   ID: {jersey_id}")
        print(f"   Image actuelle: {current_thumbnail}")
        
        if images:
            print(f"   Images disponibles ({len(images)}):")
            for j, image in enumerate(images):
                marker = "👑" if image == current_thumbnail else "  "
                print(f"   {marker} {j+1}. {image}")
        else:
            print("   ⚠️ Aucune image disponible")
        
        print("-" * 50)

def suggest_cover_changes():
    """
    Suggère des changements d'images de couverture basés sur des règles
    """
    print("💡 Suggestions d'amélioration des images de couverture...")
    
    jerseys_file = Path("data/jerseys.json")
    if not jerseys_file.exists():
        print("❌ Fichier jerseys.json non trouvé")
        return
    
    with open(jerseys_file, 'r', encoding='utf-8') as f:
        jerseys = json.load(f)
    
    suggestions = []
    
    for jersey in jerseys:
        jersey_id = jersey.get('id', 'inconnu')
        current_thumbnail = jersey.get('thumbnail', '')
        images = jersey.get('images', [])
        
        # Règles de suggestion
        if len(images) > 1:
            # Si l'image actuelle est -0.jpg, vérifier s'il y a une meilleure option
            if current_thumbnail.endswith('-0.jpg'):
                # Chercher une image qui pourrait être meilleure
                for image in images:
                    if not image.endswith('-0.jpg') and 'front' in image.lower():
                        suggestions.append({
                            'jersey_id': jersey_id,
                            'current': current_thumbnail,
                            'suggested': image,
                            'reason': 'Image avec "front" détectée'
                        })
                        break
                    elif not image.endswith('-0.jpg') and 'main' in image.lower():
                        suggestions.append({
                            'jersey_id': jersey_id,
                            'current': current_thumbnail,
                            'suggested': image,
                            'reason': 'Image avec "main" détectée'
                        })
                        break
    
    if suggestions:
        print(f"📋 {len(suggestions)} suggestions trouvées:\n")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. Maillot {suggestion['jersey_id']}:")
            print(f"   Actuel: {suggestion['current']}")
            print(f"   Suggéré: {suggestion['suggested']}")
            print(f"   Raison: {suggestion['reason']}")
            print()
    else:
        print("✅ Aucune suggestion d'amélioration nécessaire")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--suggest":
        suggest_cover_changes()
    else:
        check_cover_images()
