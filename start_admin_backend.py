#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour lancer le backend d'administration
"""

import subprocess
import sys
import os

def main():
    print("🚀 Lancement du backend d'administration...")
    
    # Vérifier que le script existe
    script_path = os.path.join('scripts', 'admin_backend.py')
    if not os.path.exists(script_path):
        print("❌ Script admin_backend.py non trouvé!")
        return
    
    try:
        # Lancer le serveur
        subprocess.run([sys.executable, script_path, '8001'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du backend d'administration")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    main()
