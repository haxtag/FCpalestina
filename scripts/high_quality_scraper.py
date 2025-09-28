#!/usr/bin/env python3
"""
Scraper pour télécharger des images de haute qualité depuis Yupoo
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
from urllib.parse import urljoin, urlparse
import logging
import random

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HighQualityYupooScraper:
    """Scraper pour images haute qualité"""
    
    def __init__(self, base_url: str = "https://shixingtiyu.x.yupoo.com"):
        self.base_url = base_url
        self.session = requests.Session()
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
        
        os.makedirs('assets/images/jerseys', exist_ok=True)
    
    def get_high_quality_images(self, album_url: str) -> list:
        """Récupère les images haute qualité d'un album"""
        try:
            logger.info(f"Récupération images HD de: {album_url}")
            
            response = self.session.get(album_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            images = []
            
            # Chercher les images dans différents conteneurs
            selectors = [
                'img[src*="photo.yupoo.com"]',
                'img[data-src*="photo.yupoo.com"]',
                'img[data-original*="photo.yupoo.com"]',
                '.photo img',
                '.album img',
                '.gallery img',
                '.item img'
            ]
            
            for selector in selectors:
                found_images = soup.select(selector)
                for img in found_images:
                    src = img.get('src') or img.get('data-src') or img.get('data-original')
                    if src and self.is_valid_image_url(src):
                        # Convertir en image haute qualité
                        hd_url = self.convert_to_hd_url(src)
                        if hd_url:
                            images.append(hd_url)
            
            # Supprimer les doublons
            images = list(set(images))
            logger.info(f"Trouvé {len(images)} images HD")
            return images
            
        except Exception as e:
            logger.error(f"Erreur récupération images HD: {e}")
            return []
    
    def convert_to_hd_url(self, url: str) -> str:
        """Convertit une URL d'image en version haute qualité"""
        try:
            # Remplacer les suffixes de taille par 'large' ou 'original'
            hd_url = url
            
            # Remplacer les tailles connues par 'large'
            size_replacements = [
                ('/small.jpg', '/large.jpg'),
                ('/medium.jpg', '/large.jpg'),
                ('/square.jpg', '/large.jpg'),
                ('/thumb.jpg', '/large.jpg'),
                ('/thumbnail.jpg', '/large.jpg')
            ]
            
            for old_size, new_size in size_replacements:
                if old_size in hd_url:
                    hd_url = hd_url.replace(old_size, new_size)
                    break
            
            # Si pas de suffixe de taille, essayer d'ajouter /large.jpg
            if not any(size in hd_url for size in ['/small', '/medium', '/square', '/thumb', '/large', '/original']):
                if hd_url.endswith('.jpg'):
                    hd_url = hd_url.replace('.jpg', '/large.jpg')
                elif hd_url.endswith('.jpeg'):
                    hd_url = hd_url.replace('.jpeg', '/large.jpg')
                elif hd_url.endswith('.png'):
                    hd_url = hd_url.replace('.png', '/large.jpg')
            
            return hd_url
            
        except Exception as e:
            logger.error(f"Erreur conversion HD: {e}")
            return url
    
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
        if 'yupoo' in url_lower or 'photo' in url_lower:
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
            
            logger.info(f"Téléchargement HD: {image_url}")
            
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
            
            # Vérifier la taille de l'image
            content_length = len(response.content)
            if content_length < 10000:  # Moins de 10KB = probablement une image de mauvaise qualité
                logger.warning(f"Image trop petite: {content_length} bytes")
                return False
            
            # Sauvegarder l'image
            filepath = os.path.join('assets/images/jerseys', filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Image HD téléchargée: {filename} ({content_length} bytes)")
            return True
            
        except Exception as e:
            logger.error(f"Erreur téléchargement {filename}: {e}")
            return False
    
    def update_jerseys_with_hd_images(self):
        """Met à jour les maillots avec des images haute qualité"""
        try:
            # Lire le fichier jerseys.json
            with open('data/jerseys.json', 'r', encoding='utf-8') as f:
                jerseys = json.load(f)
            
            logger.info(f"Traitement de {len(jerseys)} maillots pour images HD...")
            
            for i, jersey in enumerate(jerseys, 1):
                logger.info(f"Traitement maillot {i}/{len(jerseys)}: {jersey['title']}")
                
                # Récupérer l'URL source de l'album
                source_url = jersey.get('source_url')
                if not source_url:
                    logger.warning(f"Pas d'URL source pour {jersey['title']}")
                    continue
                
                # Récupérer les images HD de l'album
                hd_image_urls = self.get_high_quality_images(source_url)
                
                if hd_image_urls:
                    # Télécharger les images HD
                    hd_images = []
                    for j, img_url in enumerate(hd_image_urls[:6]):  # Max 6 images
                        filename = f"jersey-{jersey['id']}-hd-{j}.jpg"
                        if self.download_image(img_url, filename):
                            hd_images.append(filename)
                    
                    if hd_images:
                        # Mettre à jour les URLs d'images
                        jersey['images'] = hd_images
                        jersey['thumbnail'] = hd_images[0]
                        logger.info(f"  {len(hd_images)} images HD téléchargées")
                    else:
                        logger.warning(f"  Aucune image HD téléchargée")
                else:
                    logger.warning(f"  Aucune image HD trouvée dans l'album")
                
                # Pause entre les maillots
                time.sleep(2)
            
            # Sauvegarder les modifications
            with open('data/jerseys.json', 'w', encoding='utf-8') as f:
                json.dump(jerseys, f, ensure_ascii=False, indent=2)
            
            logger.info("Mise à jour HD terminée !")
            return True
            
        except Exception as e:
            logger.error(f"Erreur mise à jour HD: {e}")
            return False

def main():
    """Fonction principale"""
    scraper = HighQualityYupooScraper()
    
    print("Téléchargement des images haute qualité depuis Yupoo")
    print("=" * 60)
    
    success = scraper.update_jerseys_with_hd_images()
    
    if success:
        print("✅ Images HD téléchargées avec succès !")
    else:
        print("❌ Échec du téléchargement des images HD")

if __name__ == "__main__":
    main()
