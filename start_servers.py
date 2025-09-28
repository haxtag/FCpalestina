#!/usr/bin/env python3
"""
Script pour démarrer les deux serveurs nécessaires
"""

import subprocess
import sys
import time
import threading
import os

def start_http_server():
    """Démarrer le serveur HTTP principal sur le port 8000"""
    print("🌐 Démarrage du serveur HTTP principal sur le port 8000...")
    subprocess.run([sys.executable, "-m", "http.server", "8000"], cwd=os.getcwd())

def start_backend_server():
    """Démarrer le backend API sur le port 8001"""
    print("🔧 Démarrage du backend API sur le port 8001...")
    subprocess.run([sys.executable, "scripts/simple_backend.py"], cwd=os.getcwd())

if __name__ == "__main__":
    print("🚀 Démarrage des serveurs FC Palestina...")
    print("📱 Site principal: http://localhost:8000")
    print("🔧 API admin: http://localhost:8001/api/")
    print("🛑 Appuyez sur Ctrl+C pour arrêter tous les serveurs")
    
    try:
        # Démarrer le backend en arrière-plan
        backend_thread = threading.Thread(target=start_backend_server)
        backend_thread.daemon = True
        backend_thread.start()
        
        # Attendre un peu que le backend démarre
        time.sleep(2)
        
        # Démarrer le serveur HTTP principal (bloquant)
        start_http_server()
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt des serveurs...")
        sys.exit(0)
