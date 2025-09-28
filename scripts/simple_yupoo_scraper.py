#!/usr/bin/env python3
"""
Scraper simplifié pour Yupoo - FC Palestina
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
import random

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

class SimpleYupooScraper:
    """Scraper simplifié pour Yupoo"""
    
    def __init__(self, base_url: str = "https://shixingtiyu.x.yupoo.com"):
        self.base_url = base_url
        self.session = requests.Session()
        
        # Headers pour Yupoo
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        })
    
    def test_connection(self) -> bool:
        """Tester la connexion à Yupoo"""
        try:
            logger.info("Test de connexion à Yupoo...")
            response = self.session.get(self.base_url, timeout=30)
            response.raise_for_status()
            logger.info("✅ Connexion réussie !")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur de connexion: {e}")
            return False
    
    def get_all_albums(self) -> list:
        """Récupérer tous les albums"""
        try:
            logger.info("Récupération des albums...")
            response = self.session.get(f"{self.base_url}/albums", timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            albums = []
            
            # Chercher les liens d'albums
            album_links = soup.find_all('a', href=re.compile(r'/albums/\d+'))
            
            for link in album_links:
                href = link.get('href')
                if href:
                    full_url = urljoin(self.base_url, href)
                    title = link.get_text(strip=True) or "Album sans titre"
                    
                    albums.append({
                        'url': full_url,
                        'title': title
                    })
            
            logger.info(f"✅ {len(albums)} albums trouvés")
            return albums
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération des albums: {e}")
            return []
    
    def extract_album_data(self, album_url: str) -> list:
        """Extraire les données d'un album"""
        try:
            logger.info(f"Extraction de l'album: {album_url}")
            response = self.session.get(album_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            jerseys = []
            
            # Chercher les images dans l'album
            images = soup.find_all('img')
            
            for img in images:
                src = img.get('src') or img.get('data-src')
                if src and ('jersey' in src.lower() or 'maillot' in src.lower() or 'shirt' in src.lower()):
                    # Extraire le titre
                    title = img.get('alt') or img.get('title') or "Maillot FC Palestina"
                    
                    # Déterminer la catégorie
                    category = self.determine_category(title)
                    
                    # Créer l'objet maillot
                    jersey = {
                        'id': f"jersey-{len(jerseys) + 1}",
                        'title': title,
                        'description': f"Maillot officiel FC Palestina - {title}",
                        'category': category,
                        'year': self.extract_year(title),
                        'images': [src],
                        'thumbnail': src,
                        'price': None,
                        'availability': True,
                        'tags': [category, 'FC Palestina'],
                        'created_at': datetime.now().isoformat(),
                        'updated_at': datetime.now().isoformat()
                    }
                    
                    jerseys.append(jersey)
            
            logger.info(f"✅ {len(jerseys)} maillots extraits de cet album")
            return jerseys
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction de l'album: {e}")
            return []
    
    def determine_category(self, title: str) -> str:
        """Déterminer la catégorie d'un maillot"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['home', 'domicile', 'maison']):
            return 'home'
        elif any(word in title_lower for word in ['away', 'extérieur', 'extérieur']):
            return 'away'
        elif any(word in title_lower for word in ['keeper', 'gardien', 'goalkeeper']):
            return 'keeper'
        elif any(word in title_lower for word in ['special', 'spécial', 'limited', 'limitée']):
            return 'special'
        elif any(word in title_lower for word in ['vintage', 'retro', 'classic']):
            return 'vintage'
        else:
            return 'home'  # Par défaut
    
    def extract_year(self, title: str) -> str:
        """Extraire l'année du titre"""
        year_match = re.search(r'\b(20\d{2})\b', title)
        if year_match:
            return year_match.group(1)
        return '2024'  # Par défaut
    
    def download_image(self, image_url: str, filename: str) -> bool:
        """Télécharger une image"""
        try:
            response = self.session.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Créer le dossier s'il n'existe pas
            os.makedirs('assets/images/jerseys', exist_ok=True)
            
            # Sauvegarder l'image
            filepath = os.path.join('assets/images/jerseys', filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"✅ Image téléchargée: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur téléchargement {filename}: {e}")
            return False
    
    def scrape_all_jerseys(self) -> list:
        """Scraper tous les maillots"""
        try:
            logger.info("🚀 Démarrage du scraping complet...")
            
            # Tester la connexion
            if not self.test_connection():
                return []
            
            # Récupérer tous les albums
            albums = self.get_all_albums()
            if not albums:
                return []
            
            all_jerseys = []
            
            # Traiter chaque album
            for i, album in enumerate(albums, 1):
                logger.info(f"📸 Traitement album {i}/{len(albums)}: {album['title']}")
                
                jerseys = self.extract_album_data(album['url'])
                if jerseys:
                    all_jerseys.extend(jerseys)
                    logger.info(f"   ✅ {len(jerseys)} maillots extraits")
                
                # Pause entre les albums
                time.sleep(2)
            
            logger.info(f"🎉 Total: {len(all_jerseys)} maillots extraits !")
            return all_jerseys
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du scraping: {e}")
            return []

def main():
    """Fonction principale pour tester le scraper"""
    scraper = SimpleYupooScraper()
    
    print("🧪 Test du scraper Yupoo simplifié")
    print("=" * 40)
    
    # Test de connexion
    if scraper.test_connection():
        print("✅ Connexion réussie !")
        
        # Test de récupération des albums
        albums = scraper.get_all_albums()
        if albums:
            print(f"✅ {len(albums)} albums trouvés")
            
            # Test d'extraction d'un album
            if albums:
                first_album = albums[0]
                print(f"📸 Test d'extraction: {first_album['title']}")
                
                jerseys = scraper.extract_album_data(first_album['url'])
                if jerseys:
                    print(f"✅ {len(jerseys)} maillots extraits")
                    print("🎉 Le scraper fonctionne !")
                else:
                    print("⚠️ Aucun maillot extrait")
        else:
            print("❌ Aucun album trouvé")
    else:
        print("❌ Connexion échouée")

if __name__ == "__main__":
    main()
