#!/usr/bin/env python3
"""
Scraper intelligent pour Yupoo - FC Palestina
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

class SmartYupooScraper:
    """Scraper intelligent pour Yupoo"""
    
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
            logger.info("Connexion réussie !")
            return True
        except Exception as e:
            logger.error(f"Erreur de connexion: {e}")
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
            
            logger.info(f"{len(albums)} albums trouvés")
            return albums
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des albums: {e}")
            return []
    
    def extract_album_data(self, album_url: str) -> list:
        """Extraire les données d'un album avec méthode intelligente"""
        try:
            logger.info(f"Extraction de l'album: {album_url}")
            response = self.session.get(album_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            jerseys = []
            
            # Méthode 1: Chercher les images dans les conteneurs d'albums
            album_containers = soup.find_all(['div', 'section'], class_=re.compile(r'album|gallery|photo'))
            
            for container in album_containers:
                images = container.find_all('img')
                for img in images:
                    src = img.get('src') or img.get('data-src') or img.get('data-original')
                    if src and self.is_valid_image(src):
                        title = img.get('alt') or img.get('title') or "Maillot FC Palestina"
                        
                        jersey = self.create_jersey_from_image(src, title, album_url)
                        if jersey:
                            jerseys.append(jersey)
            
            # Méthode 2: Chercher toutes les images de la page
            if not jerseys:
                all_images = soup.find_all('img')
                for img in all_images:
                    src = img.get('src') or img.get('data-src') or img.get('data-original')
                    if src and self.is_valid_image(src):
                        title = img.get('alt') or img.get('title') or "Maillot FC Palestina"
                        
                        jersey = self.create_jersey_from_image(src, title, album_url)
                        if jersey:
                            jerseys.append(jersey)
            
            # Méthode 3: Créer un maillot basé sur le titre de l'album
            if not jerseys:
                album_title = soup.find('title')
                if album_title:
                    title_text = album_title.get_text(strip=True)
                    jersey = self.create_jersey_from_album_title(title_text, album_url)
                    if jersey:
                        jerseys.append(jersey)
            
            logger.info(f"{len(jerseys)} maillots extraits de cet album")
            return jerseys
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction de l'album: {e}")
            return []
    
    def is_valid_image(self, src: str) -> bool:
        """Vérifier si l'image est valide"""
        if not src:
            return False
        
        # Exclure les images de navigation, logos, etc.
        exclude_patterns = [
            'logo', 'icon', 'avatar', 'profile', 'nav', 'menu', 'button',
            'banner', 'header', 'footer', 'social', 'share', 'loading'
        ]
        
        src_lower = src.lower()
        for pattern in exclude_patterns:
            if pattern in src_lower:
                return False
        
        # Inclure les images de maillots
        include_patterns = [
            'jersey', 'maillot', 'shirt', 'kit', 'uniform', 'sport',
            'football', 'soccer', 'team', 'club', 'player'
        ]
        
        for pattern in include_patterns:
            if pattern in src_lower:
                return True
        
        # Si l'image est dans un dossier d'album, l'inclure
        if '/albums/' in src or '/photos/' in src:
            return True
        
        return False
    
    def create_jersey_from_image(self, image_url: str, title: str, album_url: str) -> dict:
        """Créer un objet maillot à partir d'une image"""
        try:
            # Nettoyer le titre
            clean_title = self.clean_title(title)
            
            # Déterminer la catégorie
            category = self.determine_category(clean_title)
            
            # Extraire l'année
            year = self.extract_year(clean_title)
            
            # Créer l'objet maillot
            jersey = {
                'id': f"jersey-{hash(image_url) % 100000}",
                'title': clean_title,
                'description': f"Maillot officiel FC Palestina - {clean_title}",
                'category': category,
                'year': year,
                'images': [image_url],
                'thumbnail': image_url,
                'price': None,
                'availability': True,
                'tags': [category, 'FC Palestina'],
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'source_url': album_url
            }
            
            return jersey
            
        except Exception as e:
            logger.error(f"Erreur création maillot: {e}")
            return None
    
    def create_jersey_from_album_title(self, album_title: str, album_url: str) -> dict:
        """Créer un maillot à partir du titre de l'album"""
        try:
            # Nettoyer le titre
            clean_title = self.clean_title(album_title)
            
            # Déterminer la catégorie
            category = self.determine_category(clean_title)
            
            # Extraire l'année
            year = self.extract_year(clean_title)
            
            # Créer une image placeholder
            placeholder_image = f"https://via.placeholder.com/400x400/2c5530/ffffff?text={clean_title[:20]}"
            
            # Créer l'objet maillot
            jersey = {
                'id': f"jersey-{hash(album_url) % 100000}",
                'title': clean_title,
                'description': f"Maillot officiel FC Palestina - {clean_title}",
                'category': category,
                'year': year,
                'images': [placeholder_image],
                'thumbnail': placeholder_image,
                'price': None,
                'availability': True,
                'tags': [category, 'FC Palestina'],
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'source_url': album_url
            }
            
            return jersey
            
        except Exception as e:
            logger.error(f"Erreur création maillot depuis album: {e}")
            return None
    
    def clean_title(self, title: str) -> str:
        """Nettoyer le titre"""
        if not title:
            return "Maillot FC Palestina"
        
        # Supprimer les caractères spéciaux
        clean = re.sub(r'[^\w\s\-]', ' ', title)
        
        # Supprimer les espaces multiples
        clean = re.sub(r'\s+', ' ', clean)
        
        # Limiter la longueur
        if len(clean) > 50:
            clean = clean[:47] + "..."
        
        return clean.strip() or "Maillot FC Palestina"
    
    def determine_category(self, title: str) -> str:
        """Déterminer la catégorie d'un maillot"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['home', 'domicile', 'maison', '主']):
            return 'home'
        elif any(word in title_lower for word in ['away', 'extérieur', 'extérieur', '客']):
            return 'away'
        elif any(word in title_lower for word in ['keeper', 'gardien', 'goalkeeper', '门将']):
            return 'keeper'
        elif any(word in title_lower for word in ['special', 'spécial', 'limited', 'limitée', '特别', '特别版']):
            return 'special'
        elif any(word in title_lower for word in ['vintage', 'retro', 'classic', '经典']):
            return 'vintage'
        else:
            return 'home'  # Par défaut
    
    def extract_year(self, title: str) -> str:
        """Extraire l'année du titre"""
        year_match = re.search(r'\b(20\d{2})\b', title)
        if year_match:
            return year_match.group(1)
        return '2024'  # Par défaut
    
    def scrape_all_jerseys(self) -> list:
        """Scraper tous les maillots"""
        try:
            logger.info("Démarrage du scraping complet...")
            
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
                logger.info(f"Traitement album {i}/{len(albums)}: {album['title']}")
                
                jerseys = self.extract_album_data(album['url'])
                if jerseys:
                    all_jerseys.extend(jerseys)
                    logger.info(f"   {len(jerseys)} maillots extraits")
                
                # Pause entre les albums
                time.sleep(1)
            
            logger.info(f"Total: {len(all_jerseys)} maillots extraits !")
            return all_jerseys
            
        except Exception as e:
            logger.error(f"Erreur lors du scraping: {e}")
            return []

def main():
    """Fonction principale pour tester le scraper"""
    scraper = SmartYupooScraper()
    
    print("Test du scraper Yupoo intelligent")
    print("=" * 40)
    
    # Test de connexion
    if scraper.test_connection():
        print("Connexion réussie !")
        
        # Test de récupération des albums
        albums = scraper.get_all_albums()
        if albums:
            print(f"{len(albums)} albums trouvés")
            
            # Test d'extraction d'un album
            if albums:
                first_album = albums[0]
                print(f"Test d'extraction: {first_album['title']}")
                
                jerseys = scraper.extract_album_data(first_album['url'])
                if jerseys:
                    print(f"{len(jerseys)} maillots extraits")
                    print("Le scraper fonctionne !")
                else:
                    print("Aucun maillot extrait")
        else:
            print("Aucun album trouvé")
    else:
        print("Connexion échouée")

if __name__ == "__main__":
    main()
