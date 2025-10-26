#!/usr/bin/env python3
"""
Script pour s'assurer que tous les thumbnails sont la première image
Respecte la logique Yupoo : image de présentation = première image
"""

import json
import os
from pathlib import Path

def fix_thumbnails():
    """Corriger les thumbnails pour qu'ils soient toujours la première image"""
    
    jerseys_file = Path('data/jerseys.json')
    
    if not jerseys_file.exists():
        print(f"❌ Fichier non trouvé: {jerseys_file}")
        return
    
    # Charger les données
    with open(jerseys_file, 'r', encoding='utf-8') as f:
        jerseys = json.load(f)
    
    modified_count = 0
    
    for jersey in jerseys:
        if 'images' not in jersey or not jersey['images']:
            continue
        
        first_image = jersey['images'][0]
        current_thumbnail = jersey.get('thumbnail')
        
        # Si le thumbnail n'est pas la première image, le corriger
        if current_thumbnail != first_image:
            print(f"🔧 Correction: {jersey.get('title', jersey.get('id'))}")
            print(f"   Ancien thumbnail: {current_thumbnail}")
            print(f"   Nouveau thumbnail: {first_image}")
            jersey['thumbnail'] = first_image
            modified_count += 1
    
    if modified_count > 0:
        # Sauvegarder les modifications
        with open(jerseys_file, 'w', encoding='utf-8') as f:
            json.dump(jerseys, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ {modified_count} thumbnail(s) corrigé(s)")
        print(f"💾 Fichier sauvegardé: {jerseys_file}")
    else:
        print("✅ Tous les thumbnails sont déjà corrects (première image)")

if __name__ == '__main__':
    fix_thumbnails()
