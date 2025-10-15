#!/usr/bin/env python3
"""
Script de nettoyage du projet FC Palestina pour la production
"""

import os
import shutil
import glob

def clean_project():
    """Nettoyer le projet pour la production"""
    print("🧹 Nettoyage du projet FC Palestina")
    print("=" * 40)
    
    # Fichiers à supprimer
    files_to_remove = [
        # Fichiers de test et debug
        "debug_*.html",
        "test_*.html", 
        "test_*.py",
        "test-*.html",
        "create_demo_images.html",
        "create_demo_images.py",
        "generate_test_jerseys.py",
        "create_placeholder_images.py",
        
        # Fichiers JS de debug
        "fix_js_errors.js",
        "fix_modal.js", 
        "force_buttons.js",
        "gallery_simple.js",
        
        # CSS de fix temporaires
        "fix_modal_styles.css",
        
        # Logs
        "*.log",
        "advanced_yupoo_scraper.log",
        "image_scraper.log",
        "yupoo_scraper.log",
        
        # Fichiers de données de test
        "data/test_jerseys.json",
    ]
    
    # Dossiers à nettoyer
    folders_to_clean = [
        "scripts/__pycache__",
        "data/backups",  # Garder quelques backups récents seulement
    ]
    
    removed_files = 0
    
    # Supprimer les fichiers
    for pattern in files_to_remove:
        for file_path in glob.glob(pattern):
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"  ✅ Supprimé: {file_path}")
                    removed_files += 1
                except Exception as e:
                    print(f"  ❌ Erreur suppression {file_path}: {e}")
    
    # Nettoyer les dossiers
    for folder in folders_to_clean:
        if os.path.exists(folder):
            try:
                if folder == "data/backups":
                    # Garder seulement les 3 backups les plus récents
                    backup_files = glob.glob(os.path.join(folder, "*"))
                    backup_files.sort(key=os.path.getmtime, reverse=True)
                    
                    for backup_file in backup_files[3:]:  # Supprimer tout sauf les 3 plus récents
                        os.remove(backup_file)
                        print(f"  ✅ Backup supprimé: {backup_file}")
                        removed_files += 1
                else:
                    shutil.rmtree(folder)
                    print(f"  ✅ Dossier supprimé: {folder}")
                    removed_files += 1
            except Exception as e:
                print(f"  ❌ Erreur nettoyage {folder}: {e}")
    
    print(f"\n🎯 Nettoyage terminé: {removed_files} éléments supprimés")
    print("\n📦 Fichiers essentiels conservés:")
    
    essential_files = [
        "index.html",
        "admin.html", 
        "scripts/yupoo_scraper.py",
        "scripts/simple_backend.py",
        "scripts/requirements.txt",
        "data/jerseys.json",
        "data/categories.json", 
        "data/tags.json",
        "assets/ (complet)",
        "run_scraper.py"
    ]
    
    for file in essential_files:
        print(f"  ✅ {file}")
    
    print("\n🚀 Projet prêt pour la production!")

if __name__ == "__main__":
    clean_project()