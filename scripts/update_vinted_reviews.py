#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de mise à jour automatique des avis Vinted
À exécuter périodiquement pour récupérer les nouveaux avis
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime
import time

# Import du scraper complet
from complete_vinted_scraper import CompleteVintedReviewsScraper

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_update_reviews.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class VintedReviewsUpdater:
    def __init__(self):
        self.reviews_file = Path("data/reviews.json")
        self.backup_dir = Path("data/backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def load_current_reviews(self):
        """Charge les avis actuels"""
        if not self.reviews_file.exists():
            return []
        
        try:
            with open(self.reviews_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('reviews', [])
        except Exception as e:
            logger.error(f"❌ Erreur lecture reviews.json: {e}")
            return []
    
    def backup_current_reviews(self):
        """Sauvegarde les avis actuels"""
        if not self.reviews_file.exists():
            logger.info("ℹ️ Pas de fichier de reviews à sauvegarder")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"reviews_backup_{timestamp}.json"
        
        try:
            import shutil
            shutil.copy2(self.reviews_file, backup_file)
            logger.info(f"💾 Sauvegarde: {backup_file}")
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde: {e}")
    
    def compare_reviews(self, current_reviews, new_reviews):
        """Compare les avis actuels avec les nouveaux"""
        current_comments = {review.get('comment', '') for review in current_reviews}
        new_comments = {review.get('comment', '') for review in new_reviews}
        
        # Nouveaux avis
        truly_new = [review for review in new_reviews 
                    if review.get('comment', '') not in current_comments]
        
        logger.info(f"📊 Comparaison:")
        logger.info(f"  - Avis actuels: {len(current_reviews)}")
        logger.info(f"  - Avis scrapés: {len(new_reviews)}")
        logger.info(f"  - Nouveaux avis: {len(truly_new)}")
        
        if truly_new:
            logger.info("🆕 Nouveaux avis trouvés:")
            for review in truly_new:
                logger.info(f"  • [{review.get('username', 'Anonyme')}] {review.get('comment', '')[:50]}...")
        
        return truly_new
    
    def update_reviews_if_needed(self, new_reviews):
        """Met à jour les avis si nécessaire"""
        current_reviews = self.load_current_reviews()
        truly_new = self.compare_reviews(current_reviews, new_reviews)
        
        if not truly_new:
            logger.info("✅ Aucun nouvel avis, pas de mise à jour nécessaire")
            return False
        
        # Faire une sauvegarde
        self.backup_current_reviews()
        
        # Combiner tous les avis (nouveaux + existants)
        all_reviews = new_reviews  # Prendre tous les avis scrapés comme référence
        
        # Reformater pour l'ID
        for i, review in enumerate(all_reviews):
            review['id'] = i + 1
        
        # Créer la structure finale
        reviews_data = {
            "last_updated": datetime.now().isoformat(),
            "source": "vinted_real_scraper_auto",
            "total_reviews": len(all_reviews),
            "new_reviews_count": len(truly_new),
            "reviews": all_reviews
        }
        
        # Sauvegarder
        with open(self.reviews_file, 'w', encoding='utf-8') as f:
            json.dump(reviews_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ Avis mis à jour: {len(all_reviews)} total ({len(truly_new)} nouveaux)")
        return True
    
    def run_update(self):
        """Exécute une mise à jour complète"""
        logger.info("🔄 MISE À JOUR AUTOMATIQUE DES AVIS VINTED")
        logger.info("="*50)
        
        try:
            # 1. Scraper les avis actuels
            logger.info("🕷️ Scraping des avis...")
            scraper = CompleteVintedReviewsScraper()
            new_reviews = scraper.run()
            
            if not new_reviews:
                logger.error("❌ Aucun avis récupéré")
                return False
            
            # 2. Comparer et mettre à jour si nécessaire
            updated = self.update_reviews_if_needed(new_reviews)
            
            # 3. Résumé
            if updated:
                logger.info("🎉 MISE À JOUR TERMINÉE AVEC SUCCÈS!")
                
                # Afficher un résumé des avis
                logger.info("\n📝 AVIS ACTUELS:")
                for i, review in enumerate(new_reviews, 1):
                    logger.info(f"  {i}. [{review['username']}] {review['comment']}")
            else:
                logger.info("✅ Pas de mise à jour nécessaire")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la mise à jour: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Fonction principale"""
    updater = VintedReviewsUpdater()
    success = updater.run_update()
    
    if success:
        logger.info("🏁 Mise à jour terminée")
    else:
        logger.error("❌ Échec de la mise à jour")
        sys.exit(1)

if __name__ == "__main__":
    main()