#!/usr/bin/env python3
"""
Script pour changer manuellement l'image de couverture d'un maillot
"""

import json
import os
from pathlib import Path

def change_cover_image(jersey_id, new_image):
    """
    Change l'image de couverture d'un maillot spécifique
    """
    print(f"🔄 Changement de l'image de couverture pour le maillot {jersey_id}...")
    
    # Charger les données des maillots
    jerseys_file = Path("data/jerseys.json")
    if not jerseys_file.exists():
        print("❌ Fichier jerseys.json non trouvé")
        return False
    
    with open(jerseys_file, 'r', encoding='utf-8') as f:
        jerseys = json.load(f)
    
    # Trouver le maillot
    jersey = None
    for j in jerseys:
        if j.get('id') == jersey_id:
            jersey = j
            break
    
    if not jersey:
        print(f"❌ Maillot {jersey_id} non trouvé")
        return False
    
    # Vérifier que la nouvelle image existe dans la liste
    images = jersey.get('images', [])
    if new_image not in images:
        print(f"❌ Image {new_image} non trouvée dans les images disponibles")
        print(f"Images disponibles: {images}")
        return False
    
    # Changer l'image de couverture
    old_image = jersey.get('thumbnail', '')
    jersey['thumbnail'] = new_image
    
    # Sauvegarder
    with open(jerseys_file, 'w', encoding='utf-8') as f:
        json.dump(jerseys, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Image de couverture changée:")
    print(f"   Ancienne: {old_image}")
    print(f"   Nouvelle: {new_image}")
    
    return True

def interactive_cover_selector():
    """
    Interface interactive pour changer les images de couverture
    """
    print("🎯 Sélecteur interactif d'images de couverture")
    print("=" * 50)
    
    # Charger les données des maillots
    jerseys_file = Path("data/jerseys.json")
    if not jerseys_file.exists():
        print("❌ Fichier jerseys.json non trouvé")
        return
    
    with open(jerseys_file, 'r', encoding='utf-8') as f:
        jerseys = json.load(f)
    
    while True:
        print(f"\n📋 {len(jerseys)} maillots disponibles:")
        for i, jersey in enumerate(jerseys):
            title = jersey.get('title', 'Sans titre')[:50]
            print(f"  {i+1}. {title}")
        
        try:
            choice = input(f"\nChoisissez un maillot (1-{len(jerseys)}) ou 'q' pour quitter: ").strip()
            
            if choice.lower() == 'q':
                print("👋 Au revoir!")
                break
            
            jersey_index = int(choice) - 1
            if jersey_index < 0 or jersey_index >= len(jerseys):
                print("❌ Choix invalide")
                continue
            
            jersey = jerseys[jersey_index]
            jersey_id = jersey.get('id')
            title = jersey.get('title', 'Sans titre')
            current_thumbnail = jersey.get('thumbnail', '')
            images = jersey.get('images', [])
            
            print(f"\n🏆 Maillot sélectionné: {title}")
            print(f"   ID: {jersey_id}")
            print(f"   Image actuelle: {current_thumbnail}")
            
            if not images:
                print("   ⚠️ Aucune image disponible")
                continue
            
            print(f"\n📸 Images disponibles ({len(images)}):")
            for i, image in enumerate(images):
                marker = "👑" if image == current_thumbnail else "  "
                print(f"   {marker} {i+1}. {image}")
            
            try:
                img_choice = input(f"\nChoisissez une nouvelle image (1-{len(images)}) ou 'c' pour annuler: ").strip()
                
                if img_choice.lower() == 'c':
                    continue
                
                img_index = int(img_choice) - 1
                if img_index < 0 or img_index >= len(images):
                    print("❌ Choix d'image invalide")
                    continue
                
                new_image = images[img_index]
                
                if new_image == current_thumbnail:
                    print("✅ Cette image est déjà sélectionnée")
                    continue
                
                # Confirmer le changement
                confirm = input(f"Confirmer le changement vers {new_image}? (y/n): ").strip().lower()
                if confirm == 'y':
                    if change_cover_image(jersey_id, new_image):
                        print("🎉 Changement effectué avec succès!")
                    else:
                        print("❌ Erreur lors du changement")
                else:
                    print("❌ Changement annulé")
                    
            except ValueError:
                print("❌ Choix invalide")
                continue
                
        except ValueError:
            print("❌ Choix invalide")
            continue
        except KeyboardInterrupt:
            print("\n👋 Au revoir!")
            break

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 3:
        # Mode ligne de commande: python script.py jersey_id new_image
        jersey_id = sys.argv[1]
        new_image = sys.argv[2]
        change_cover_image(jersey_id, new_image)
    else:
        # Mode interactif
        interactive_cover_selector()
