#!/usr/bin/env python3
"""
NETTOYAGE FINAL - FC PALESTINA
Supprime tous les fichiers de développement et de test pour préparer la production
"""

import os
import shutil
from pathlib import Path

# Dossier racine du projet
PROJECT_ROOT = Path("c:/Users/linkl/Desktop/FCpalestina")

# Fichiers et dossiers à supprimer pour la production
FILES_TO_DELETE = [
    # Fichiers de test
    "test-contact-final.html",
    "test-formsubmit.html", 
    "test_admin_api.py",
    "test_buttons.html",
    "test_extraction.py",
    "test_gallery.html",
    "test_gallery_simple.html", 
    "test_images.html",
    "test_image_access.html",
    "test_modal_debug.html",
    "test_modal_simple.html",
    "test_simple.html",
    "test_yupoo_connection.py",
    
    # Fichiers de développement
    "debug_gallery.html",
    "debug_modal.html",
    "favicon-generator.html",
    "create_demo_images.html",
    "create_demo_images.py",
    
    # Scripts Python non nécessaires
    "change_cover_simple.py",
    "import_batch.py", 
    "import_quick.py",
    "import_simple.py",
    "import_smart.py",
    "import_yupoo_jerseys.py",
    "optimize_images.py",
    "run_scraper.py",
    "translate_jerseys.py",
    "launch_site.py",
    
    # Fichiers temporaires et logs
    "advanced_yupoo_scraper.log",
    "image_scraper.log", 
    "yupoo_scraper.log",
    
    # Scripts de démarrage dev
    "start_admin.bat",
    "start_admin.ps1", 
    "start_admin_backend.bat",
    "start_admin_backend.py",
    "start_backend.py",
    "start_servers.py",
    
    # Fichiers JS temporaires
    "fix_js_errors.js",
    "fix_modal.js",
    "force_buttons.js",
    "gallery_simple.js",
    
    # Fichiers CSS temporaires  
    "fix_modal_styles.css",
    
    # Page de remerciement locale
    "merci.html",
    
    # Guides de dev
    "GUIDE-EMAILJS.md",
    "GUIDE_IMPORTATION.md",
    "GUIDE_SCRAPER.md",
    "ADMIN_GUIDE.md",
    "ADMIN_README.md",
    
    # Favicon SVG non utilisée
    "assets/img/favicon.svg",
]

# Dossiers à supprimer
DIRS_TO_DELETE = [
    "scripts",  # Scripts Python pour scraping
]

def clean_project():
    """Nettoie le projet pour la production"""
    
    print("🧹 NETTOYAGE FINAL FC PALESTINA")
    print("=" * 50)
    
    deleted_count = 0
    
    # Supprimer les fichiers
    for file_path in FILES_TO_DELETE:
        full_path = PROJECT_ROOT / file_path
        if full_path.exists():
            try:
                full_path.unlink()
                print(f"✅ Supprimé: {file_path}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Erreur suppression {file_path}: {e}")
        else:
            print(f"⚠️  Déjà absent: {file_path}")
    
    # Supprimer les dossiers
    for dir_path in DIRS_TO_DELETE:
        full_path = PROJECT_ROOT / dir_path
        if full_path.exists():
            try:
                shutil.rmtree(full_path)
                print(f"✅ Dossier supprimé: {dir_path}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Erreur suppression dossier {dir_path}: {e}")
    
    print("=" * 50)
    print(f"🎉 Nettoyage terminé ! {deleted_count} éléments supprimés")
    print()
    
    # Lister les fichiers restants
    print("📁 FICHIERS FINAUX POUR PRODUCTION:")
    print("-" * 30)
    
    essential_files = []
    for item in PROJECT_ROOT.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            essential_files.append(item.name)
    
    essential_files.sort()
    for file in essential_files:
        print(f"📄 {file}")
    
    print()
    print("📁 DOSSIERS FINAUX:")
    print("-" * 15)
    for item in PROJECT_ROOT.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            print(f"📂 {item.name}/")
    
    print()
    print("✅ Projet FC Palestina prêt pour la production !")

if __name__ == "__main__":
    clean_project()