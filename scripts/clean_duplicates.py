#!/usr/bin/env python3
"""
Script de nettoyage des doublons et maillots sans images
"""
import argparse
import json
import os
from pathlib import Path
from datetime import datetime
import shutil

def load_jerseys():
    """Charger les maillots"""
    with open('data/jerseys.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_jerseys(jerseys):
    """Sauvegarder les maillots avec backup"""
    os.makedirs('data/backups', exist_ok=True)
    backup_name = f"data/backups/jerseys_before_clean_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy2('data/jerseys.json', backup_name)
    print(f"✓ Backup créé: {backup_name}")

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
                # Accepte Cloudflare/R2/CDN ou extensions d'image
                if (
                    'cloudflare' in cover or
                    'r2cdn' in cover or
                    cover.endswith(('.jpg', '.jpeg', '.png', '.webp'))
                ):
                    has_valid_image = True
            # Si c'est un nom de fichier image
            elif cover.endswith(('.jpg', '.jpeg', '.png', '.webp')):
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
                    if (
                        'cloudflare' in img or
                        'r2cdn' in img or
                        img.endswith(('.jpg', '.jpeg', '.png', '.webp'))
                    ):
                        has_valid_image = True
                        break
                # Si c'est un nom de fichier image
                elif img.endswith(('.jpg', '.jpeg', '.png', '.webp')):
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

def run_cleanup(mode: str, number: int = 0, auto_confirm: bool = False):
    """Nettoyer selon le mode choisi (non interactif)."""
    jerseys = load_jerseys()
    initial_count = len(jerseys)
    cleaned = jerseys
    removed_items = []

    if mode == 'duplicates':
        print("\n🔍 Recherche des doublons...")
        cleaned, removed_items = remove_duplicates(jerseys)

    elif mode == 'no-images':
        print("\n🔍 Recherche des maillots sans images...")
        cleaned, removed_items = remove_without_images(jerseys)

    elif mode == 'last':
        print(f"\n🔍 Suppression des {number} derniers maillots...")
        cleaned, removed_items = remove_last_n(jerseys, number)

    elif mode == 'all':
        print("\n🔍 Nettoyage complet...")
        print("\nÉtape 1: Doublons")
        cleaned, dup_removed = remove_duplicates(jerseys)
        removed_items.extend(dup_removed)

        print("\nÉtape 2: Sans images")
        cleaned, no_img_removed = remove_without_images(cleaned)
        removed_items.extend(no_img_removed)

    else:
        print("❌ Mode invalide")
        return False

    final_count = len(cleaned)
    removed_count = len(removed_items)

    print(f"\n📊 Résumé:")
    print(f"  Avant: {initial_count} maillots")
    print(f"  Après: {final_count} maillots")
    print(f"  Supprimés: {removed_count} maillots")

    if removed_count == 0:
        print("\n✓ Aucun maillot à supprimer!")
        return True

    if auto_confirm:
        save_jerseys(cleaned)
        print(f"\n✓ Nettoyage terminé! {removed_count} maillots supprimés.")
        print(f"✓ {final_count} maillots conservés.")
        return True

    confirm = input("\n⚠️  Confirmer la suppression? (oui/non): ").strip().lower()
    if confirm in ['oui', 'o', 'yes', 'y']:
        save_jerseys(cleaned)
        print(f"\n✓ Nettoyage terminé! {removed_count} maillots supprimés.")
        print(f"✓ {final_count} maillots conservés.")
        return True

    print("\n❌ Nettoyage annulé.")
    return False


def interactive_menu():
    """Mode interactif legacy (console)."""
    print("🧹 Nettoyage des maillots\n")

    jerseys = load_jerseys()
    initial_count = len(jerseys)
    print(f"📊 Maillots actuels: {initial_count}\n")

    print("Options:")
    print("1. Supprimer les doublons (basé sur le titre)")
    print("2. Supprimer les maillots sans images")
    print("3. Supprimer les N derniers maillots")
    print("4. Tout nettoyer (doublons + sans images)")

    choice = input("\nChoisissez une option (1-4): ").strip()

    if choice == '1':
        return run_cleanup('duplicates')
    if choice == '2':
        return run_cleanup('no-images')
    if choice == '3':
        try:
            n = int(input("\nCombien de maillots supprimer (depuis la fin)? "))
        except ValueError:
            print("❌ Nombre invalide")
            return False
        return run_cleanup('last', number=n)
    if choice == '4':
        return run_cleanup('all')

    print("❌ Option invalide")
    return False


def main():
    parser = argparse.ArgumentParser(description="Nettoyage des maillots")
    parser.add_argument('--mode', choices=['duplicates', 'no-images', 'last', 'all'], help='Mode de nettoyage')
    parser.add_argument('--number', type=int, default=0, help='Nombre de maillots (pour mode last)')
    parser.add_argument('--yes', action='store_true', help='Confirmer automatiquement')

    args = parser.parse_args()

    if args.mode:
        success = run_cleanup(args.mode, args.number, auto_confirm=args.yes)
        raise SystemExit(0 if success else 1)

    # Mode interactif si aucun argument
    success = interactive_menu()
    raise SystemExit(0 if success else 1)

if __name__ == "__main__":
    main()
