#!/usr/bin/env python3
"""
Scraper spécialisé pour Yupoo - Version optimisée pour FC Palestina
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
from urllib.parse import urljoin, urlparse, parse_qs
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
        logging.FileHandler('yupoo_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class YupooSpecializedScraper:
    """Scraper spécialisé pour Yupoo avec détection intelligente"""
    
    def __init__(self, base_url: str = "https://shixingtiyu.x.yupoo.com"):
        self.base_url = base_url
        self.session = requests.Session()
        
        # Configuration des headers pour Yupoo
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',  # Yupoo est chinois
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
        
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Récupérer une page avec gestion d'erreurs améliorée"""
        try:
            logger.info(f"Récupération: {url}")
            
            # Changer l'User-Agent
            self.session.headers['User-Agent'] = random.choice(self.user_agents)
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Détecter l'encodage
            if response.encoding == 'ISO-8859-1':
                response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Délai aléatoire
            time.sleep(random.uniform(1, 3))
            
            return soup
            
        except Exception as e:
            logger.error(f"Erreur pour {url}: {e}")
            return None
    
    def extract_jersey_data(self, album_url: str, soup: BeautifulSoup) -> Optional[Dict]:
        """Extraire les données d'un maillot depuis Yupoo"""
        try:
            # Titre - plusieurs méthodes pour Yupoo
            title = self.extract_title(soup)
            if not title:
                logger.warning(f"Titre non trouvé pour {album_url}")
                return None
            
            # Images - méthode spécialisée pour Yupoo
            images = self.extract_images(soup, album_url)
            if not images:
                logger.warning(f"Aucune image trouvée pour {album_url}")
                return None
            
            # Description
            description = self.extract_description(soup, title)
            
            # Catégorie basée sur le titre
            category = self.determine_category(title)
            
            # Année
            year = self.extract_year(title)
            
            # Générer l'ID
            jersey_id = self.generate_jersey_id(title, album_url)
            
            # Créer l'objet maillot
            jersey = {
                'id': jersey_id,
                'title': title,
                'description': description,
                'category': category,
                'year': year,
                'price': None,
                'images': images,
                'thumbnail': images[0] if images else None,
                'tags': self.generate_tags(title, description),
                'date': datetime.now().isoformat(),
                'views': random.randint(100, 2000),
                'featured': self.is_featured(title),
                'source_url': album_url,
                'last_updated': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Maillot extrait: {title} ({len(images)} images)")
            return jersey
            
        except Exception as e:
            logger.error(f"Erreur extraction {album_url}: {e}")
            return None
    
    def extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extraire le titre avec plusieurs méthodes"""
        # Méthodes pour Yupoo
        selectors = [
            'h1',
            '.album-title',
            '.gallery-title',
            '.photo-title',
            'title',
            '.item-title',
            '[class*="title"]',
            '[class*="name"]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                title = element.get_text(strip=True)
                if title and len(title) > 3 and 'yupoo' not in title.lower():
                    return title
        
        return None
    
    def extract_images(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extraire les images avec méthodes spécialisées pour Yupoo"""
        images = []
        
        # Sélecteurs d'images pour Yupoo
        img_selectors = [
            'img[src*="yupoo"]',
            'img[data-src*="yupoo"]',
            'img[data-original*="yupoo"]',
            '.photo img',
            '.gallery img',
            '.album img',
            '.item img',
            'img[class*="photo"]',
            'img[class*="gallery"]',
            'img[class*="album"]'
        ]
        
        for selector in img_selectors:
            elements = soup.select(selector)
            for img in elements:
                # Essayer différents attributs
                for attr in ['src', 'data-src', 'data-original', 'data-lazy']:
                    src = img.get(attr)
                    if src and self.is_valid_image_url(src):
                        # Convertir en URL absolue
                        if src.startswith('//'):
                            src = 'https:' + src
                        elif src.startswith('/'):
                            src = urljoin(base_url, src)
                        
                        if src not in images:
                            images.append(src)
        
        # Nettoyer et dédupliquer
        unique_images = list(dict.fromkeys(images))
        logger.info(f"Trouvé {len(unique_images)} images")
        
        return unique_images[:10]  # Limiter à 10 images par maillot
    
    def is_valid_image_url(self, url: str) -> bool:
        """Vérifier si l'URL est une image valide"""
        if not url:
            return False
        
        # Extensions d'images
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
        url_lower = url.lower()
        
        # Vérifier l'extension
        has_extension = any(url_lower.endswith(ext) for ext in valid_extensions)
        
        # Vérifier que c'est une image Yupoo
        is_yupoo_image = 'yupoo' in url_lower or 'photo' in url_lower
        
        return has_extension and is_yupoo_image
    
    def extract_description(self, soup: BeautifulSoup, title: str) -> str:
        """Extraire la description"""
        # Sélecteurs pour la description
        desc_selectors = [
            '.album-description',
            '.gallery-description',
            '.photo-description',
            '.item-description',
            '[class*="description"]',
            '[class*="desc"]'
        ]
        
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                desc = element.get_text(strip=True)
                if desc and len(desc) > 10:
                    return desc
        
        # Fallback: utiliser le titre comme description
        return f"Maillot FC Palestina - {title}"
    
    def determine_category(self, title: str) -> str:
        """Déterminer la catégorie basée sur le titre"""
        title_lower = title.lower()
        
        # Mots-clés pour les catégories
        if any(word in title_lower for word in ['domicile', 'home', 'maison', '主场']):
            return 'home'
        elif any(word in title_lower for word in ['extérieur', 'away', 'extérieur', '客场']):
            return 'away'
        elif any(word in title_lower for word in ['gardien', 'keeper', 'goal', '门将']):
            return 'keeper'
        elif any(word in title_lower for word in ['spécial', 'special', 'édition', 'edition', '特别', '限量']):
            return 'special'
        elif any(word in title_lower for word in ['vintage', 'rétro', 'retro', 'classic', '复古']):
            return 'vintage'
        else:
            return 'home'  # Par défaut
    
    def extract_year(self, title: str) -> int:
        """Extraire l'année du titre"""
        year_match = re.search(r'\b(19|20)\d{2}\b', title)
        if year_match:
            return int(year_match.group())
        return datetime.now().year
    
    def generate_jersey_id(self, title: str, url: str) -> str:
        """Générer un ID unique"""
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        clean_title = re.sub(r'[^a-zA-Z0-9]', '', title.lower())[:20]
        return f"jersey-{clean_title}-{url_hash}"
    
    def generate_tags(self, title: str, description: str) -> List[str]:
        """Générer des tags"""
        text = f"{title} {description}".lower()
        tags = []
        
        keywords = {
            'officiel': ['officiel', 'official', '官方'],
            '2024': ['2024'],
            '2023': ['2023'],
            'domicile': ['domicile', 'home', '主场'],
            'extérieur': ['extérieur', 'away', '客场'],
            'spécial': ['spécial', 'special', '特别'],
            'vintage': ['vintage', 'rétro', 'retro', '复古'],
            'gardien': ['gardien', 'keeper', '门将']
        }
        
        for tag, words in keywords.items():
            if any(word in text for word in words):
                tags.append(tag)
        
        return tags[:5]
    
    def is_featured(self, title: str) -> bool:
        """Déterminer si le maillot est mis en avant"""
        title_lower = title.lower()
        featured_keywords = ['spécial', 'special', 'édition', 'edition', 'limitée', 'exclusif', '特别', '限量']
        return any(keyword in title_lower for keyword in featured_keywords)
    
    def scrape_albums(self, max_pages: int = 3) -> List[Dict]:
        """Scraper les albums Yupoo"""
        logger.info("🚀 Début du scraping Yupoo")
        
        for page in range(1, max_pages + 1):
            try:
                # URL des albums Yupoo
                albums_url = f"{self.base_url}/albums?page={page}"
                soup = self.get_page(albums_url)
                
                if not soup:
                    logger.warning(f"Page {page} non accessible")
                    continue
                
                # Trouver les liens d'albums
                album_links = self.find_album_links(soup)
                
                if not album_links:
                    logger.info(f"Aucun album trouvé sur la page {page}")
                    break
                
                logger.info(f"Traitement de {len(album_links)} albums (page {page})")
                
                for album_url in album_links:
                    if album_url in self.processed_urls:
                        continue
                    
                    self.processed_urls.add(album_url)
                    
                    # Récupérer l'album
                    album_soup = self.get_page(album_url)
                    if not album_soup:
                        continue
                    
                    # Extraire les données
                    jersey = self.extract_jersey_data(album_url, album_soup)
                    if jersey:
                        self.jerseys.append(jersey)
                    
                    # Pause entre les albums
                    time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                logger.error(f"Erreur page {page}: {e}")
                continue
        
        logger.info(f"✅ Scraping terminé: {len(self.jerseys)} maillots trouvés")
        return self.jerseys
    
    def find_album_links(self, soup: BeautifulSoup) -> List[str]:
        """Trouver les liens d'albums Yupoo"""
        links = []
        
        # Sélecteurs spécifiques Yupoo
        selectors = [
            'a[href*="/albums/"]',
            'a[href*="/album/"]',
            '.album-item a',
            '.gallery-item a',
            '.photo-item a',
            'a[class*="album"]',
            'a[class*="gallery"]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                href = element.get('href')
                if href and '/albums/' in href:
                    if href.startswith('/'):
                        href = urljoin(self.base_url, href)
                    
                    if href not in links and href not in self.processed_urls:
                        links.append(href)
        
        return links[:15]  # Limiter à 15 albums par page
    
    def save_jerseys(self, filename: str = 'data/jerseys.json') -> bool:
        """Sauvegarder les maillots"""
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.jerseys, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 {len(self.jerseys)} maillots sauvegardés dans {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde: {e}")
            return False
    
    def run(self, max_pages: int = 3) -> bool:
        """Exécuter le scraping complet"""
        try:
            logger.info("=== Début du scraping Yupoo ===")
            
            # Scraper les albums
            jerseys = self.scrape_albums(max_pages)
            
            if jerseys:
                # Sauvegarder
                success = self.save_jerseys()
                if success:
                    logger.info("=== Scraping terminé avec succès ===")
                    return True
            
            logger.error("Aucun maillot trouvé")
            return False
            
        except Exception as e:
            logger.error(f"Erreur scraping: {e}")
            return False

def main():
    """Fonction principale"""
    print("🏆 Scraper Yupoo FC Palestina")
    print("=" * 40)
    
    # Configuration
    YUPOO_URL = input("URL Yupoo (Entrée pour défaut): ").strip()
    if not YUPOO_URL:
        YUPOO_URL = "https://shixingtiyu.x.yupoo.com"
    
    MAX_PAGES = input("Nombre de pages à scraper (défaut: 3): ").strip()
    if not MAX_PAGES:
        MAX_PAGES = 3
    else:
        MAX_PAGES = int(MAX_PAGES)
    
    # Créer et lancer le scraper
    scraper = YupooSpecializedScraper(YUPOO_URL)
    success = scraper.run(max_pages=MAX_PAGES)
    
    if success:
        print(f"✅ Scraping terminé ! {len(scraper.jerseys)} maillots trouvés")
        print("📁 Données sauvegardées dans data/jerseys.json")
        print("🌐 Rechargez votre site pour voir les nouveaux maillots")
    else:
        print("❌ Erreur lors du scraping")
        print("💡 Vérifiez l'URL et votre connexion internet")

if __name__ == "__main__":
    main()
