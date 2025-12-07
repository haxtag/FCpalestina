#!/usr/bin/env python3
"""
Script de nettoyage des doublons et maillots sans images
"""
import json
import os
from pathlib import Path
import hashlib
from datetime import datetime
import shutil

def load_jerseys():
    """Charger les maillots"""
    with open('data/jerseys.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_jerseys(jerseys):
    """Sauvegarder les maillots avec backup"""
    # Backup
    os.makedirs('data/backups', exist_ok=True)
    backup_name = f"data/backups/jerseys_before_clean_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy2('data/jerseys.json', backup_name)
    print(f"✓ Backup créé: {backup_name}")
    
    # Sauvegarder
    with open('data/jerseys.json', 'w', encoding='utf-8') as f:
        json.dump(jerseys, f, ensure_ascii=False, indent=2)

def remove_duplicates(jerseys):
    """Supprimer les doublons basés sur le titre"""
    seen = {}
    unique = []
    duplicates = []
    
    for jersey in jerseys:
        title = jersey.get('title', '').strip().lower()
        if not title:
            continue
            
        if title not in seen:
            seen[title] = jersey
            unique.append(jersey)
        else:
            duplicates.append(jersey)
            print(f"  Doublon trouvé: {jersey.get('title')} (id: {jersey.get('id')})")
    
    return unique, duplicates

def remove_without_images(jerseys):
    """Supprimer les maillots sans images valides"""
    with_images = []
    without_images = []
    
    for jersey in jerseys:
        has_valid_image = False
        
        # Vérifier cover_image
        cover = jersey.get('cover_image', '')
        if cover:
            # Si c'est un chemin local
            if cover.startswith('assets/images/'):
                img_path = Path(cover)
                if img_path.exists():
                    has_valid_image = True
            # Si c'est une URL
            elif cover.startswith('http'):
                has_valid_image = True
        
        # Vérifier images array
        images = jersey.get('images', [])
        if images and len(images) > 0:
            for img in images:
                if img.startswith('assets/images/'):
                    if Path(img).exists():
                        has_valid_image = True
                        break
                elif img.startswith('http'):
                    has_valid_image = True
                    break
        
        if has_valid_image:
            with_images.append(jersey)
        else:
            without_images.append(jersey)
            print(f"  Sans image: {jersey.get('title')} (id: {jersey.get('id')})")
    
    return with_images, without_images

def remove_last_n(jerseys, n):
    """Supprimer les N derniers maillots"""
    if n <= 0 or n >= len(jerseys):
        print(f"❌ Nombre invalide: {n} (total: {len(jerseys)})")
        return jerseys, []
    
    kept = jerseys[:-n]
    removed = jerseys[-n:]
    
    print(f"\nMaillots à supprimer (les {n} derniers):")
    for jersey in removed:
        print(f"  - {jersey.get('title')} (id: {jersey.get('id')})")
    
    return kept, removed

def main():
    print("🧹 Nettoyage des maillots\n")
    
    # Charger
    jerseys = load_jerseys()
    initial_count = len(jerseys)
    print(f"📊 Maillots actuels: {initial_count}\n")
    
    # Menu
    print("Options:")
    print("1. Supprimer les doublons (basé sur le titre)")
    print("2. Supprimer les maillots sans images")
    print("3. Supprimer les N derniers maillots")
    print("4. Tout nettoyer (doublons + sans images)")
    
    choice = input("\nChoisissez une option (1-4): ").strip()
    
    cleaned = jerseys
    removed_items = []
    
    if choice == '1':
        print("\n🔍 Recherche des doublons...")
        cleaned, removed_items = remove_duplicates(jerseys)
        
    elif choice == '2':
        print("\n🔍 Recherche des maillots sans images...")
        cleaned, removed_items = remove_without_images(jerseys)
        
    elif choice == '3':
        try:
            n = int(input("\nCombien de maillots supprimer (depuis la fin)? "))
            print(f"\n🔍 Suppression des {n} derniers maillots...")
            cleaned, removed_items = remove_last_n(jerseys, n)
        except ValueError:
            print("❌ Nombre invalide")
            return
            
    elif choice == '4':
        print("\n🔍 Nettoyage complet...")
        # D'abord les doublons
        print("\nÉtape 1: Doublons")
        cleaned, dup_removed = remove_duplicates(jerseys)
        removed_items.extend(dup_removed)
        
        # Ensuite les sans images
        print("\nÉtape 2: Sans images")
        cleaned, no_img_removed = remove_without_images(cleaned)
        removed_items.extend(no_img_removed)
        
    else:
        print("❌ Option invalide")
        return
    
    # Résumé
    final_count = len(cleaned)
    removed_count = len(removed_items)
    
    print(f"\n📊 Résumé:")
    print(f"  Avant: {initial_count} maillots")
    print(f"  Après: {final_count} maillots")
    print(f"  Supprimés: {removed_count} maillots")
    
    if removed_count == 0:
        print("\n✓ Aucun maillot à supprimer!")
        return
    
    # Confirmation
    confirm = input("\n⚠️  Confirmer la suppression? (oui/non): ").strip().lower()
    if confirm in ['oui', 'o', 'yes', 'y']:
        save_jerseys(cleaned)
        print(f"\n✓ Nettoyage terminé! {removed_count} maillots supprimés.")
        print(f"✓ {final_count} maillots conservés.")
    else:
        print("\n❌ Nettoyage annulé.")

if __name__ == "__main__":
    main()
