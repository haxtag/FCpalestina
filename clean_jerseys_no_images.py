#!/usr/bin/env python3
"""
Nettoie jerseys.json pour ne garder QUE les maillots avec des images valides
"""
import json
import os
from pathlib import Path

def clean_jerseys():
    """Supprime tous les maillots sans images"""
    
    # Charger les données
    jerseys_file = 'data/jerseys.json'
    with open(jerseys_file, 'r', encoding='utf-8') as f:
        jerseys = json.load(f)
    
    initial_count = len(jerseys)
    print(f"📦 Total initial: {initial_count} maillots")
    
    # Filtrer uniquement ceux avec images valides
    valid_jerseys = []
    removed_count = 0
    
    for jersey in jerseys:
        thumbnail = jersey.get('thumbnail', '')
        
        if not thumbnail:
            print(f"❌ Supprimé (pas de thumbnail): {jersey.get('title', 'Sans titre')}")
            removed_count += 1
            continue
        
        # Vérifier si l'image existe
        img_path = Path(f"assets/images/jerseys/{thumbnail}")
        if not img_path.exists():
            print(f"❌ Supprimé (image manquante {thumbnail}): {jersey.get('title', 'Sans titre')}")
            removed_count += 1
            continue
        
        # Vérifier si le fichier a une taille > 0
        if img_path.stat().st_size == 0:
            print(f"❌ Supprimé (image vide): {jersey.get('title', 'Sans titre')}")
            removed_count += 1
            continue
        
        # OK, on garde ce maillot
        valid_jerseys.append(jersey)
    
    # Sauvegarder
    with open(jerseys_file, 'w', encoding='utf-8') as f:
        json.dump(valid_jerseys, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Nettoyage terminé!")
    print(f"📊 Maillots conservés: {len(valid_jerseys)}")
    print(f"🗑️  Maillots supprimés: {removed_count}")
    print(f"💾 Fichier mis à jour: {jerseys_file}")

if __name__ == "__main__":
    clean_jerseys()
