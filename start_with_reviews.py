#!/usr/bin/env python3
"""
Script de démarrage complet avec auto-update des avis
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def start_reviews_updater():
    """Démarrer l'auto-updater des avis en arrière-plan"""
    try:
        script_dir = Path(__file__).parent
        updater_script = script_dir / "auto_update_reviews.py"
        
        print("🔄 Démarrage de l'auto-updater des avis Vinted...")
        
        # Lancer une mise à jour immédiate
        subprocess.run([sys.executable, str(updater_script), "--once"], 
                      cwd=str(script_dir))
        
        print("✅ Mise à jour initiale des avis terminée")
        
    except Exception as e:
        print(f"⚠️ Erreur lors du démarrage de l'updater: {e}")

def start_backend():
    """Démarrer le serveur backend"""
    try:
        script_dir = Path(__file__).parent
        backend_script = script_dir / "simple_backend.py"
        
        if backend_script.exists():
            print("🌐 Démarrage du serveur backend...")
            subprocess.run([sys.executable, str(backend_script)], cwd=str(script_dir))
        else:
            print("⚠️ Script backend non trouvé, démarrage du serveur Python simple...")
            os.chdir(script_dir.parent)
            subprocess.run([sys.executable, "-m", "http.server", "8000"])
            
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du backend: {e}")

def main():
    """Fonction principale de démarrage"""
    print("🌟 FC Palestina - Démarrage complet avec avis Vinted")
    print("=" * 60)
    
    # Démarrer l'updater des avis en thread séparé
    updater_thread = threading.Thread(target=start_reviews_updater, daemon=True)
    updater_thread.start()
    
    # Attendre que l'updater termine sa première mise à jour
    time.sleep(3)
    
    # Démarrer le serveur backend
    start_backend()

if __name__ == "__main__":
    main()