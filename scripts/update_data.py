#!/usr/bin/env python3
"""
Script de mise à jour automatique des données
"""

import schedule
import time
import logging
from scraper import YupooScraper
from datetime import datetime
import os
import json

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataUpdater:
    """Gestionnaire de mise à jour automatique des données"""
    
    def __init__(self):
        self.scraper = YupooScraper()
        self.last_update_file = 'data/last_update.json'
        
    def update_jerseys(self):
        """Mettre à jour les maillots"""
        try:
            logger.info("=== Début de la mise à jour automatique ===")
            
            # Charger les données existantes
            existing_jerseys = self.scraper.load_existing_jerseys()
            logger.info(f"{len(existing_jerseys)} maillots existants")
            
            # Scraper les nouveaux maillots (seulement 2 pages pour les mises à jour)
            new_jerseys = self.scraper.scrape_albums(max_pages=2)
            logger.info(f"{len(new_jerseys)} nouveaux maillots trouvés")
            
            # Fusionner les données
            all_jerseys = self.scraper.merge_jerseys(existing_jerseys, new_jerseys)
            
            # Sauvegarder
            success = self.scraper.save_jerseys()
            
            if success:
                # Mettre à jour le timestamp
                self.update_last_update_time()
                
                logger.info(f"=== Mise à jour terminée ===")
                logger.info(f"Total: {len(all_jerseys)} maillots")
                logger.info(f"Nouveaux: {len(new_jerseys)} maillots")
                
                # Envoyer une notification (optionnel)
                self.send_notification(len(new_jerseys))
                
                return True
            else:
                logger.error("Erreur lors de la sauvegarde")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour: {e}")
            return False
    
    def update_last_update_time(self):
        """Mettre à jour le timestamp de la dernière mise à jour"""
        try:
            update_info = {
                'last_update': datetime.now().isoformat(),
                'status': 'success'
            }
            
            with open(self.last_update_file, 'w') as f:
                json.dump(update_info, f, indent=2)
                
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du timestamp: {e}")
    
    def get_last_update_time(self):
        """Obtenir le timestamp de la dernière mise à jour"""
        try:
            if os.path.exists(self.last_update_file):
                with open(self.last_update_file, 'r') as f:
                    data = json.load(f)
                    return data.get('last_update')
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du timestamp: {e}")
        
        return None
    
    def send_notification(self, new_count):
        """Envoyer une notification (à personnaliser selon vos besoins)"""
        if new_count > 0:
            logger.info(f"🔔 {new_count} nouveaux maillots ajoutés !")
            
            # Ici vous pouvez ajouter :
            # - Envoi d'email
            # - Notification Discord/Slack
            # - Webhook
            # - etc.
    
    def check_for_updates(self):
        """Vérifier s'il y a des mises à jour disponibles"""
        try:
            # Vérifier la dernière mise à jour
            last_update = self.get_last_update_time()
            
            if last_update:
                last_update_dt = datetime.fromisoformat(last_update)
                time_since_update = datetime.now() - last_update_dt
                
                # Si plus de 6 heures depuis la dernière mise à jour
                if time_since_update.total_seconds() > 6 * 3600:
                    logger.info("Mise à jour nécessaire")
                    return True
                else:
                    logger.info("Pas de mise à jour nécessaire")
                    return False
            else:
                logger.info("Première mise à jour")
                return True
                
        except Exception as e:
            logger.error(f"Erreur lors de la vérification des mises à jour: {e}")
            return True
    
    def run_scheduled_update(self):
        """Exécuter la mise à jour programmée"""
        if self.check_for_updates():
            self.update_jerseys()
        else:
            logger.info("Mise à jour ignorée (trop récente)")
    
    def start_scheduler(self):
        """Démarrer le planificateur de tâches"""
        logger.info("Démarrage du planificateur de mises à jour")
        
        # Programmer les mises à jour
        schedule.every(2).hours.do(self.run_scheduled_update)  # Toutes les 2 heures
        schedule.every().day.at("09:00").do(self.update_jerseys)  # Tous les jours à 9h
        schedule.every().day.at("21:00").do(self.update_jerseys)  # Tous les jours à 21h
        
        logger.info("Planificateur configuré :")
        logger.info("- Mise à jour toutes les 2 heures")
        logger.info("- Mise à jour quotidienne à 9h et 21h")
        
        # Boucle principale
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Vérifier toutes les minutes
            except KeyboardInterrupt:
                logger.info("Arrêt du planificateur")
                break
            except Exception as e:
                logger.error(f"Erreur dans le planificateur: {e}")
                time.sleep(60)

def main():
    """Fonction principale"""
    updater = DataUpdater()
    
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "update":
            # Mise à jour manuelle
            updater.update_jerseys()
        elif command == "check":
            # Vérifier les mises à jour
            if updater.check_for_updates():
                print("Mise à jour nécessaire")
            else:
                print("Pas de mise à jour nécessaire")
        elif command == "start":
            # Démarrer le planificateur
            updater.start_scheduler()
        else:
            print("Commandes disponibles:")
            print("  update  - Mise à jour manuelle")
            print("  check   - Vérifier les mises à jour")
            print("  start   - Démarrer le planificateur")
    else:
        # Mise à jour par défaut
        updater.update_jerseys()

if __name__ == "__main__":
    main()
