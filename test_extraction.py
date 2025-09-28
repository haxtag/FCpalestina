#!/usr/bin/env python3
"""
Test d'extraction rapide depuis Yupoo
"""

import sys
import os
import json
from datetime import datetime

# Ajouter le dossier scripts au path
sys.path.append('scripts')

def test_extraction():
    """Test d'extraction de quelques albums"""
    
    print("Test d'extraction rapide depuis Yupoo")
    print("=" * 40)
    
    try:
        from smart_yupoo_scraper import SmartYupooScraper
        
        # Initialiser le scraper
        scraper = SmartYupooScraper()
        
        # Tester la connexion
        print("Test de connexion...")
        if not scraper.test_connection():
            print("Impossible de se connecter à Yupoo")
            return False
        
        print("Connexion réussie !")
        
        # Récupérer tous les albums
        print("\nRécupération des albums...")
        albums = scraper.get_all_albums()
        
        if not albums:
            print("Aucun album trouvé")
            return False
        
        print(f"{len(albums)} albums trouvés")
        
        # Tester l'extraction sur les 5 premiers albums
        print("\nTest d'extraction sur les 5 premiers albums...")
        test_jerseys = []
        
        for i, album in enumerate(albums[:5], 1):
            print(f"Album {i}/5: {album['title']}")
            
            try:
                jerseys = scraper.extract_album_data(album['url'])
                if jerseys:
                    test_jerseys.extend(jerseys)
                    print(f"   {len(jerseys)} maillots extraits")
                else:
                    print(f"   Aucun maillot trouvé")
                    
            except Exception as e:
                print(f"   Erreur: {e}")
                continue
        
        if not test_jerseys:
            print("Aucun maillot extrait lors du test")
            return False
        
        print(f"\nTest réussi ! {len(test_jerseys)} maillots extraits")
        
        # Afficher quelques exemples
        print("\nExemples de maillots extraits:")
        for i, jersey in enumerate(test_jerseys[:3], 1):
            print(f"{i}. {jersey['title']} ({jersey['category']}) - {jersey['year']}")
        
        # Sauvegarder le test
        os.makedirs('data', exist_ok=True)
        with open('data/test_jerseys.json', 'w', encoding='utf-8') as f:
            json.dump(test_jerseys, f, ensure_ascii=False, indent=2)
        
        print(f"\nTest sauvegardé dans data/test_jerseys.json")
        
        return True
        
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    
    print("Test d'extraction rapide depuis Yupoo")
    print("=" * 40)
    
    success = test_extraction()
    
    if success:
        print("\nTest réussi ! Le scraper fonctionne correctement.")
        print("Vous pouvez maintenant lancer l'importation complète avec:")
        print("python import_smart.py")
    else:
        print("\nTest échoué. Vérifiez la configuration.")

if __name__ == "__main__":
    main()
