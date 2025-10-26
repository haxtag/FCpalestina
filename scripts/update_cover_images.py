#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour mettre à jour les thumbnails avec les images de couverture Yupoo
SANS re-scraper tous les albums (juste extraire les covers existantes)
"""

import json
import logging
import requests
from bs4 import BeautifulSoup
import time
import os
import hashlib
from urllib.parse import urlparse, urljoin
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update_cover_images.log'),
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
    
    def update_jerseys(self, jerseys_path: str = 'data/jerseys.json'):
        """Met à jour les thumbnails avec les images de couverture"""
        try:
            # Charger jerseys.json
            with open(jerseys_path, 'r', encoding='utf-8') as f:
                jerseys = json.load(f)
            
            logger.info(f"Charge {len(jerseys)} maillots depuis {jerseys_path}")
            
            updated_count = 0
            skipped_count = 0
            failed_count = 0
            
            for i, jersey in enumerate(jerseys, 1):
                jersey_id = jersey.get('id')
                source_url = jersey.get('source_url')
                current_thumbnail = jersey.get('thumbnail')
                
                if not source_url:
                    logger.warning(f"[{i}/{len(jerseys)}] Pas d'URL source pour: {jersey.get('title')}")
                    skipped_count += 1
                    continue
                
                # Vérifier si le thumbnail est déjà une image de couverture
                if current_thumbnail and '_cover.' in current_thumbnail:
                    logger.info(f"[{i}/{len(jerseys)}] Thumbnail deja une couverture: {jersey.get('title')}")
                    skipped_count += 1
                    continue
                
                logger.info(f"\n[{i}/{len(jerseys)}] Traitement: {jersey.get('title')}")
                logger.info(f"  URL: {source_url}")
                
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
                        
                        if cover_filename and cover_filename != "placeholder.jpg":
                            # Mettre à jour le thumbnail
                            old_thumbnail = jersey.get('thumbnail')
                            jersey['thumbnail'] = cover_filename
                            logger.info(f"  Thumbnail mis a jour: {old_thumbnail} -> {cover_filename}")
                            updated_count += 1
                        else:
                            logger.warning(f"  Echec telechargement, garde thumbnail actuel: {current_thumbnail}")
                            failed_count += 1
                    else:
                        logger.warning(f"  Pas de couverture trouvee, garde thumbnail actuel: {current_thumbnail}")
                        skipped_count += 1
                    
                    # Pause pour ne pas surcharger Yupoo
                    time.sleep(1.5)
                    
                except Exception as e:
                    logger.error(f"  Erreur traitement {jersey.get('title')}: {e}")
                    failed_count += 1
                    continue
            
            # Sauvegarder le fichier mis à jour
            backup_path = jerseys_path.replace('.json', '_backup_before_covers.json')
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(jerseys, f, ensure_ascii=False, indent=2)
            logger.info(f"\nBackup sauvegarde: {backup_path}")
            
            with open(jerseys_path, 'w', encoding='utf-8') as f:
                json.dump(jerseys, f, ensure_ascii=False, indent=2)
            
            logger.info(f"\nTERMINE!")
            logger.info(f"  • Mis a jour: {updated_count}")
            logger.info(f"  • Ignores (deja OK ou pas de couverture): {skipped_count}")
            logger.info(f"  • Echecs: {failed_count}")
            logger.info(f"  • Total traite: {len(jerseys)}")
            
        except Exception as e:
            logger.error(f"Erreur fatale: {e}")
            raise

def main():
    updater = CoverImageUpdater()
    updater.update_jerseys()

if __name__ == '__main__':
    main()
