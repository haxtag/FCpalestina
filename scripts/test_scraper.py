#!/usr/bin/env python3
"""
Script de test pour le scraper Yupoo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from yupoo_scraper import YupooSpecializedScraper
import json

def test_scraper():
    """Tester le scraper avec des données de démonstration"""
    print("🧪 Test du Scraper Yupoo")
    print("=" * 30)
    
    # Créer le scraper
    scraper = YupooSpecializedScraper()
    
    # Test 1: Vérifier la configuration
    print("1. Test de configuration...")
    print(f"   Base URL: {scraper.base_url}")
    print(f"   User-Agent: {scraper.session.headers['User-Agent'][:50]}...")
    print("   ✅ Configuration OK")
    
    # Test 2: Test de connexion
    print("\n2. Test de connexion...")
    try:
        soup = scraper.get_page(scraper.base_url)
        if soup:
            print("   ✅ Connexion réussie")
        else:
            print("   ❌ Connexion échouée")
            return False
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
        return False
    
    # Test 3: Test d'extraction de liens
    print("\n3. Test d'extraction de liens...")
    try:
        albums_url = f"{scraper.base_url}/albums"
        soup = scraper.get_page(albums_url)
        if soup:
            links = scraper.find_album_links(soup)
            print(f"   ✅ {len(links)} liens d'albums trouvés")
            if links:
                print(f"   Premier lien: {links[0]}")
        else:
            print("   ❌ Impossible de récupérer la page des albums")
    except Exception as e:
        print(f"   ❌ Erreur extraction liens: {e}")
    
    # Test 4: Test d'extraction d'un album
    print("\n4. Test d'extraction d'album...")
    try:
        if links and len(links) > 0:
            album_url = links[0]
            album_soup = scraper.get_page(album_url)
            if album_soup:
                jersey = scraper.extract_jersey_data(album_url, album_soup)
                if jersey:
                    print(f"   ✅ Maillot extrait: {jersey['title']}")
                    print(f"   📸 {len(jersey['images'])} images trouvées")
                    print(f"   🏷️  Catégorie: {jersey['category']}")
                else:
                    print("   ❌ Impossible d'extraire les données du maillot")
            else:
                print("   ❌ Impossible de récupérer l'album")
        else:
            print("   ⚠️  Aucun lien d'album pour le test")
    except Exception as e:
        print(f"   ❌ Erreur extraction album: {e}")
    
    print("\n🎯 Test terminé !")
    return True

def create_demo_data():
    """Créer des données de démonstration si le scraping échoue"""
    print("\n📝 Création de données de démonstration...")
    
    demo_jerseys = [
        {
            "id": "demo-jersey-1",
            "title": "Maillot Domicile FC Palestina 2024",
            "description": "Maillot officiel domicile FC Palestina saison 2024. Couleurs traditionnelles avec design moderne.",
            "category": "home",
            "year": 2024,
            "price": 89.99,
            "images": [
                "jersey-home-2024-1.jpg",
                "jersey-home-2024-2.jpg",
                "jersey-home-2024-3.jpg"
            ],
            "thumbnail": "jersey-home-2024-1.jpg",
            "tags": ["domicile", "2024", "officiel", "moderne"],
            "date": "2024-01-15T10:30:00",
            "views": 1250,
            "featured": True,
            "source_url": "https://demo.yupoo.com/album1",
            "last_updated": "2024-01-15T10:30:00"
        },
        {
            "id": "demo-jersey-2",
            "title": "Maillot Extérieur FC Palestina 2024",
            "description": "Maillot officiel extérieur FC Palestina saison 2024. Design élégant pour les matchs à l'extérieur.",
            "category": "away",
            "year": 2024,
            "price": 89.99,
            "images": [
                "jersey-away-2024-1.jpg",
                "jersey-away-2024-2.jpg",
                "jersey-away-2024-3.jpg"
            ],
            "thumbnail": "jersey-away-2024-1.jpg",
            "tags": ["extérieur", "2024", "officiel", "élégant"],
            "date": "2024-01-10T14:20:00",
            "views": 980,
            "featured": False,
            "source_url": "https://demo.yupoo.com/album2",
            "last_updated": "2024-01-10T14:20:00"
        },
        {
            "id": "demo-jersey-3",
            "title": "Maillot Spécial Liberté FC Palestina",
            "description": "Maillot spécial édition limitée \"Liberté\" avec design unique et message de solidarité.",
            "category": "special",
            "year": 2024,
            "price": 129.99,
            "images": [
                "jersey-special-2024-1.jpg",
                "jersey-special-2024-2.jpg",
                "jersey-special-2024-3.jpg"
            ],
            "thumbnail": "jersey-special-2024-1.jpg",
            "tags": ["spécial", "liberté", "édition limitée", "solidarité"],
            "date": "2024-02-01T09:15:00",
            "views": 2100,
            "featured": True,
            "source_url": "https://demo.yupoo.com/album3",
            "last_updated": "2024-02-01T09:15:00"
        }
    ]
    
    try:
        os.makedirs('data', exist_ok=True)
        with open('data/jerseys.json', 'w', encoding='utf-8') as f:
            json.dump(demo_jerseys, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ {len(demo_jerseys)} maillots de démonstration créés")
        print("   📁 Fichier: data/jerseys.json")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur création données démo: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test du Scraper Yupoo FC Palestina")
    print("=" * 50)
    
    # Demander le type de test
    print("Choisissez une option:")
    print("1. Test complet du scraper")
    print("2. Créer des données de démonstration")
    print("3. Test rapide de connexion")
    
    choice = input("\nVotre choix (1-3): ").strip()
    
    if choice == "1":
        # Test complet
        test_scraper()
        
        # Proposer de créer des données de démo si le test échoue
        create_demo = input("\nCréer des données de démonstration ? (o/n): ").strip().lower()
        if create_demo in ['o', 'oui', 'y', 'yes']:
            create_demo_data()
    
    elif choice == "2":
        # Créer des données de démonstration
        create_demo_data()
    
    elif choice == "3":
        # Test rapide
        scraper = YupooSpecializedScraper()
        print(f"Test de connexion à: {scraper.base_url}")
        
        try:
            soup = scraper.get_page(scraper.base_url)
            if soup:
                print("✅ Connexion réussie !")
            else:
                print("❌ Connexion échouée")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    else:
        print("❌ Choix invalide")
    
    print("\n🎯 Test terminé !")
    print("💡 Pour lancer le scraper complet: python scripts/yupoo_scraper.py")

if __name__ == "__main__":
    main()
