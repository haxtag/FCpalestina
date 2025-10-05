#!/usr/bin/env python3
"""
Script de lancement simple pour le scraper Yupoo
"""

import os
import sys
import subprocess

def main():
    print("Scraper Yupoo FC Palestina")
    print("=" * 40)
    
    # Verifier que nous sommes dans le bon repertoire (ASCII-only for Windows console)
    if not os.path.exists('scripts'):
        print("Erreur: Dossier 'scripts' non trouve")
        print("Astuce: Assurez-vous d'etre dans le repertoire du projet")
        return
    
    print("Choisissez une action:")
    print("1. Tester le scraper")
    print("2. Lancer le scraping complet (recommande)")
    print("3. Lancer l'ancien scraper (legacy)")
    print("4. Creer des donnees de demonstration")
    print("5. Installer les dependances")
    
    choice = input("\nVotre choix (1-5): ").strip()
    
    if choice == "1":
        print("\nLancement du test...")
        try:
            subprocess.run([sys.executable, "scripts/test_scraper.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors du test: {e}")
        except FileNotFoundError:
            print("Python non trouve. Assurez-vous que Python est installe.")
    
    elif choice == "2":
        print("\nLancement du scraping complet (nouveau)...")
        try:
            subprocess.run([sys.executable, "scripts/yupoo_scraper_complet.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors du scraping: {e}")
        except FileNotFoundError:
            print("Python non trouve. Assurez-vous que Python est installe.")
    
    elif choice == "3":
        print("\nLancement de l'ancien scraper (legacy)...")
        try:
            subprocess.run([sys.executable, "scripts/yupoo_scraper.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors du scraping legacy: {e}")
        except FileNotFoundError:
            print("Python non trouve. Assurez-vous que Python est installe.")
    
    elif choice == "4":
        print("\nCreation des donnees de demonstration...")
        try:
            subprocess.run([sys.executable, "scripts/test_scraper.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erreur: {e}")
    
    elif choice == "5":
        print("\nInstallation des dependances...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "scripts/requirements.txt"], check=True)
            print("Dependances installees avec succes !")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'installation: {e}")
        except FileNotFoundError:
            print("pip non trouve. Assurez-vous que Python est installe.")
    
    else:
        print("Choix invalide")
    
    print("\nAction terminee !")
    print("Astuce: Pour voir les resultats, rechargez votre site web")

if __name__ == "__main__":
    main()
