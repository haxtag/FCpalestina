#!/usr/bin/env python3
"""
Script d'importation par lots depuis Yupoo
"""

import sys
import os
import json
import time
from datetime import datetime

# Ajouter le dossier scripts au path
sys.path.append('scripts')

def import_jerseys_batch(batch_size=10):
    """Importe les maillots par lots"""
    
    print("Importation des maillots FC Palestina depuis Yupoo (par lots)")
    print("=" * 60)
    
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
        
        # Traiter par lots
        all_jerseys = []
        total_batches = (len(albums) + batch_size - 1) // batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(albums))
            batch_albums = albums[start_idx:end_idx]
            
            print(f"\nTraitement du lot {batch_num + 1}/{total_batches} (albums {start_idx + 1}-{end_idx})")
            
            for i, album in enumerate(batch_albums, 1):
                print(f"  Album {start_idx + i}/{len(albums)}: {album['title']}")
                
                try:
                    jerseys = scraper.extract_album_data(album['url'])
                    if jerseys:
                        all_jerseys.extend(jerseys)
                        print(f"    {len(jerseys)} maillots extraits")
                    else:
                        print(f"    Aucun maillot trouvé")
                        
                except Exception as e:
                    print(f"    Erreur: {e}")
                    continue
            
            # Pause entre les lots
            if batch_num < total_batches - 1:
                print(f"  Pause de 3 secondes avant le lot suivant...")
                time.sleep(3)
        
        if not all_jerseys:
            print("Aucun maillot extrait")
            return False
        
        print(f"\nTotal: {len(all_jerseys)} maillots extraits !")
        
        # Sauvegarder les données
        print("\nSauvegarde des données...")
        
        # Créer le dossier data s'il n'existe pas
        os.makedirs('data', exist_ok=True)
        
        # Sauvegarder dans jerseys.json
        with open('data/jerseys.json', 'w', encoding='utf-8') as f:
            json.dump(all_jerseys, f, ensure_ascii=False, indent=2)
        
        print("Données sauvegardées dans data/jerseys.json")
        
        # Créer un rapport
        create_report(all_jerseys)
        
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
    
    print("Importation des maillots FC Palestina depuis Yupoo (par lots)")
    print("=" * 60)
    
    # Demander la taille des lots
    print("\nChoisissez la taille des lots:")
    print("1. Petits lots (5 albums) - Plus lent mais plus sûr")
    print("2. Lots moyens (10 albums) - Équilibré")
    print("3. Gros lots (20 albums) - Plus rapide mais plus risqué")
    
    choice = input("\nVotre choix (1/2/3): ").strip()
    
    if choice == "1":
        batch_size = 5
    elif choice == "3":
        batch_size = 20
    else:
        batch_size = 10  # Par défaut
    
    print(f"\nTaille des lots: {batch_size} albums")
    
    # Demander confirmation
    print("\nCette opération va:")
    print("   Récupérer tous les maillots depuis Yupoo")
    print("   Remplacer le fichier data/jerseys.json actuel")
    print("   Prendre plusieurs minutes")
    
    response = input("\nVoulez-vous continuer ? (o/n): ").lower().strip()
    
    if response not in ['o', 'oui', 'y', 'yes']:
        print("Importation annulée")
        return
    
    # Lancer l'importation
    success = import_jerseys_batch(batch_size)
    
    if success:
        print("\nImportation terminée avec succès !")
        print("Rechargez votre site pour voir les nouveaux maillots")
    else:
        print("\nImportation échouée")

if __name__ == "__main__":
    main()
