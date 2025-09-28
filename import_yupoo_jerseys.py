#!/usr/bin/env python3
"""
Script d'importation automatique des maillots depuis Yupoo
"""

import sys
import os
import json
import time
from datetime import datetime

# Ajouter le dossier scripts au path
sys.path.append('scripts')

from yupoo_scraper import YupooSpecializedScraper

def import_all_jerseys():
    """Importe tous les maillots depuis Yupoo"""
    
    print("🚀 Démarrage de l'importation Yupoo...")
    print("=" * 50)
    
    # Initialiser le scraper
    scraper = YupooSpecializedScraper()
    
    try:
        # 1. Tester la connexion
        print("🔍 Test de connexion à Yupoo...")
        if not scraper.test_connection():
            print("❌ Impossible de se connecter à Yupoo")
            return False
        
        print("✅ Connexion réussie !")
        
        # 2. Récupérer tous les albums
        print("\n📁 Récupération de tous les albums...")
        albums = scraper.get_all_albums()
        
        if not albums:
            print("❌ Aucun album trouvé")
            return False
        
        print(f"✅ {len(albums)} albums trouvés")
        
        # 3. Extraire les données de tous les albums
        print("\n🖼️ Extraction des données des maillots...")
        all_jerseys = []
        
        for i, album in enumerate(albums, 1):
            print(f"📸 Traitement album {i}/{len(albums)}: {album.get('title', 'Sans titre')}")
            
            try:
                jerseys = scraper.extract_album_data(album['url'])
                if jerseys:
                    all_jerseys.extend(jerseys)
                    print(f"   ✅ {len(jerseys)} maillots extraits")
                else:
                    print(f"   ⚠️ Aucun maillot trouvé dans cet album")
                    
                # Pause entre les albums pour éviter d'être bloqué
                time.sleep(2)
                
            except Exception as e:
                print(f"   ❌ Erreur sur l'album {i}: {e}")
                continue
        
        if not all_jerseys:
            print("❌ Aucun maillot extrait")
            return False
        
        print(f"\n🎉 Total: {len(all_jerseys)} maillots extraits !")
        
        # 4. Sauvegarder les données
        print("\n💾 Sauvegarde des données...")
        
        # Créer le dossier data s'il n'existe pas
        os.makedirs('data', exist_ok=True)
        
        # Sauvegarder dans jerseys.json
        with open('data/jerseys.json', 'w', encoding='utf-8') as f:
            json.dump(all_jerseys, f, ensure_ascii=False, indent=2)
        
        print("✅ Données sauvegardées dans data/jerseys.json")
        
        # 5. Créer un rapport
        create_import_report(all_jerseys)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'importation: {e}")
        return False

def create_import_report(jerseys):
    """Crée un rapport d'importation"""
    
    report = {
        "import_date": datetime.now().isoformat(),
        "total_jerseys": len(jerseys),
        "categories": {},
        "years": {},
        "statistics": {
            "with_images": 0,
            "without_images": 0,
            "with_descriptions": 0,
            "without_descriptions": 0
        }
    }
    
    # Analyser les catégories et années
    for jersey in jerseys:
        # Catégories
        category = jersey.get('category', 'unknown')
        report['categories'][category] = report['categories'].get(category, 0) + 1
        
        # Années
        year = jersey.get('year', 'unknown')
        report['years'][year] = report['years'].get(year, 0) + 1
        
        # Statistiques
        if jersey.get('images') and len(jersey['images']) > 0:
            report['statistics']['with_images'] += 1
        else:
            report['statistics']['without_images'] += 1
            
        if jersey.get('description') and jersey['description'].strip():
            report['statistics']['with_descriptions'] += 1
        else:
            report['statistics']['without_descriptions'] += 1
    
    # Sauvegarder le rapport
    with open('data/import_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("\n📊 Rapport d'importation créé:")
    print(f"   • Total maillots: {report['total_jerseys']}")
    print(f"   • Avec images: {report['statistics']['with_images']}")
    print(f"   • Sans images: {report['statistics']['without_images']}")
    print(f"   • Avec descriptions: {report['statistics']['with_descriptions']}")
    print(f"   • Sans descriptions: {report['statistics']['without_descriptions']}")
    
    print("\n📁 Catégories trouvées:")
    for category, count in report['categories'].items():
        print(f"   • {category}: {count} maillots")
    
    print("\n📅 Années trouvées:")
    for year, count in report['years'].items():
        print(f"   • {year}: {count} maillots")

def main():
    """Fonction principale"""
    
    print("🏆 Importation des maillots FC Palestina depuis Yupoo")
    print("=" * 60)
    
    # Vérifier que le scraper est disponible
    try:
        from yupoo_scraper import YupooSpecializedScraper
    except ImportError:
        print("❌ Le scraper Yupoo n'est pas disponible")
        print("   Assurez-vous que scripts/yupoo_scraper.py existe")
        return
    
    # Demander confirmation
    print("\n⚠️ Cette opération va:")
    print("   • Récupérer tous les maillots depuis Yupoo")
    print("   • Télécharger les images")
    print("   • Remplacer le fichier data/jerseys.json actuel")
    print("   • Prendre plusieurs minutes")
    
    response = input("\n❓ Voulez-vous continuer ? (o/n): ").lower().strip()
    
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Importation annulée")
        return
    
    # Lancer l'importation
    success = import_all_jerseys()
    
    if success:
        print("\n🎉 Importation terminée avec succès !")
        print("🔄 Rechargez votre site pour voir les nouveaux maillots")
    else:
        print("\n❌ Importation échouée")
        print("📋 Vérifiez les logs pour plus de détails")

if __name__ == "__main__":
    main()
