#!/usr/bin/env python3
"""
Scraper spécialisé pour télécharger les vraies images depuis Yupoo
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
import hashlib

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('image_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ImageScraper:
    """Scraper spécialisé pour télécharger les images depuis Yupoo"""
    
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
        
        # Créer le dossier des images
        os.makedirs('assets/images/jerseys', exist_ok=True)
    
    def download_image(self, image_url: str, filename: str) -> bool:
        """Télécharge une image depuis une URL"""
        try:
            # Nettoyer l'URL
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            elif image_url.startswith('/'):
                image_url = self.base_url + image_url
            
            logger.info(f"Téléchargement: {image_url}")
            
            response = self.session.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Vérifier que c'est bien une image
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                logger.warning(f"URL ne pointe pas vers une image: {content_type}")
                return False
            
            # Sauvegarder l'image
            filepath = os.path.join('assets/images/jerseys', filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Image téléchargée: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur téléchargement {filename}: {e}")
            return False
    
    def extract_images_from_album(self, album_url: str) -> list:
        """Extrait les URLs des images d'un album Yupoo"""
        try:
            logger.info(f"Extraction des images de: {album_url}")
            
            response = self.session.get(album_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            image_urls = []
            
            # Méthode 1: Chercher les images dans les conteneurs d'albums
            album_containers = soup.find_all(['div', 'section'], class_=re.compile(r'album|gallery|photo'))
            
            for container in album_containers:
                images = container.find_all('img')
                for img in images:
                    src = img.get('src') or img.get('data-src') or img.get('data-original')
                    if src and self.is_valid_image_url(src):
                        image_urls.append(src)
            
            # Méthode 2: Chercher toutes les images de la page
            if not image_urls:
                all_images = soup.find_all('img')
                for img in all_images:
                    src = img.get('src') or img.get('data-src') or img.get('data-original')
                    if src and self.is_valid_image_url(src):
                        image_urls.append(src)
            
            # Supprimer les doublons
            image_urls = list(set(image_urls))
            
            logger.info(f"Trouvé {len(image_urls)} images dans l'album")
            return image_urls
            
        except Exception as e:
            logger.error(f"Erreur extraction images: {e}")
            return []
    
    def is_valid_image_url(self, url: str) -> bool:
        """Vérifie si l'URL pointe vers une image valide"""
        if not url:
            return False
        
        # Exclure les images de navigation, logos, etc.
        exclude_patterns = [
            'logo', 'icon', 'avatar', 'profile', 'nav', 'menu', 'button',
            'banner', 'header', 'footer', 'social', 'share', 'loading'
        ]
        
        url_lower = url.lower()
        for pattern in exclude_patterns:
            if pattern in url_lower:
                return False
        
        # Inclure les images de maillots
        include_patterns = [
            'jersey', 'maillot', 'shirt', 'kit', 'uniform', 'sport',
            'football', 'soccer', 'team', 'club', 'player'
        ]
        
        for pattern in include_patterns:
            if pattern in url_lower:
                return True
        
        # Si l'image est dans un dossier d'album, l'inclure
        if '/albums/' in url or '/photos/' in url:
            return True
        
        return False
    
    def update_jerseys_with_images(self):
        """Met à jour les maillots avec les vraies images"""
        try:
            # Lire le fichier jerseys.json
            with open('data/jerseys.json', 'r', encoding='utf-8') as f:
                jerseys = json.load(f)
            
            logger.info(f"Traitement de {len(jerseys)} maillots...")
            
            for i, jersey in enumerate(jerseys, 1):
                logger.info(f"Traitement maillot {i}/{len(jerseys)}: {jersey['title']}")
                
                # Récupérer l'URL source de l'album
                source_url = jersey.get('source_url')
                if not source_url:
                    logger.warning(f"Pas d'URL source pour {jersey['title']}")
                    continue
                
                # Extraire les images de l'album
                image_urls = self.extract_images_from_album(source_url)
                
                if image_urls:
                    # Télécharger la première image comme image principale
                    main_image_url = image_urls[0]
                    main_filename = f"jersey-{jersey['id']}-main.jpg"
                    
                    if self.download_image(main_image_url, main_filename):
                        # Mettre à jour les URLs d'images
                        jersey['images'] = [main_filename]
                        jersey['thumbnail'] = main_filename
                        
                        # Télécharger les autres images (max 5)
                        additional_images = []
                        for j, img_url in enumerate(image_urls[1:6], 1):
                            filename = f"jersey-{jersey['id']}-{j}.jpg"
                            if self.download_image(img_url, filename):
                                additional_images.append(filename)
                        
                        if additional_images:
                            jersey['images'].extend(additional_images)
                        
                        logger.info(f"  {len(jersey['images'])} images téléchargées")
                    else:
                        logger.warning(f"  Échec téléchargement image principale")
                else:
                    logger.warning(f"  Aucune image trouvée dans l'album")
                
                # Pause entre les maillots
                time.sleep(2)
            
            # Sauvegarder les modifications
            with open('data/jerseys.json', 'w', encoding='utf-8') as f:
                json.dump(jerseys, f, ensure_ascii=False, indent=2)
            
            logger.info("Mise à jour terminée !")
            return True
            
        except Exception as e:
            logger.error(f"Erreur mise à jour: {e}")
            return False

def main():
    """Fonction principale"""
    scraper = ImageScraper()
    
    print("Téléchargement des vraies images depuis Yupoo")
    print("=" * 50)
    
    success = scraper.update_jerseys_with_images()
    
    if success:
        print("✅ Images téléchargées avec succès !")
    else:
        print("❌ Échec du téléchargement des images")

if __name__ == "__main__":
    main()
