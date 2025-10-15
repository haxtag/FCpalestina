#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour lancer le backend d'administration
"""

import subprocess
import sys
import os

def main():
    print("🚀 Lancement du backend d'administration (Flask simple_backend.py)...")
    
    # Utiliser le backend Flask simple et officiel
    script_path = os.path.join('scripts', 'simple_backend.py')
    if not os.path.exists(script_path):
        print("❌ Script simple_backend.py non trouvé!")
        return
    
    try:
        # Lancer le serveur Flask sur 8001
        subprocess.run([sys.executable, script_path], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du backend d'administration")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    main()
