#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper Vinted avec Selenium pour extraire les avis réels
Nécessite l'exécution JavaScript pour charger le contenu dynamique
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
import requests

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('selenium_vinted_scraper.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class VintedReviewsSelenium:
    def __init__(self):
        self.url = "https://www.vinted.fr/member/287196181-maillotsdupeuple?tab=feedback"
        self.driver = None
        
    def setup_driver(self):
        """Configure le driver Selenium avec Chrome"""
        logger.info("🔧 Configuration du driver Selenium...")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Mode sans interface
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        
        try:
            # Utiliser webdriver-manager pour gérer ChromeDriver automatiquement
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("✅ Driver Selenium configuré avec succès")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur lors de la configuration du driver: {e}")
            # Fallback sans webdriver-manager
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                logger.info("✅ Driver Selenium configuré avec succès (fallback)")
                return True
            except Exception as e2:
                logger.error(f"❌ Erreur fallback: {e2}")
                return False
    
    def load_page_and_wait(self):
        """Charge la page et attend que le contenu se charge"""
        logger.info(f"🌐 Chargement de la page: {self.url}")
        
        try:
            self.driver.get(self.url)
            logger.info("📄 Page chargée, attente du contenu...")
            
            # Attendre que la page soit complètement chargée
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Attendre spécifiquement l'onglet feedback
            try:
                feedback_tab = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "feedback"))
                )
                logger.info("✅ Onglet feedback trouvé")
            except TimeoutException:
                logger.warning("⚠️ Onglet feedback non trouvé directement")
            
            # Attendre un peu plus pour que les avis se chargent
            time.sleep(5)
            
            # Faire défiler la page pour déclencher le chargement
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            logger.info("✅ Page entièrement chargée")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement de la page: {e}")
            return False
    
    def extract_reviews_from_dom(self):
        """Extrait les avis depuis le DOM après chargement JavaScript"""
        logger.info("🔍 Extraction des avis depuis le DOM...")
        
        reviews = []
        
        # Sélecteurs possibles pour les avis
        review_selectors = [
            "[data-testid*='feedback']",
            "[data-testid*='review']",
            ".feedback-item",
            ".review-item",
            ".user-feedback",
            "[class*='feedback']",
            "[class*='review']",
            "[class*='rating']"
        ]
        
        # Chercher dans tout le DOM
        page_source = self.driver.page_source
        
        # Vérifier si les utilisateurs sont maintenant présents
        target_users = ['rosiecol3', 'sosso3440']
        target_texts = ['stunning', 'qualité', 'recommande']
        
        found_users = []
        found_texts = []
        
        for user in target_users:
            if user.lower() in page_source.lower():
                found_users.append(user)
                logger.info(f"✅ Utilisateur '{user}' trouvé dans le DOM!")
        
        for text in target_texts:
            if text.lower() in page_source.lower():
                found_texts.append(text)
                logger.info(f"✅ Texte '{text}' trouvé dans le DOM!")
        
        # Essayer différents sélecteurs
        for selector in review_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    logger.info(f"✅ {len(elements)} éléments trouvés avec le sélecteur: {selector}")
                    
                    for element in elements:
                        text_content = element.text
                        if text_content and len(text_content) > 10:
                            logger.info(f"📝 Contenu trouvé: {text_content[:100]}...")
            except Exception as e:
                logger.debug(f"Sélecteur {selector} échoué: {e}")
        
        # Recherche directe des avis par mots-clés
        try:
            # Chercher tous les éléments contenant les termes d'avis
            all_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'stunning') or contains(text(), 'Stunning') or contains(text(), 'qualité') or contains(text(), 'recommande')]")
            
            if all_elements:
                logger.info(f"🎯 {len(all_elements)} éléments contenant les termes d'avis trouvés!")
                for element in all_elements:
                    text = element.text
                    if text:
                        logger.info(f"📝 Texte d'avis potentiel: {text}")
                        
                        # Essayer d'extraire les informations de l'avis
                        parent = element.find_element(By.XPATH, "./..")
                        context = parent.text
                        
                        review_data = {
                            'text': text,
                            'context': context,
                            'html': element.get_attribute('outerHTML')
                        }
                        reviews.append(review_data)
        
        except Exception as e:
            logger.error(f"❌ Erreur lors de la recherche directe: {e}")
        
        # Essayer de cliquer sur l'onglet feedback si nécessaire
        try:
            feedback_tab = self.driver.find_element(By.XPATH, "//li[contains(@id, 'feedback') or contains(text(), 'Évaluations')]")
            if feedback_tab:
                logger.info("🖱️ Tentative de clic sur l'onglet feedback...")
                self.driver.execute_script("arguments[0].click();", feedback_tab)
                time.sleep(3)
                
                # Recharger et analyser
                page_source = self.driver.page_source
                for user in target_users:
                    if user.lower() in page_source.lower():
                        logger.info(f"✅ Après clic: Utilisateur '{user}' maintenant trouvé!")
                        
        except Exception as e:
            logger.debug(f"Clic sur l'onglet feedback échoué: {e}")
        
        return reviews, found_users, found_texts
    
    def save_full_page_source(self):
        """Sauvegarde le code source complet après chargement JavaScript"""
        try:
            page_source = self.driver.page_source
            
            # Sauvegarder dans un nouveau fichier
            output_file = Path("selenium_vinted_page.html")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(page_source)
            
            logger.info(f"💾 Page source sauvegardée: {output_file} ({len(page_source)} caractères)")
            
            # Comparer avec l'ancienne version
            old_file = Path("debug_vinted_page.html")
            if old_file.exists():
                with open(old_file, 'r', encoding='utf-8') as f:
                    old_content = f.read()
                
                logger.info(f"📊 Ancienne version: {len(old_content)} caractères")
                logger.info(f"📊 Nouvelle version: {len(page_source)} caractères")
                logger.info(f"📊 Différence: {len(page_source) - len(old_content)} caractères")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde: {e}")
    
    def cleanup(self):
        """Ferme le driver"""
        if self.driver:
            self.driver.quit()
            logger.info("🔧 Driver fermé")
    
    def run(self):
        """Exécute le scraping complet"""
        logger.info("🚀 Démarrage du scraping Selenium des avis Vinted...")
        
        try:
            # 1. Configurer le driver
            if not self.setup_driver():
                logger.error("❌ Impossible de configurer le driver")
                return []
            
            # 2. Charger la page
            if not self.load_page_and_wait():
                logger.error("❌ Impossible de charger la page")
                return []
            
            # 3. Sauvegarder le source complet
            self.save_full_page_source()
            
            # 4. Extraire les avis
            reviews, found_users, found_texts = self.extract_reviews_from_dom()
            
            # 5. Résumé
            logger.info("📊 RÉSUMÉ DE L'EXTRACTION:")
            logger.info(f"  👥 Utilisateurs trouvés: {found_users}")
            logger.info(f"  📝 Textes trouvés: {found_texts}")
            logger.info(f"  ⭐ Avis extraits: {len(reviews)}")
            
            if reviews:
                logger.info("✅ AVIS TROUVÉS:")
                for i, review in enumerate(reviews):
                    logger.info(f"  {i+1}. {review['text'][:100]}...")
            
            return reviews
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du scraping: {e}")
            import traceback
            traceback.print_exc()
            return []
        
        finally:
            self.cleanup()

def check_selenium_requirements():
    """Vérifie si Selenium et ChromeDriver sont disponibles"""
    try:
        import selenium
        logger.info(f"✅ Selenium installé: version {selenium.__version__}")
        return True
    except ImportError:
        logger.error("❌ Selenium non installé. Installez avec: pip install selenium")
        return False

def main():
    """Fonction principale"""
    logger.info("🎯 SCRAPER VINTED AVEC SELENIUM")
    logger.info("="*50)
    
    # Vérifier les requirements
    if not check_selenium_requirements():
        logger.error("❌ Requirements manquants")
        return
    
    # Lancer le scraping
    scraper = VintedReviewsSelenium()
    reviews = scraper.run()
    
    if reviews:
        # Sauvegarder les résultats
        output_file = Path("data/selenium_reviews.json")
        output_file.parent.mkdir(exist_ok=True)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'url': scraper.url,
            'reviews_count': len(reviews),
            'reviews': reviews
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 Résultats sauvegardés: {output_file}")
    
    logger.info("🏁 Scraping terminé")

if __name__ == "__main__":
    main()