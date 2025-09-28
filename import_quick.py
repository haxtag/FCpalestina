#!/usr/bin/env python3
"""
Importation rapide de quelques maillots depuis Yupoo
"""

import sys
import os
import json
from datetime import datetime

# Ajouter le dossier scripts au path
sys.path.append('scripts')

def import_quick():
    """Importe rapidement quelques maillots"""
    
    print("Importation rapide de quelques maillots depuis Yupoo")
    print("=" * 50)
    
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
        
        # Extraire seulement les 10 premiers albums
        print("\nExtraction des 10 premiers albums...")
        jerseys = []
        
        for i, album in enumerate(albums[:10], 1):
            print(f"Album {i}/10: {album['title']}")
            
            try:
                album_jerseys = scraper.extract_album_data(album['url'])
                if album_jerseys:
                    jerseys.extend(album_jerseys)
                    print(f"   {len(album_jerseys)} maillots extraits")
                else:
                    print(f"   Aucun maillot trouvé")
                    
            except Exception as e:
                print(f"   Erreur: {e}")
                continue
        
        if not jerseys:
            print("Aucun maillot extrait")
            return False
        
        print(f"\nTotal: {len(jerseys)} maillots extraits !")
        
        # Sauvegarder les données
        print("\nSauvegarde des données...")
        
        # Créer le dossier data s'il n'existe pas
        os.makedirs('data', exist_ok=True)
        
        # Sauvegarder dans jerseys.json
        with open('data/jerseys.json', 'w', encoding='utf-8') as f:
            json.dump(jerseys, f, ensure_ascii=False, indent=2)
        
        print("Données sauvegardées dans data/jerseys.json")
        
        # Créer un rapport
        create_report(jerseys)
        
        return True
        
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def create_report(jerseys):
    """Crée un rapport d'importation"""
    
    report = {
        "import_date": datetime.now().isoformat(),
        "total_jerseys": len(jerseys),
        "categories": {},
        "years": {}
    }
    
    # Analyser les catégories et années
    for jersey in jerseys:
        category = jersey.get('category', 'unknown')
        report['categories'][category] = report['categories'].get(category, 0) + 1
        
        year = jersey.get('year', 'unknown')
        report['years'][year] = report['years'].get(year, 0) + 1
    
    # Sauvegarder le rapport
    with open('data/import_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("\nRapport d'importation:")
    print(f"   Total maillots: {report['total_jerseys']}")
    
    print("\nCatégories:")
    for category, count in report['categories'].items():
        print(f"   {category}: {count} maillots")
    
    print("\nAnnées:")
    for year, count in report['years'].items():
        print(f"   {year}: {count} maillots")

def main():
    """Fonction principale"""
    
    print("Importation rapide de quelques maillots depuis Yupoo")
    print("=" * 50)
    
    # Lancer l'importation
    success = import_quick()
    
    if success:
        print("\nImportation terminée avec succès !")
        print("Rechargez votre site pour voir les nouveaux maillots")
    else:
        print("\nImportation échouée")

if __name__ == "__main__":
    main()
