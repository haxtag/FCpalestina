#!/usr/bin/env python3
"""
Script de gestion rapide des avis
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def main():
    print("🌟 Gestionnaire d'Avis FC Palestina")
    print("=" * 40)
    
    while True:
        print("\nActions disponibles:")
        print("1. Scraper nouveaux avis Vinted")
        print("2. Voir les avis actuels")
        print("3. Ouvrir page de test")
        print("4. Ouvrir site complet")
        print("5. Quitter")
        
        choice = input("\nChoisissez une action (1-5): ").strip()
        
        if choice == '1':
            scrape_reviews()
        elif choice == '2':
            show_reviews()
        elif choice == '3':
            open_test_page()
        elif choice == '4':
            open_full_site()
        elif choice == '5':
            print("👋 À bientôt!")
            break
        else:
            print("❌ Choix invalide, essayez encore")

def scrape_reviews():
    print("\n🚀 Lancement du scraper d'avis...")
    try:
        result = subprocess.run([sys.executable, "scripts/vinted_reviews_scraper.py"], 
                              capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        if result.stderr:
            print("Erreurs:", result.stderr)
    except Exception as e:
        print(f"❌ Erreur: {e}")

def show_reviews():
    print("\n📝 Avis actuels:")
    reviews_file = Path("data/reviews.json")
    
    if not reviews_file.exists():
        print("❌ Aucun fichier d'avis trouvé")
        return
    
    try:
        with open(reviews_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        reviews = data.get('reviews', [])
        print(f"\n📊 Total: {len(reviews)} avis")
        print(f"📅 Dernière mise à jour: {data.get('last_updated', 'Inconnue')}")
        
        print("\n" + "="*50)
        for i, review in enumerate(reviews[:5], 1):  # Afficher les 5 premiers
            print(f"\n{i}. {review.get('author', 'Anonyme')} - {'⭐' * review.get('rating', 0)}")
            print(f"   {review.get('text', '')[:100]}...")
            print(f"   {review.get('date', '')}")
        
        if len(reviews) > 5:
            print(f"\n... et {len(reviews) - 5} autres avis")
            
    except Exception as e:
        print(f"❌ Erreur lecture avis: {e}")

def open_test_page():
    print("\n🧪 Ouverture de la page de test...")
    try:
        subprocess.run(["start", "test_reviews.html"], shell=True)
        print("✅ Page de test ouverte dans votre navigateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def open_full_site():
    print("\n🌐 Ouverture du site complet...")
    try:
        subprocess.run(["start", "index.html"], shell=True)
        print("✅ Site complet ouvert dans votre navigateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()