#!/usr/bin/env python3
"""
Scraper avancé pour Yupoo avec support JavaScript
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
import random
import hashlib

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('advanced_yupoo_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedYupooScraper:
    """Scraper avancé pour Yupoo avec support JavaScript"""
    
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
            'Cache-Control': 'max-age=0',
            'Referer': base_url
        })
        
        # Créer le dossier des images
        os.makedirs('assets/images/jerseys', exist_ok=True)
    
    def get_album_images(self, album_url: str) -> list:
        """Récupère les images d'un album Yupoo"""
        try:
            logger.info(f"Récupération des images de: {album_url}")
            
            # Essayer plusieurs méthodes pour récupérer les images
            
            # Méthode 1: Page principale de l'album
            images = self.extract_images_from_page(album_url)
            if images:
                logger.info(f"Méthode 1: {len(images)} images trouvées")
                return images
            
            # Méthode 2: API JSON de Yupoo
            images = self.extract_images_from_api(album_url)
            if images:
                logger.info(f"Méthode 2: {len(images)} images trouvées")
                return images
            
            # Méthode 3: Analyse des scripts JavaScript
            images = self.extract_images_from_scripts(album_url)
            if images:
                logger.info(f"Méthode 3: {len(images)} images trouvées")
                return images
            
            logger.warning("Aucune image trouvée avec toutes les méthodes")
            return []
            
        except Exception as e:
            logger.error(f"Erreur récupération images: {e}")
            return []
    
    def extract_images_from_page(self, album_url: str) -> list:
        """Extrait les images depuis la page HTML"""
        try:
            response = self.session.get(album_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            images = []
            
            # Chercher les images dans différents conteneurs
            selectors = [
                'img[src*="yupoo"]',
                'img[data-src*="yupoo"]',
                'img[data-original*="yupoo"]',
                '.photo img',
                '.album img',
                '.gallery img',
                '.item img',
                'img[src*="photo"]',
                'img[src*="image"]'
            ]
            
            for selector in selectors:
                found_images = soup.select(selector)
                for img in found_images:
                    src = img.get('src') or img.get('data-src') or img.get('data-original')
                    if src and self.is_valid_image_url(src):
                        images.append(src)
            
            # Supprimer les doublons
            images = list(set(images))
            return images
            
        except Exception as e:
            logger.error(f"Erreur extraction page: {e}")
            return []
    
    def extract_images_from_api(self, album_url: str) -> list:
        """Extrait les images depuis l'API JSON de Yupoo"""
        try:
            # Extraire l'ID de l'album depuis l'URL
            album_id = self.extract_album_id(album_url)
            if not album_id:
                return []
            
            # Construire l'URL de l'API
            api_url = f"{self.base_url}/albums/{album_id}/photos"
            
            # Headers pour l'API
            api_headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'application/json, text/plain, */*',
                'Referer': album_url,
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            response = self.session.get(api_url, headers=api_headers, timeout=30)
            if response.status_code == 200:
                try:
                    data = response.json()
                    images = []
                    
                    # Extraire les URLs d'images du JSON
                    if isinstance(data, dict):
                        photos = data.get('photos', [])
                        for photo in photos:
                            if isinstance(photo, dict):
                                img_url = photo.get('url') or photo.get('src') or photo.get('image')
                                if img_url:
                                    images.append(img_url)
                    
                    return images
                except json.JSONDecodeError:
                    pass
            
            return []
            
        except Exception as e:
            logger.error(f"Erreur extraction API: {e}")
            return []
    
    def extract_images_from_scripts(self, album_url: str) -> list:
        """Extrait les images depuis les scripts JavaScript"""
        try:
            response = self.session.get(album_url, timeout=30)
            response.raise_for_status()
            
            # Chercher les scripts qui contiennent des URLs d'images
            scripts = re.findall(r'<script[^>]*>(.*?)</script>', response.text, re.DOTALL)
            images = []
            
            for script in scripts:
                # Chercher les URLs d'images dans le JavaScript
                img_patterns = [
                    r'"(https?://[^"]*\.(?:jpg|jpeg|png|gif|webp)[^"]*)"',
                    r"'(https?://[^']*\.(?:jpg|jpeg|png|gif|webp)[^']*)'",
                    r'url\(["\']?(https?://[^"\']*\.(?:jpg|jpeg|png|gif|webp)[^"\']*)["\']?\)',
                    r'src:\s*["\'](https?://[^"\']*\.(?:jpg|jpeg|png|gif|webp)[^"\']*)["\']'
                ]
                
                for pattern in img_patterns:
                    matches = re.findall(pattern, script, re.IGNORECASE)
                    for match in matches:
                        if self.is_valid_image_url(match):
                            images.append(match)
            
            # Supprimer les doublons
            images = list(set(images))
            return images
            
        except Exception as e:
            logger.error(f"Erreur extraction scripts: {e}")
            return []
    
    def extract_album_id(self, album_url: str) -> str:
        """Extrait l'ID de l'album depuis l'URL"""
        try:
            # Pattern pour extraire l'ID de l'album
            patterns = [
                r'/albums/(\d+)',
                r'album_id=(\d+)',
                r'id=(\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, album_url)
                if match:
                    return match.group(1)
            
            return None
            
        except Exception as e:
            logger.error(f"Erreur extraction ID: {e}")
            return None
    
    def is_valid_image_url(self, url: str) -> bool:
        """Vérifie si l'URL pointe vers une image valide"""
        if not url:
            return False
        
        # Exclure les images de navigation, logos, etc.
        exclude_patterns = [
            'logo', 'icon', 'avatar', 'profile', 'nav', 'menu', 'button',
            'banner', 'header', 'footer', 'social', 'share', 'loading',
            'placeholder', 'default', 'empty'
        ]
        
        url_lower = url.lower()
        for pattern in exclude_patterns:
            if pattern in url_lower:
                return False
        
        # Vérifier l'extension
        if not any(url_lower.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            return False
        
        # Inclure les images de Yupoo
        if 'yupoo' in url_lower or 'photo' in url_lower or 'image' in url_lower:
            return True
        
        return False
    
    def download_image(self, image_url: str, filename: str) -> bool:
        """Télécharge une image depuis une URL"""
        try:
            # Nettoyer l'URL
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            elif image_url.startswith('/'):
                image_url = self.base_url + image_url
            
            logger.info(f"Téléchargement: {image_url}")
            
            # Headers pour le téléchargement d'image
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Referer': self.base_url,
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
            }
            
            response = self.session.get(image_url, headers=headers, timeout=30)
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
    
    def update_jerseys_with_real_images(self):
        """Met à jour les maillots avec les vraies images de Yupoo"""
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
                
                # Récupérer les images de l'album
                image_urls = self.get_album_images(source_url)
                
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
                time.sleep(3)
            
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
    scraper = AdvancedYupooScraper()
    
    print("Téléchargement des vraies images depuis Yupoo (version avancée)")
    print("=" * 60)
    
    success = scraper.update_jerseys_with_real_images()
    
    if success:
        print("✅ Images téléchargées avec succès !")
    else:
        print("❌ Échec du téléchargement des images")

if __name__ == "__main__":
    main()
