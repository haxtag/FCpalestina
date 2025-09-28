#!/usr/bin/env python3
"""
Script d'auto-update des avis Vinted
Se lance automatiquement au démarrage du site
"""

import os
import sys
import subprocess
import schedule
import time
import json
from datetime import datetime, timedelta
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_update_reviews.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ReviewsAutoUpdater:
    def __init__(self):
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.reviews_file = os.path.join(self.script_path, '..', 'data', 'reviews.json')
        self.scraper_script = os.path.join(self.script_path, 'vinted_reviews_scraper.py')
        
    def should_update(self) -> bool:
        """Vérifier s'il faut mettre à jour les avis"""
        try:
            if not os.path.exists(self.reviews_file):
                logger.info("Fichier d'avis inexistant, mise à jour nécessaire")
                return True
                
            # Lire la date de dernière mise à jour
            with open(self.reviews_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            last_update = data.get('last_updated')
            if not last_update:
                return True
                
            # Convertir en datetime
            last_update_dt = datetime.fromisoformat(last_update.replace('Z', '+00:00').replace('+00:00', ''))
            now = datetime.now()
            
            # Mettre à jour si plus de 6 heures
            if (now - last_update_dt) > timedelta(hours=6):
                logger.info(f"Dernière mise à jour il y a {now - last_update_dt}, mise à jour nécessaire")
                return True
                
            logger.info(f"Mise à jour récente ({last_update}), pas de mise à jour nécessaire")
            return False
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification: {e}")
            return True
    
    def update_reviews(self) -> bool:
        """Mettre à jour les avis en lançant le scraper"""
        try:
            logger.info("🔄 Lancement de la mise à jour des avis Vinted...")
            
            # Lancer le scraper
            result = subprocess.run([
                sys.executable, self.scraper_script
            ], capture_output=True, text=True, cwd=self.script_path)
            
            if result.returncode == 0:
                logger.info("✅ Mise à jour des avis réussie !")
                return True
            else:
                logger.error(f"❌ Erreur lors de la mise à jour: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Exception lors de la mise à jour: {e}")
            return False
    
    def run_update_if_needed(self):
        """Exécuter la mise à jour si nécessaire"""
        logger.info("🔍 Vérification des avis Vinted...")
        
        if self.should_update():
            logger.info("📥 Mise à jour des avis en cours...")
            success = self.update_reviews()
            if success:
                logger.info("🎉 Avis mis à jour avec succès !")
            else:
                logger.error("💥 Échec de la mise à jour des avis")
        else:
            logger.info("✅ Avis déjà à jour")
    
    def start_scheduler(self):
        """Démarrer le planificateur de tâches"""
        logger.info("📅 Démarrage du planificateur d'auto-update")
        
        # Vérifier immédiatement au démarrage
        self.run_update_if_needed()
        
        # Planifier des vérifications régulières
        schedule.every(6).hours.do(self.run_update_if_needed)
        schedule.every().day.at("08:00").do(self.run_update_if_needed)
        schedule.every().day.at("20:00").do(self.run_update_if_needed)
        
        logger.info("⏰ Planification configurée : toutes les 6h et à 8h/20h")
        
        # Boucle principale
        while True:
            schedule.run_pending()
            time.sleep(300)  # Vérifier toutes les 5 minutes

def main():
    """Fonction principale"""
    print("🚀 Auto-updater des avis Vinted - FC Palestina")
    print("=" * 50)
    
    updater = ReviewsAutoUpdater()
    
    # Mode direct ou planificateur
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # Mode une fois
        updater.run_update_if_needed()
    else:
        # Mode planificateur continu
        try:
            updater.start_scheduler()
        except KeyboardInterrupt:
            logger.info("🛑 Arrêt du planificateur")
        except Exception as e:
            logger.error(f"💥 Erreur du planificateur: {e}")

if __name__ == "__main__":
    main()