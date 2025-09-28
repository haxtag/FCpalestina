#!/usr/bin/env python3
"""
Script simple pour changer l'image de couverture d'un maillot
"""

import json
import os
from pathlib import Path

def load_jerseys():
    """Charger les maillots depuis le fichier JSON"""
    jerseys_file = Path("data/jerseys.json")
    if jerseys_file.exists():
        with open(jerseys_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_jerseys(jerseys):
    """Sauvegarder les maillots dans le fichier JSON"""
    jerseys_file = Path("data/jerseys.json")
    with open(jerseys_file, 'w', encoding='utf-8') as f:
        json.dump(jerseys, f, ensure_ascii=False, indent=2)

def display_jerseys(jerseys):
    """Afficher la liste des maillots"""
    print("\n📋 Maillots disponibles :")
    print("-" * 50)
    for i, jersey in enumerate(jerseys, 1):
        print(f"{i}. {jersey['title']} ({jersey['category']}) - {jersey['year']}")
        print(f"   ID: {jersey['id']}")
        print(f"   Image actuelle: {jersey.get('thumbnail', 'Aucune')}")
        print(f"   Images disponibles: {len(jersey.get('images', []))}")
        print()

def change_cover_image():
    """Changer l'image de couverture d'un maillot"""
    jerseys = load_jerseys()
    
    if not jerseys:
        print("❌ Aucun maillot trouvé")
        return
    
    display_jerseys(jerseys)
    
    try:
        # Sélectionner le maillot
        choice = int(input("🔢 Choisissez le numéro du maillot à modifier : ")) - 1
        
        if choice < 0 or choice >= len(jerseys):
            print("❌ Numéro invalide")
            return
        
        jersey = jerseys[choice]
        print(f"\n✅ Maillot sélectionné : {jersey['title']}")
        
        # Afficher les images disponibles
        images = jersey.get('images', [])
        if not images:
            print("❌ Aucune image disponible pour ce maillot")
            return
        
        print(f"\n🖼️ Images disponibles ({len(images)}) :")
        print("-" * 30)
        for i, image in enumerate(images, 1):
            status = " (ACTUELLE)" if image == jersey.get('thumbnail') else ""
            print(f"{i}. {image}{status}")
        
        # Sélectionner la nouvelle image
        img_choice = int(input("\n🔢 Choisissez le numéro de la nouvelle image de couverture : ")) - 1
        
        if img_choice < 0 or img_choice >= len(images):
            print("❌ Numéro d'image invalide")
            return
        
        new_thumbnail = images[img_choice]
        
        # Mettre à jour
        jersey['thumbnail'] = new_thumbnail
        
        # Sauvegarder
        save_jerseys(jerseys)
        
        print(f"\n✅ Image de couverture mise à jour !")
        print(f"📸 Nouvelle image : {new_thumbnail}")
        
    except ValueError:
        print("❌ Veuillez entrer un numéro valide")
    except KeyboardInterrupt:
        print("\n❌ Opération annulée")

def main():
    """Fonction principale"""
    print("🏆 FC Palestina - Changer l'image de couverture")
    print("=" * 50)
    
    change_cover_image()

if __name__ == "__main__":
    main()
