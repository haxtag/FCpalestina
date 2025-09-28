#!/usr/bin/env python3
"""
SCRAPER MASSIF FC PALESTINA - Import complet depuis Yupoo
Optimisé pour importer plus de 100 maillots avec pagination
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
from datetime import datetime
import logging
import random
import hashlib
from urllib.parse import urljoin, urlparse, parse_qs
import concurrent.futures
from threading import Lock

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mass_import.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MassYupooImporter:
    """Importateur massif pour Yupoo optimisé pour FC Palestina"""
    
    def __init__(self):
        self.base_url = "https://shixingtiyu.x.yupoo.com"
        self.session = requests.Session()
        self.data_lock = Lock()
        self.imported_count = 0
        self.failed_count = 0
        
        # Configuration des répertoires
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.data_dir = os.path.join(self.project_root, 'data')
        self.images_dir = os.path.join(self.project_root, 'assets', 'images', 'jerseys')
        self.thumbnails_dir = os.path.join(self.project_root, 'assets', 'images', 'thumbnails')
        
        # Créer les répertoires si nécessaires
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.thumbnails_dir, exist_ok=True)
        
        # Headers
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,fr;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })
        
        # Catégories prédéfinies FC Palestina
        self.categories_mapping = {
            'home': {'name': 'Domicile', 'description': 'Maillots domicile'},
            'away': {'name': 'Extérieur', 'description': 'Maillots extérieur'},
            'third': {'name': 'Troisième', 'description': 'Troisièmes maillots'},
            'keeper': {'name': 'Gardien', 'description': 'Maillots de gardien'},
            'special': {'name': 'Spéciaux', 'description': 'Éditions spéciales'},
            'vintage': {'name': 'Vintage', 'description': 'Maillots vintage'},
            'training': {'name': 'Entraînement', 'description': 'Maillots d\'entraînement'}
        }
        
        # Tags prédéfinies
        self.available_tags = [
            {'id': 'fcpalestina', 'name': 'FC Palestina', 'color': '#8B1538'},
            {'id': 'new', 'name': 'Nouveau', 'color': '#28a745'},
            {'id': 'limited', 'name': 'Édition limitée', 'color': '#dc3545'},
            {'id': 'popular', 'name': 'Populaire', 'color': '#007bff'},
            {'id': 'classic', 'name': 'Classique', 'color': '#6f42c1'}
        ]

    def get_album_list(self, start_page=1, max_pages=20):
        """Récupère la liste des albums depuis Yupoo"""
        albums = []
        
        try:
            for page in range(start_page, start_page + max_pages):
                logger.info(f"📄 Récupération page {page}...")
                
                page_url = f"{self.base_url}/albums?tab=galley&page={page}"
                response = self.session.get(page_url, timeout=30)
                
                if response.status_code != 200:
                    logger.warning(f"⚠️ Erreur page {page}: HTTP {response.status_code}")
                    continue
                    
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Chercher les liens d'albums
                album_links = soup.find_all('a', href=re.compile(r'/albums/\d+'))
                
                if not album_links:
                    logger.info(f"🔚 Plus d'albums trouvés à la page {page}")
                    break
                
                for link in album_links:
                    album_url = urljoin(self.base_url, link.get('href'))
                    album_title = link.get('title', '').strip()
                    
                    if album_url not in [a['url'] for a in albums]:
                        albums.append({
                            'url': album_url,
                            'title': album_title,
                            'page': page
                        })
                
                logger.info(f"✅ Page {page}: {len(album_links)} albums trouvés")
                time.sleep(random.uniform(1, 3))  # Anti-détection
                
        except Exception as e:
            logger.error(f"❌ Erreur récupération albums: {e}")
        
        logger.info(f"🎯 Total: {len(albums)} albums récupérés")
        return albums

    def extract_jersey_data(self, album_url, album_title=""):
        """Extrait les données d'un maillot depuis un album"""
        try:
            logger.info(f"🔍 Extraction: {album_url}")
            
            response = self.session.get(album_url, timeout=30)
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraire les images
            images = self.extract_images(soup)
            if not images:
                logger.warning(f"⚠️ Aucune image trouvée: {album_url}")
                return None
            
            # Générer un ID unique
            jersey_id = f"jersey-{random.randint(10000, 99999)}"
            
            # Déterminer la catégorie en fonction du titre
            category = self.determine_category(album_title)
            
            # Générer des tags
            tags = self.generate_tags(album_title)
            
            # Créer l'objet jersey
            jersey_data = {
                "id": jersey_id,
                "title": album_title or "Maillot FC Palestina",
                "name": album_title or "Maillot FC Palestina", 
                "description": f"Maillot officiel FC Palestina - {album_title}",
                "category": category,
                "categories": [category],
                "year": "2024",
                "images": [],
                "thumbnail": "",
                "price": None,
                "size": "M-XL",
                "availability": True,
                "tags": tags,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "source_url": album_url
            }
            
            # Télécharger et traiter les images
            downloaded_images = self.download_images(images[:5], jersey_id)  # Max 5 images
            if downloaded_images:
                jersey_data["images"] = downloaded_images
                jersey_data["thumbnail"] = downloaded_images[0]
                
                return jersey_data
            else:
                logger.warning(f"⚠️ Échec téléchargement images: {album_url}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erreur extraction {album_url}: {e}")
            return None

    def extract_images(self, soup):
        """Extrait les URLs des images depuis la page"""
        images = []
        
        # Sélecteurs pour trouver les images
        selectors = [
            'img[src*="photo"]',
            'img[data-src*="photo"]',
            'img[src*="image"]',
            '.photo img',
            '.album img',
            '.gallery img'
        ]
        
        for selector in selectors:
            found_images = soup.select(selector)
            for img in found_images:
                src = img.get('src') or img.get('data-src') or img.get('data-original')
                if src and self.is_valid_image_url(src):
                    # Convertir en haute qualité si possible
                    if '!c' in src:
                        src = src.split('!c')[0]  # Supprimer les paramètres de compression
                    images.append(src)
        
        # Supprimer les doublons et limiter
        images = list(set(images))
        return images[:5]  # Max 5 images par maillot

    def is_valid_image_url(self, url):
        """Vérifie si l'URL est une image valide"""
        if not url:
            return False
        return any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp'])

    def determine_category(self, title):
        """Détermine la catégorie en fonction du titre"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['home', 'domicile', 'dom']):
            return 'home'
        elif any(word in title_lower for word in ['away', 'extérieur', 'ext']):
            return 'away'  
        elif any(word in title_lower for word in ['third', 'troisième', '3rd']):
            return 'third'
        elif any(word in title_lower for word in ['keeper', 'gardien', 'gk']):
            return 'keeper'
        elif any(word in title_lower for word in ['special', 'édition', 'limited']):
            return 'special'
        elif any(word in title_lower for word in ['vintage', 'retro', 'classic']):
            return 'vintage'
        elif any(word in title_lower for word in ['training', 'entraînement']):
            return 'training'
        else:
            return 'home'  # Par défaut

    def generate_tags(self, title):
        """Génère des tags en fonction du titre"""
        tags = ['fcpalestina']  # Tag obligatoire
        
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['new', 'nouveau', '2024', '2025']):
            tags.append('new')
        if any(word in title_lower for word in ['limited', 'édition', 'special']):
            tags.append('limited')
        if any(word in title_lower for word in ['classic', 'vintage', 'retro']):
            tags.append('classic')
            
        return tags

    def download_images(self, image_urls, jersey_id):
        """Télécharge les images et retourne les noms des fichiers locaux"""
        downloaded = []
        
        for i, image_url in enumerate(image_urls):
            try:
                # Nom de fichier local
                filename = f"{jersey_id}-hd-{i}.jpg"
                filepath = os.path.join(self.images_dir, filename)
                
                # Télécharger l'image
                response = self.session.get(image_url, timeout=30)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    downloaded.append(filename)
                    logger.info(f"💾 Image téléchargée: {filename}")
                    
            except Exception as e:
                logger.error(f"❌ Erreur téléchargement image {image_url}: {e}")
                continue
        
        return downloaded

    def save_data(self, jerseys):
        """Sauvegarde les données des maillots"""
        try:
            # Sauvegarder les jerseys
            jerseys_file = os.path.join(self.data_dir, 'jerseys.json')
            with open(jerseys_file, 'w', encoding='utf-8') as f:
                json.dump(jerseys, f, ensure_ascii=False, indent=2)
            
            # Sauvegarder les catégories
            categories = [
                {"id": cat_id, "name": cat_data["name"], "description": cat_data["description"]}
                for cat_id, cat_data in self.categories_mapping.items()
            ]
            
            categories_file = os.path.join(self.data_dir, 'categories.json')
            with open(categories_file, 'w', encoding='utf-8') as f:
                json.dump(categories, f, ensure_ascii=False, indent=2)
            
            # Sauvegarder les tags
            tags_file = os.path.join(self.data_dir, 'tags.json')
            with open(tags_file, 'w', encoding='utf-8') as f:
                json.dump(self.available_tags, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 Données sauvegardées: {len(jerseys)} maillots")
            
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde: {e}")

    def run_mass_import(self, max_albums=150):
        """Lance l'import massif"""
        logger.info(f"🚀 DÉMARRAGE IMPORT MASSIF - Max {max_albums} maillots")
        
        start_time = datetime.now()
        jerseys = []
        
        try:
            # Récupérer la liste des albums
            albums = self.get_album_list(max_pages=20)
            albums = albums[:max_albums]  # Limiter
            
            logger.info(f"📦 Processing {len(albums)} albums...")
            
            # Traitement par lots pour éviter la surcharge
            batch_size = 10
            for i in range(0, len(albums), batch_size):
                batch = albums[i:i+batch_size]
                
                logger.info(f"🔄 Traitement lot {i//batch_size + 1}/{(len(albums)-1)//batch_size + 1}")
                
                # Traitement parallèle du lot
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    future_to_album = {
                        executor.submit(self.extract_jersey_data, album['url'], album['title']): album 
                        for album in batch
                    }
                    
                    for future in concurrent.futures.as_completed(future_to_album):
                        album = future_to_album[future]
                        try:
                            jersey_data = future.result()
                            if jersey_data:
                                with self.data_lock:
                                    jerseys.append(jersey_data)
                                    self.imported_count += 1
                                logger.info(f"✅ Importé: {jersey_data['title'][:50]}...")
                            else:
                                with self.data_lock:
                                    self.failed_count += 1
                        except Exception as e:
                            logger.error(f"❌ Erreur traitement {album['url']}: {e}")
                            with self.data_lock:
                                self.failed_count += 1
                
                # Pause entre les lots
                time.sleep(2)
                
                # Sauvegarde intermédiaire toutes les 50 importations
                if len(jerseys) % 50 == 0 and jerseys:
                    self.save_data(jerseys)
                    logger.info(f"💾 Sauvegarde intermédiaire: {len(jerseys)} maillots")
            
            # Sauvegarde finale
            if jerseys:
                self.save_data(jerseys)
                
            # Statistiques finales
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info(f"""
🎉 IMPORT TERMINÉ !
━━━━━━━━━━━━━━━━━━━
✅ Maillots importés: {self.imported_count}
❌ Échecs: {self.failed_count}
⏱️ Durée: {duration}
📁 Données: {os.path.join(self.data_dir, 'jerseys.json')}
🖼️ Images: {self.images_dir}

Le site est maintenant prêt avec pagination automatique pour {self.imported_count} maillots !
            """)
            
        except Exception as e:
            logger.error(f"❌ Erreur critique import: {e}")

if __name__ == "__main__":
    importer = MassYupooImporter()
    importer.run_mass_import(max_albums=150)