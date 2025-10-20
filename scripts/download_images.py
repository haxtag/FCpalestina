#!/usr/bin/env python3
"""
Script pour télécharger les images manquantes depuis les URLs dans jerseys.json
Utilisé temporairement pour les démos Render
"""

import json
import os
import requests
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def download_missing_images():
    """Télécharge uniquement les images qui manquent"""
    # Chemins
    base_dir = Path(__file__).parent.parent
    jerseys_file = base_dir / 'data' / 'jerseys.json'
    images_dir = base_dir / 'assets' / 'images' / 'jerseys'
    
    # Créer le dossier images si nécessaire
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Charger les maillots
    with open(jerseys_file, 'r', encoding='utf-8') as f:
        jerseys = json.load(f)
    
    downloaded = 0
    skipped = 0
    errors = 0
    
    logger.info(f"Vérification de {len(jerseys)} maillots...")
    
    for jersey in jerseys:
        image_url = jersey.get('image_url')
        image_path = jersey.get('image')
        
        if not image_url or not image_path:
            continue
        
        # Chemin complet de l'image locale
        local_image = base_dir / image_path.lstrip('/')
        
        # Si l'image existe déjà, on skip
        if local_image.exists():
            skipped += 1
            continue
        
        # Télécharger l'image
        try:
            logger.info(f"Téléchargement: {local_image.name}")
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            with open(local_image, 'wb') as f:
                f.write(response.content)
            
            downloaded += 1
            
        except Exception as e:
            logger.error(f"Erreur pour {local_image.name}: {e}")
            errors += 1
    
    logger.info(f"Terminé: {downloaded} téléchargées, {skipped} existantes, {errors} erreurs")
    return {"downloaded": downloaded, "skipped": skipped, "errors": errors}

if __name__ == '__main__':
    download_missing_images()
