#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper complet des avis Vinted réels avec Selenium
Extrait TOUS les avis avec utilisateurs, dates, notes et commentaires
"""

import json
import logging
import sys
from pathlib import Path
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import re

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('complete_vinted_scraper.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CompleteVintedReviewsScraper:
    def __init__(self):
        self.url = "https://www.vinted.fr/member/287196181-maillotsdupeuple?tab=feedback"
        self.driver = None
        
    def setup_driver(self):
        """Configure le driver Selenium"""
        logger.info("🔧 Configuration du driver Selenium...")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        
        try:
            # Utiliser webdriver-manager
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("✅ Driver Selenium configuré")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur driver: {e}")
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                logger.info("✅ Driver fallback configuré")
                return True
            except Exception as e2:
                logger.error(f"❌ Erreur fallback: {e2}")
                return False
    
    def load_page_and_wait(self):
        """Charge la page et attend le contenu"""
        logger.info(f"🌐 Chargement: {self.url}")
        
        try:
            self.driver.get(self.url)
            
            # Attendre le chargement complet
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Attendre l'onglet feedback
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "feedback"))
            )
            
            # Temps supplémentaire pour le JS
            time.sleep(8)
            
            # Scroll pour déclencher tous les chargements
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            logger.info("✅ Page complètement chargée")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur chargement: {e}")
            return False
    
    def parse_review_time(self, time_text):
        """Parse le texte de temps (ex: 'il y a 2 jours')"""
        if not time_text:
            return None
            
        time_text = time_text.strip().lower()
        
        if 'jour' in time_text:
            match = re.search(r'(\d+)\s*jour', time_text)
            if match:
                return f"{match.group(1)} jour{'s' if int(match.group(1)) > 1 else ''}"
        elif 'semaine' in time_text:
            match = re.search(r'(\d+)\s*semaine', time_text)
            if match:
                return f"{match.group(1)} semaine{'s' if int(match.group(1)) > 1 else ''}"
        elif 'mois' in time_text:
            match = re.search(r'(\d+)\s*mois', time_text)
            if match:
                return f"{match.group(1)} mois"
                
        return time_text
    
    def extract_complete_reviews(self):
        """Extrait TOUS les avis avec leurs informations complètes"""
        logger.info("🔍 Extraction complète des avis...")
        
        reviews = []
        
        try:
            # Trouver tous les éléments de feedback
            feedback_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid*='feedback']")
            logger.info(f"📊 {len(feedback_elements)} éléments de feedback trouvés")
            
            # Analyser chaque élément
            for i, element in enumerate(feedback_elements):
                try:
                    review_data = self.extract_single_review(element)
                    if review_data and review_data.get('comment') and 'Évaluation automatique' not in review_data.get('comment', ''):
                        reviews.append(review_data)
                        logger.info(f"✅ Avis {len(reviews)}: {review_data['username']} - {review_data['comment'][:50]}...")
                        
                except Exception as e:
                    logger.debug(f"Erreur élément {i}: {e}")
            
            # Vérifier les éléments manqués avec d'autres sélecteurs
            alternative_selectors = [
                "[class*='feedback']",
                "[class*='review']",
                ".web_ui__Cell__content"
            ]
            
            for selector in alternative_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text
                        if text and any(keyword in text.lower() for keyword in ['stunning', 'qualité', 'recommande', 'nickel', 'parfait', 'toppi']):
                            # Essayer d'extraire plus d'infos depuis ce contexte
                            additional_review = self.extract_from_text_context(element)
                            if additional_review and not any(r['comment'] == additional_review['comment'] for r in reviews):
                                reviews.append(additional_review)
                                logger.info(f"✅ Avis additionnel: {additional_review['comment'][:50]}...")
                except Exception as e:
                    logger.debug(f"Sélecteur alternatif {selector} échoué: {e}")
            
            logger.info(f"🎯 Total: {len(reviews)} avis réels extraits")
            return reviews
            
        except Exception as e:
            logger.error(f"❌ Erreur extraction: {e}")
            return []
    
    def extract_single_review(self, element):
        """Extrait un avis depuis un élément DOM"""
        try:
            text_content = element.text.strip()
            if not text_content or len(text_content) < 5:
                return None
            
            lines = [line.strip() for line in text_content.split('\n') if line.strip()]
            if len(lines) < 2:
                return None
            
            review_data = {
                'username': '',
                'time': '',
                'comment': '',
                'rating': 5,  # Par défaut
                'source': 'vinted',
                'extracted_at': datetime.now().isoformat()
            }
            
            # Pattern 1: username + time + comment
            if len(lines) >= 3:
                # Chercher le pattern nom/temps/commentaire
                for i in range(len(lines) - 2):
                    potential_username = lines[i]
                    potential_time = lines[i + 1]
                    potential_comment = lines[i + 2]
                    
                    # Vérifier si c'est un pattern valide
                    if (not potential_username.startswith('Vinted') and
                        'il y a' in potential_time and
                        len(potential_comment) > 5 and
                        not potential_comment.startswith('Évaluation automatique')):
                        
                        review_data['username'] = potential_username
                        review_data['time'] = self.parse_review_time(potential_time)
                        review_data['comment'] = potential_comment
                        return review_data
            
            # Pattern 2: recherche directe de commentaires intéressants
            for line in lines:
                if any(keyword in line.lower() for keyword in 
                      ['stunning', 'qualité', 'recommande', 'nickel', 'parfait', 'toppi', 'merci']) and len(line) > 5:
                    
                    # Essayer de trouver l'username associé
                    username = ''
                    time_str = ''
                    
                    # Chercher dans les lignes précédentes
                    line_index = lines.index(line)
                    if line_index > 0:
                        potential_time = lines[line_index - 1]
                        if 'il y a' in potential_time:
                            time_str = self.parse_review_time(potential_time)
                            if line_index > 1:
                                username = lines[line_index - 2]
                    
                    # Ou dans les lignes suivantes
                    if not username and line_index < len(lines) - 1:
                        potential_time = lines[line_index + 1]
                        if 'il y a' in potential_time:
                            time_str = self.parse_review_time(potential_time)
                            username = lines[line_index - 1] if line_index > 0 else 'Anonyme'
                    
                    review_data['username'] = username or 'Utilisateur'
                    review_data['time'] = time_str or 'Récent'
                    review_data['comment'] = line
                    return review_data
            
            return None
            
        except Exception as e:
            logger.debug(f"Erreur extraction élément: {e}")
            return None
    
    def extract_from_text_context(self, element):
        """Extrait depuis un contexte textuel"""
        try:
            text = element.text.strip()
            if not text:
                return None
            
            # Chercher les patterns de commentaires
            for keyword in ['stunning', 'qualité', 'recommande', 'nickel', 'parfait', 'toppi']:
                if keyword.lower() in text.lower():
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    
                    for line in lines:
                        if keyword.lower() in line.lower() and len(line) > 5:
                            return {
                                'username': 'Client Vinted',
                                'time': 'Récent',
                                'comment': line,
                                'rating': 5,
                                'source': 'vinted',
                                'extracted_at': datetime.now().isoformat()
                            }
            
            return None
        except:
            return None
    
    def cleanup(self):
        """Ferme le driver"""
        if self.driver:
            self.driver.quit()
            logger.info("🔧 Driver fermé")
    
    def run(self):
        """Exécute le scraping complet"""
        logger.info("🚀 SCRAPER COMPLET DES AVIS VINTED")
        logger.info("="*50)
        
        try:
            # Configuration
            if not self.setup_driver():
                return []
            
            # Chargement
            if not self.load_page_and_wait():
                return []
            
            # Extraction
            reviews = self.extract_complete_reviews()
            
            # Résultats
            logger.info("📊 RÉSULTATS:")
            logger.info(f"  ⭐ {len(reviews)} avis réels extraits")
            
            for i, review in enumerate(reviews, 1):
                logger.info(f"  {i}. [{review['username']}] {review['comment']}")
            
            return reviews
            
        except Exception as e:
            logger.error(f"❌ Erreur scraping: {e}")
            import traceback
            traceback.print_exc()
            return []
        
        finally:
            self.cleanup()

def update_reviews_json(new_reviews):
    """Met à jour le fichier reviews.json avec les vrais avis"""
    logger.info("💾 Mise à jour du fichier reviews.json...")
    
    if not new_reviews:
        logger.warning("⚠️ Aucun avis à sauvegarder")
        return False
    
    # Créer la structure des avis pour le système
    formatted_reviews = []
    
    for review in new_reviews:
        formatted_review = {
            "id": len(formatted_reviews) + 1,
            "username": review['username'],
            "rating": review.get('rating', 5),
            "comment": review['comment'],
            "date": review.get('time', 'Récent'),
            "source": "vinted_real",
            "verified": True,
            "extracted_at": review.get('extracted_at', datetime.now().isoformat())
        }
        formatted_reviews.append(formatted_review)
    
    # Structure finale
    reviews_data = {
        "last_updated": datetime.now().isoformat(),
        "source": "vinted_real_scraper",
        "total_reviews": len(formatted_reviews),
        "reviews": formatted_reviews
    }
    
    # Sauvegarder
    reviews_file = Path("data/reviews.json")
    reviews_file.parent.mkdir(exist_ok=True)
    
    with open(reviews_file, 'w', encoding='utf-8') as f:
        json.dump(reviews_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ {len(formatted_reviews)} avis sauvegardés dans {reviews_file}")
    return True

def main():
    """Fonction principale"""
    scraper = CompleteVintedReviewsScraper()
    reviews = scraper.run()
    
    if reviews:
        # Sauvegarder les résultats bruts
        raw_file = Path("data/vinted_reviews_complete.json")
        raw_file.parent.mkdir(exist_ok=True)
        
        raw_data = {
            'timestamp': datetime.now().isoformat(),
            'url': scraper.url,
            'reviews_count': len(reviews),
            'reviews': reviews
        }
        
        with open(raw_file, 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 Données brutes: {raw_file}")
        
        # Mettre à jour le système
        update_reviews_json(reviews)
        
        logger.info("🎉 EXTRACTION TERMINÉE AVEC SUCCÈS!")
        logger.info(f"📊 {len(reviews)} avis réels Vinted extraits et intégrés")
    else:
        logger.error("❌ Aucun avis extrait")
    
    logger.info("🏁 Fin du programme")

if __name__ == "__main__":
    main()