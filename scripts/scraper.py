#!/usr/bin/env python3
"""
Scraper pour synchroniser les maillots FC Palestina depuis Yupoo
Version améliorée et fonctionnelle
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
from urllib.parse import urljoin, urlparse
from datetime import datetime
import logging
from typing import List, Dict, Optional
import hashlib
import random
from PIL import Image
import io

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class YupooScraper:
    """Scraper pour récupérer les données depuis Yupoo"""
    
    def __init__(self, base_url: str = "https://shixingtiyu.x.yupoo.com"):
        self.base_url = base_url
        self.session = requests.Session()
        
        # Headers plus réalistes pour éviter la détection
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        self.jerseys = []
        self.processed_urls = set()
        self.downloaded_images = set()
        
        # Configuration
        self.max_retries = 3
        self.delay_between_requests = (1, 3)  # Délai aléatoire entre 1 et 3 secondes
        
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Récupérer et parser une page avec retry et délais"""
        for attempt in range(self.max_retries):
            try:
                # Changer l'User-Agent à chaque tentative
                self.session.headers['User-Agent'] = random.choice(self.user_agents)
                
                logger.info(f"Récupération de la page: {url} (tentative {attempt + 1})")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                # Détecter l'encodage
                response.encoding = response.apparent_encoding
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Délai aléatoire entre les requêtes
                delay = random.uniform(*self.delay_between_requests)
                time.sleep(delay)
                
                return soup
                
            except requests.RequestException as e:
                logger.warning(f"Tentative {attempt + 1} échouée pour {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Délai exponentiel
                else:
                    logger.error(f"Toutes les tentatives échouées pour {url}")
                    return None
    
    def extract_jersey_data(self, album_url: str, soup: BeautifulSoup) -> Optional[Dict]:
        """Extraire les données d'un maillot depuis une page d'album"""
        try:
            # Titre de l'album
            title_element = soup.find('h1') or soup.find('title')
            title = title_element.get_text(strip=True) if title_element else "Maillot FC Palestina"
            
            # Nettoyer le titre
            title = re.sub(r'\s+', ' ', title).strip()
            
            # Description
            description_element = soup.find('meta', {'name': 'description'})
            description = description_element.get('content', '') if description_element else title
            
            # Images
            images = []
            img_elements = soup.find_all('img', {'src': True})
            
            for img in img_elements:
                src = img.get('src')
                if src and self.is_valid_image(src):
                    # Convertir en URL absolue
                    full_url = urljoin(album_url, src)
                    images.append(full_url)
            
            # Dédupliquer les images
            images = list(dict.fromkeys(images))
            
            if not images:
                logger.warning(f"Aucune image trouvée pour {album_url}")
                return None
            
            # Déterminer la catégorie basée sur le titre
            category = self.determine_category(title)
            
            # Générer un ID unique
            jersey_id = self.generate_jersey_id(title, album_url)
            
            # Extraire l'année si possible
            year = self.extract_year(title)
            
            # Créer l'objet maillot
            jersey = {
                'id': jersey_id,
                'title': title,
                'description': description,
                'category': category,
                'year': year,
                'price': None,  # Prix non disponible sur Yupoo
                'images': images,
                'thumbnail': images[0] if images else None,
                'tags': self.generate_tags(title, description),
                'date': datetime.now().isoformat(),
                'views': 0,
                'featured': self.is_featured(title),
                'source_url': album_url,
                'last_updated': datetime.now().isoformat()
            }
            
            logger.info(f"Maillot extrait: {title} ({len(images)} images)")
            return jersey
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction des données de {album_url}: {e}")
            return None
    
    def is_valid_image(self, src: str) -> bool:
        """Vérifier si l'URL est une image valide"""
        if not src:
            return False
        
        # Extensions d'images supportées
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
        src_lower = src.lower()
        
        return any(src_lower.endswith(ext) for ext in valid_extensions)
    
    def determine_category(self, title: str) -> str:
        """Déterminer la catégorie basée sur le titre"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['domicile', 'home', 'maison']):
            return 'home'
        elif any(word in title_lower for word in ['extérieur', 'away', 'extérieur']):
            return 'away'
        elif any(word in title_lower for word in ['gardien', 'keeper', 'goal']):
            return 'keeper'
        elif any(word in title_lower for word in ['spécial', 'special', 'édition', 'edition', 'limitée']):
            return 'special'
        elif any(word in title_lower for word in ['vintage', 'rétro', 'retro', 'classic']):
            return 'vintage'
        else:
            return 'home'  # Par défaut
    
    def generate_jersey_id(self, title: str, url: str) -> str:
        """Générer un ID unique pour le maillot"""
        # Utiliser le hash de l'URL pour l'unicité
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        # Nettoyer le titre pour l'ID
        clean_title = re.sub(r'[^a-zA-Z0-9]', '', title.lower())[:20]
        return f"jersey-{clean_title}-{url_hash}"
    
    def extract_year(self, title: str) -> int:
        """Extraire l'année du titre"""
        year_match = re.search(r'\b(19|20)\d{2}\b', title)
        if year_match:
            return int(year_match.group())
        return datetime.now().year
    
    def generate_tags(self, title: str, description: str) -> List[str]:
        """Générer des tags basés sur le titre et la description"""
        text = f"{title} {description}".lower()
        tags = []
        
        # Mots-clés pour les tags
        keywords = {
            'officiel': ['officiel', 'official'],
            '2024': ['2024'],
            '2023': ['2023'],
            'domicile': ['domicile', 'home'],
            'extérieur': ['extérieur', 'away'],
            'spécial': ['spécial', 'special', 'édition', 'edition'],
            'vintage': ['vintage', 'rétro', 'retro'],
            'gardien': ['gardien', 'keeper'],
            'moderne': ['moderne', 'modern'],
            'classique': ['classique', 'classic']
        }
        
        for tag, words in keywords.items():
            if any(word in text for word in words):
                tags.append(tag)
        
        return tags[:5]  # Limiter à 5 tags
    
    def is_featured(self, title: str) -> bool:
        """Déterminer si le maillot est mis en avant"""
        title_lower = title.lower()
        featured_keywords = ['spécial', 'special', 'édition', 'edition', 'limitée', 'exclusif']
        return any(keyword in title_lower for keyword in featured_keywords)
    
    def scrape_albums(self, max_pages: int = 10) -> List[Dict]:
        """Scraper les albums de maillots"""
        logger.info("Début du scraping des albums Yupoo")
        
        for page in range(1, max_pages + 1):
            try:
                # URL des albums (à adapter selon la structure de Yupoo)
                albums_url = f"{self.base_url}/albums?page={page}"
                soup = self.get_page(albums_url)
                
                if not soup:
                    logger.warning(f"Impossible de récupérer la page {page}")
                    continue
                
                # Trouver les liens vers les albums
                album_links = self.find_album_links(soup)
                
                if not album_links:
                    logger.info(f"Aucun album trouvé sur la page {page}")
                    break
                
                logger.info(f"Traitement de {len(album_links)} albums sur la page {page}")
                
                for album_url in album_links:
                    if album_url in self.processed_urls:
                        continue
                    
                    self.processed_urls.add(album_url)
                    
                    # Récupérer la page de l'album
                    album_soup = self.get_page(album_url)
                    if not album_soup:
                        continue
                    
                    # Extraire les données du maillot
                    jersey = self.extract_jersey_data(album_url, album_soup)
                    if jersey:
                        self.jerseys.append(jersey)
                    
                    # Pause pour éviter d'être bloqué
                    time.sleep(1)
                
                # Pause entre les pages
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Erreur lors du scraping de la page {page}: {e}")
                continue
        
        logger.info(f"Scraping terminé. {len(self.jerseys)} maillots trouvés")
        return self.jerseys
    
    def find_album_links(self, soup: BeautifulSoup) -> List[str]:
        """Trouver les liens vers les albums avec sélecteurs Yupoo spécifiques"""
        links = []
        
        # Sélecteurs spécifiques à Yupoo
        selectors = [
            # Sélecteurs génériques
            'a[href*="/albums/"]',
            'a[href*="/album/"]',
            'a[href*="yupoo.com/albums"]',
            
            # Sélecteurs spécifiques Yupoo
            '.album-item a',
            '.gallery-item a',
            '.photo-item a',
            '.item a',
            '.album a',
            '.gallery a',
            
            # Sélecteurs par classe
            'a[class*="album"]',
            'a[class*="gallery"]',
            'a[class*="photo"]',
            'a[class*="item"]',
            
            # Sélecteurs par data-attribute
            'a[data-album]',
            'a[data-gallery]',
            
            # Sélecteurs génériques
            'a[href*="yupoo.com"]'
        ]
        
        for selector in selectors:
            try:
                elements = soup.select(selector)
                for element in elements:
                    href = element.get('href')
                    if href:
                        # Nettoyer et valider l'URL
                        if href.startswith('//'):
                            href = 'https:' + href
                        elif href.startswith('/'):
                            href = urljoin(self.base_url, href)
                        
                        # Vérifier que c'est bien un album
                        if any(pattern in href.lower() for pattern in ['/albums/', '/album/', 'yupoo.com']):
                            if href not in links and href not in self.processed_urls:
                                links.append(href)
            except Exception as e:
                logger.debug(f"Erreur avec le sélecteur {selector}: {e}")
                continue
        
        # Dédupliquer et limiter
        unique_links = list(dict.fromkeys(links))
        logger.info(f"Trouvé {len(unique_links)} liens d'albums")
        
        return unique_links[:20]  # Limiter à 20 albums par page
    
    def save_jerseys(self, filename: str = 'data/jerseys.json') -> bool:
        """Sauvegarder les maillots dans un fichier JSON"""
        try:
            # Créer le dossier data s'il n'existe pas
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.jerseys, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Données sauvegardées dans {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    def load_existing_jerseys(self, filename: str = 'data/jerseys.json') -> List[Dict]:
        """Charger les maillots existants"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données existantes: {e}")
        
        return []
    
    def merge_jerseys(self, existing: List[Dict], new: List[Dict]) -> List[Dict]:
        """Fusionner les maillots existants et nouveaux"""
        # Créer un dictionnaire des maillots existants par ID
        existing_dict = {jersey['id']: jersey for jersey in existing}
        
        # Mettre à jour ou ajouter les nouveaux maillots
        for jersey in new:
            if jersey['id'] in existing_dict:
                # Mettre à jour le maillot existant
                existing_dict[jersey['id']].update(jersey)
                existing_dict[jersey['id']]['last_updated'] = datetime.now().isoformat()
            else:
                # Ajouter le nouveau maillot
                existing_dict[jersey['id']] = jersey
        
        return list(existing_dict.values())
    
    def run(self, max_pages: int = 10, update_existing: bool = True) -> bool:
        """Exécuter le scraping complet"""
        try:
            logger.info("=== Début du scraping Yupoo ===")
            
            # Charger les données existantes
            existing_jerseys = []
            if update_existing:
                existing_jerseys = self.load_existing_jerseys()
                logger.info(f"{len(existing_jerseys)} maillots existants chargés")
            
            # Scraper les nouveaux maillots
            new_jerseys = self.scrape_albums(max_pages)
            
            # Fusionner les données
            if update_existing:
                all_jerseys = self.merge_jerseys(existing_jerseys, new_jerseys)
            else:
                all_jerseys = new_jerseys
            
            # Sauvegarder
            success = self.save_jerseys()
            
            if success:
                logger.info(f"=== Scraping terminé avec succès ===")
                logger.info(f"Total: {len(all_jerseys)} maillots")
                logger.info(f"Nouveaux: {len(new_jerseys)} maillots")
                return True
            else:
                logger.error("Erreur lors de la sauvegarde")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors du scraping: {e}")
            return False

def main():
    """Fonction principale"""
    scraper = YupooScraper()
    
    # Configuration
    MAX_PAGES = 5  # Nombre de pages à scraper
    UPDATE_EXISTING = True  # Mettre à jour les données existantes
    
    # Exécuter le scraping
    success = scraper.run(max_pages=MAX_PAGES, update_existing=UPDATE_EXISTING)
    
    if success:
        print("✅ Scraping terminé avec succès !")
        print(f"📊 {len(scraper.jerseys)} maillots traités")
    else:
        print("❌ Erreur lors du scraping")
        exit(1)

if __name__ == "__main__":
    main()
