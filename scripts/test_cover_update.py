#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script TEST pour mettre à jour uniquement les 5 premiers thumbnails
"""

import json
import logging
import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_cover_update.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CoverImageUpdater:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.images_dir = Path('assets/images/jerseys')
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_cover_image(self, soup, album_url: str) -> str:
        """Extrait l'image de couverture/présentation Yupoo (celle en haut à côté du titre)"""
        # Le sélecteur correct basé sur l'analyse de la structure HTML Yupoo
        cover_selectors = [
            '.showalbumheader__gallerycover img',  # Sélecteur principal trouvé
            '.showalbumheader__gallerycover .autocover',
            '.album__cover img',
            '.showalbum__cover img',
            '.album-cover img'
        ]
        
        for selector in cover_selectors:
            img_elem = soup.select_one(selector)
            if img_elem:
                img_url = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-original')
                if img_url and 'photo' in img_url.lower():
                    # Normaliser l'URL (ajouter https: si manquant)
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    else:
                        from urllib.parse import urljoin
                        img_url = urljoin(album_url, img_url)
                    
                    # Garder medium (bonne qualité accessible), améliorer small/square vers medium
                    img_url = img_url.replace('/small.jpg', '/medium.jpg').replace('/square.jpg', '/medium.jpg')
                    
                    logger.info(f"Image de couverture trouvee avec selecteur: {selector}")
                    logger.info(f"   URL: {img_url}")
                    return img_url
        
        logger.warning(f"Aucune image de couverture trouvee pour {album_url}")
        return None
    
    def download_image(self, image_url: str, jersey_id: str, suffix: str = 'cover') -> str:
        """Télécharge une image de couverture"""
        try:
            filename = f"{jersey_id}_{suffix}.jpg"
            filepath = self.images_dir / filename
            
            # Si le fichier existe déjà, ne pas re-télécharger
            if filepath.exists():
                logger.info(f"Image de couverture deja existante: {filename}")
                return filename
            
            # Headers spéciaux pour Yupoo (anti-hotlinking)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://shixingtiyu.x.yupoo.com/',
                'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Sec-Fetch-Dest': 'image',
                'Sec-Fetch-Mode': 'no-cors',
                'Sec-Fetch-Site': 'same-site'
            }
            
            response = self.session.get(image_url, headers=headers, timeout=20)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Image de couverture telechargee: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Erreur telechargement image: {e}")
            return None
    
    def test_first_jerseys(self, count: int = 5):
        """Teste sur les N premiers maillots"""
        jerseys_path = 'data/jerseys.json'
        
        with open(jerseys_path, 'r', encoding='utf-8') as f:
            jerseys = json.load(f)
        
        logger.info(f"\n=== TEST SUR {count} PREMIERS MAILLOTS ===\n")
        
        for i, jersey in enumerate(jerseys[:count], 1):
            jersey_id = jersey.get('id')
            source_url = jersey.get('source_url')
            current_thumbnail = jersey.get('thumbnail')
            
            logger.info(f"\n[{i}/{count}] {jersey.get('title')}")
            logger.info(f"  Thumbnail actuel: {current_thumbnail}")
            logger.info(f"  URL: {source_url}")
            
            if not source_url:
                logger.warning("  Pas d'URL source, skip")
                continue
            
            try:
                # Récupérer la page Yupoo
                response = self.session.get(source_url, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extraire l'image de couverture
                cover_url = self.extract_cover_image(soup, source_url)
                
                if cover_url:
                    # Télécharger l'image de couverture
                    cover_filename = self.download_image(cover_url, jersey_id, 'cover')
                    
                    if cover_filename:
                        logger.info(f"  SUCCESS! Nouveau thumbnail: {cover_filename}")
                        jersey['thumbnail'] = cover_filename
                    else:
                        logger.warning(f"  Echec download")
                else:
                    logger.warning(f"  Pas de cover trouvee")
                
                time.sleep(1.5)
                
            except Exception as e:
                logger.error(f"  Erreur: {e}")
        
        # Sauvegarder
        test_output = jerseys_path.replace('.json', '_test_covers.json')
        with open(test_output, 'w', encoding='utf-8') as f:
            json.dump(jerseys, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\n=== TEST TERMINE ===")
        logger.info(f"Resultat sauvegarde dans: {test_output}")

if __name__ == '__main__':
    updater = CoverImageUpdater()
    updater.test_first_jerseys(5)
