#!/usr/bin/env python3
"""
Script d'automatisation pour mise à jour automatique des avis Vinted
À exécuter tous les 2 jours via CRON sur l'hébergeur
"""

import sys
import os
from pathlib import Path
import logging
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

# Configuration du logging
log_file = Path(__file__).parent.parent / 'logs' / 'auto_update_vinted.log'
log_file.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Fonction principale d'automatisation"""
    logger.info("=" * 70)
    logger.info("🤖 MISE À JOUR AUTOMATIQUE DES AVIS VINTED")
    logger.info("=" * 70)
    logger.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Importer le scraper
        from complete_vinted_scraper import CompleteVintedReviewsScraper, update_reviews_json
        
        logger.info("🚀 Lancement du scraper Vinted...")
        
        # Créer et exécuter le scraper
        scraper = CompleteVintedReviewsScraper()
        reviews = scraper.run()
        
        if reviews:
            logger.info(f"📊 {len(reviews)} avis récupérés depuis Vinted")
            
            # Sauvegarder les données brutes (backup)
            raw_file = Path("data/vinted_reviews_complete.json")
            raw_file.parent.mkdir(exist_ok=True)
            
            import json
            raw_data = {
                'timestamp': datetime.now().isoformat(),
                'url': scraper.url,
                'reviews_count': len(reviews),
                'reviews': reviews
            }
            
            with open(raw_file, 'w', encoding='utf-8') as f:
                json.dump(raw_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 Backup sauvegardé: {raw_file}")
            
            # Mettre à jour reviews.json avec fusion intelligente
            success = update_reviews_json(reviews)
            
            if success:
                logger.info("✅ MISE À JOUR RÉUSSIE!")
                logger.info("🎯 Les nouveaux avis ont été intégrés au site")
                logger.info("📱 Le site web affichera automatiquement les nouveaux avis")
                return 0
            else:
                logger.error("❌ Échec de la mise à jour du fichier reviews.json")
                return 1
        else:
            logger.warning("⚠️ Aucun avis récupéré")
            logger.info("💡 Le fichier reviews.json reste inchangé")
            return 0
            
    except Exception as e:
        logger.error(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1
    
    finally:
        logger.info("=" * 70)
        logger.info("🏁 Fin de la mise à jour automatique")
        logger.info("=" * 70)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
