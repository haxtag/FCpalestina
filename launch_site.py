#!/usr/bin/env python3
"""
Script de lancement simple pour FC Palestina
"""

import subprocess
import sys
import time
import os
import webbrowser
from threading import Thread

def start_backend():
    """Démarrer le backend Flask"""
    print("🔧 Démarrage du backend Flask...")
    try:
        subprocess.run([sys.executable, "scripts/simple_backend.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend arrêté")
    except Exception as e:
        print(f"❌ Erreur backend: {e}")

def start_frontend():
    """Démarrer le serveur HTTP frontend"""
    print("🌐 Démarrage du serveur HTTP...")
    try:
        subprocess.run([sys.executable, "-m", "http.server", "8000"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend arrêté")
    except Exception as e:
        print(f"❌ Erreur frontend: {e}")

def main():
    print("🚀 Lancement de FC Palestina...")
    print("📱 Site principal: http://localhost:8000")
    print("🔧 API admin: http://localhost:8001/api/")
    print("🛑 Appuyez sur Ctrl+C pour arrêter tous les serveurs")
    print()
    
    # Vérifier que les fichiers existent
    if not os.path.exists("scripts/simple_backend.py"):
        print("❌ Erreur: scripts/simple_backend.py non trouvé")
        return
    
    if not os.path.exists("index.html"):
        print("❌ Erreur: index.html non trouvé")
        return
    
    # Démarrer le backend en arrière-plan
    backend_thread = Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Attendre un peu que le backend démarre
    time.sleep(2)
    
    # Ouvrir le navigateur
    print("🌐 Ouverture du navigateur...")
    webbrowser.open("http://localhost:8000")
    
    # Démarrer le frontend (bloquant)
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt des serveurs...")
        print("✅ Au revoir !")

if __name__ == "__main__":
    main()
