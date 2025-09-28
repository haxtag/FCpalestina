#!/usr/bin/env python3
"""
Test rapide de connexion et extraction depuis Yupoo
"""

import sys
import os

# Ajouter le dossier scripts au path
sys.path.append('scripts')

def test_yupoo_connection():
    """Test rapide de connexion à Yupoo"""
    
    print("🔍 Test de connexion à Yupoo...")
    print("=" * 40)
    
    try:
        from yupoo_scraper import YupooSpecializedScraper
        
        # Initialiser le scraper
        scraper = YupooSpecializedScraper()
        
        # Test 1: Connexion
        print("1️⃣ Test de connexion...")
        if scraper.test_connection():
            print("   ✅ Connexion réussie !")
        else:
            print("   ❌ Connexion échouée")
            return False
        
        # Test 2: Récupération des albums
        print("\n2️⃣ Test de récupération des albums...")
        albums = scraper.get_all_albums()
        
        if albums:
            print(f"   ✅ {len(albums)} albums trouvés")
            
            # Afficher les premiers albums
            print("   📁 Premiers albums:")
            for i, album in enumerate(albums[:5], 1):
                title = album.get('title', 'Sans titre')
                print(f"      {i}. {title}")
            
            if len(albums) > 5:
                print(f"      ... et {len(albums) - 5} autres albums")
                
        else:
            print("   ❌ Aucun album trouvé")
            return False
        
        # Test 3: Extraction d'un album (premier album)
        print("\n3️⃣ Test d'extraction d'un album...")
        if albums:
            first_album = albums[0]
            print(f"   📸 Test sur: {first_album.get('title', 'Sans titre')}")
            
            try:
                jerseys = scraper.extract_album_data(first_album['url'])
                
                if jerseys:
                    print(f"   ✅ {len(jerseys)} maillots extraits")
                    
                    # Afficher le premier maillot
                    if jerseys:
                        first_jersey = jerseys[0]
                        print("   🏆 Premier maillot:")
                        print(f"      • Titre: {first_jersey.get('title', 'N/A')}")
                        print(f"      • Catégorie: {first_jersey.get('category', 'N/A')}")
                        print(f"      • Année: {first_jersey.get('year', 'N/A')}")
                        print(f"      • Images: {len(first_jersey.get('images', []))}")
                        print(f"      • Description: {len(first_jersey.get('description', ''))} caractères")
                        
                else:
                    print("   ⚠️ Aucun maillot extrait de cet album")
                    
            except Exception as e:
                print(f"   ❌ Erreur lors de l'extraction: {e}")
                return False
        
        print("\n🎉 Tous les tests sont passés !")
        print("✅ Le scraper est prêt pour l'importation complète")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("   Vérifiez que scripts/yupoo_scraper.py existe")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def main():
    """Fonction principale"""
    
    print("🧪 Test de connexion Yupoo")
    print("=" * 30)
    
    success = test_yupoo_connection()
    
    if success:
        print("\n✅ Le scraper fonctionne correctement !")
        print("🚀 Vous pouvez maintenant lancer l'importation complète avec:")
        print("   python import_yupoo_jerseys.py")
    else:
        print("\n❌ Le scraper a des problèmes")
        print("🔧 Vérifiez la configuration et les dépendances")

if __name__ == "__main__":
    main()
