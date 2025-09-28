#!/usr/bin/env python3
"""
Script simple pour démarrer le backend admin
"""

import subprocess
import sys
import os

def start_backend():
    """Démarre le backend admin (Flask simple_backend) sur le port 8001"""
    try:
        # Chemin vers le script backend
        backend_script = os.path.join('scripts', 'simple_backend.py')

        if not os.path.exists(backend_script):
            print(f"❌ Script backend non trouvé: {backend_script}")
            return False

        print("🚀 Démarrage du backend admin (Flask) sur le port 8001...")
        print("📱 API disponible sur: http://localhost:8001/api/")
        print("💡 Admin ultra-simple: http://localhost:8000/index.html?admin=true")
        print("🛑 Appuyez sur Ctrl+C pour arrêter")

        # Démarrer le backend
        subprocess.run([sys.executable, backend_script], cwd=os.getcwd())

    except KeyboardInterrupt:
        print("\n🛑 Backend arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du backend: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_backend()
