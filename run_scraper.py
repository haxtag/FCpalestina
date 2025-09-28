#!/usr/bin/env python3
"""
Script de lancement simple pour le scraper Yupoo
"""

import os
import sys
import subprocess

def main():
    print("🏆 Scraper Yupoo FC Palestina")
    print("=" * 40)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists('scripts'):
        print("❌ Erreur: Dossier 'scripts' non trouvé")
        print("💡 Assurez-vous d'être dans le répertoire du projet")
        return
    
    print("Choisissez une action:")
    print("1. 🧪 Tester le scraper")
    print("2. 🚀 Lancer le scraping complet")
    print("3. 📝 Créer des données de démonstration")
    print("4. 🔧 Installer les dépendances")
    
    choice = input("\nVotre choix (1-4): ").strip()
    
    if choice == "1":
        print("\n🧪 Lancement du test...")
        try:
            subprocess.run([sys.executable, "scripts/test_scraper.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors du test: {e}")
        except FileNotFoundError:
            print("❌ Python non trouvé. Assurez-vous que Python est installé.")
    
    elif choice == "2":
        print("\n🚀 Lancement du scraping...")
        try:
            subprocess.run([sys.executable, "scripts/yupoo_scraper.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors du scraping: {e}")
        except FileNotFoundError:
            print("❌ Python non trouvé. Assurez-vous que Python est installé.")
    
    elif choice == "3":
        print("\n📝 Création des données de démonstration...")
        try:
            subprocess.run([sys.executable, "scripts/test_scraper.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur: {e}")
    
    elif choice == "4":
        print("\n🔧 Installation des dépendances...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "scripts/requirements.txt"], check=True)
            print("✅ Dépendances installées avec succès !")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation: {e}")
        except FileNotFoundError:
            print("❌ pip non trouvé. Assurez-vous que Python est installé.")
    
    else:
        print("❌ Choix invalide")
    
    print("\n🎯 Action terminée !")
    print("💡 Pour voir les résultats, rechargez votre site web")

if __name__ == "__main__":
    main()
