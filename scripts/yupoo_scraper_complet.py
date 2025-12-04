#!/usr/bin/env python3
"""
Scraper Yupoo Complet avec Traduction et Téléchargement d'Images
Version complète pour FC Palestina
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
import hashlib
import random
from PIL import Image
import io
import urllib.request
from pathlib import Path
import argparse

# Configuration du logging (compatibilite Windows, pas d'emojis)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('yupoo_scraper_complet.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class YupooCompleteScraper:
    """Scraper Yupoo complet avec traduction et téléchargement d'images"""
    
    def __init__(self, base_url: str = "https://shixingtiyu.x.yupoo.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.dry_run = False  # peut etre active via argument
        self.generated_titles = set()  # pour assurer des titres uniques
        
        # Tables de traduction structurées
        self.team_map = {
            '巴萨': 'Barcelone', '巴塞罗那': 'Barcelone', '皇马': 'Real Madrid','拜仁': 'Bayern','曼联': 'Manchester United','曼城': 'Manchester City','利物浦': 'Liverpool','阿森纳': 'Arsenal','热刺': 'Tottenham','尤文': 'Juventus','米兰': 'AC Milan','国米': 'Inter Milan','多特': 'Dortmund','那不勒斯': 'Naples','马竞': 'Atletico Madrid','塞维利亚': 'Sevilla','巴勒斯坦': 'Palestine', '绿洲乐队': 'Oasis', '世星': 'Palestine'
        }
        self.category_tokens = {
            '主场': 'home','主': 'home','客场': 'away','客': 'away','第三': 'third','三': 'third','三客': 'third','守门员': 'keeper','门将': 'keeper','特别版': 'special','限量版': 'special','纪念版': 'special','复古': 'vintage','经典': 'vintage', '二客': 'away', '训练服': 'special', '训练': 'special'
        }
        self.color_map = {'黑': 'Noir','白': 'Blanc','红': 'Rouge','蓝': 'Bleu','绿': 'Vert','黄': 'Jaune','粉': 'Rose','灰': 'Gris','紫': 'Violet','橙': 'Orange'}
        self.size_pattern = re.compile(r'(?:[XSML]-)?S-\d?XL|XS-4XL|S-2XL|S-4XL|\d{1,2}-\d{1,2}[ ]?码?')
        self.season_pattern = re.compile(r'(\d{2}[-/]\d{2}|\d{4})')
        
        # Configuration des headers
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Créer le dossier pour les images
        self.images_dir = Path('assets/images/jerseys')
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # Variables pour suivre les progrès
        self.processed_jerseys = 0
        self.downloaded_images = 0
    
    def parse_and_translate(self, raw: str) -> dict:
        original = raw or ''
        
        # Extraire le nombre d'images depuis le titre (format: "Titre | 4")
        image_count_match = re.search(r'\|\s*(\d{1,2})\s*$', original)
        expected_image_count = None
        if image_count_match:
            expected_image_count = int(image_count_match.group(1))
            # Retirer le compteur du titre pour le parsing
            original = re.sub(r'\|\s*\d{1,2}\s*$', '', original).strip()
        
        s = original.replace('|', ' ').strip()
        size_match = self.size_pattern.search(s)
        size = size_match.group() if size_match else ''
        if size:
            s = s.replace(size, ' ')
        # Recherche de la saison/année partout dans le titre (début, milieu, fin)
        season = ''
        season_token = ''
        all_season_matches = list(self.season_pattern.finditer(original))
        if all_season_matches:
            # Prendre la dernière occurrence (souvent la vraie saison)
            last_match = all_season_matches[-1]
            token = last_match.group()
            
            if len(token) == 4 and token.isdigit():  # 2526 ou 9798
                prefix = '20' if int(token[:2]) <= 30 else '19'
                season = f"{prefix}{token[:2]}-{prefix}{token[2:]}"
            else:
                parts = re.split('[-/]', token)
                if len(parts) == 2 and all(len(p) == 2 and p.isdigit() for p in parts):
                    prefix1 = '20' if int(parts[0]) <= 30 else '19'
                    prefix2 = '20' if int(parts[1]) <= 30 else '19'
                    season = f"{prefix1}{parts[0]}-{prefix2}{parts[1]}"
                else:
                    season = token
            # Enlever la saison du titre pour la suite du parsing
            s = s.replace(token, ' ')
        team = ''
        for k, v in self.team_map.items():
            if k in s:
                team = v
                s = s.replace(k, ' ')
                break
        category = 'home'
        for k, cat in self.category_tokens.items():
            if k in s:
                category = cat
                s = s.replace(k, ' ')
                break
        colors = []
        for k, v in self.color_map.items():
            if k in s:
                colors.append(v)
                s = s.replace(k, ' ')
        remainder = re.sub(r'\s+', ' ', s).strip()
        cat_label = {
            'home': 'Domicile', 'away': 'Extérieur', 'third': 'Troisième', 'keeper': 'Gardien', 'special': 'Édition Spéciale', 'vintage': 'Vintage'
        }[category]
        parts = []
        # Si aucune saison trouvée, ne pas forcer 2024-2025 si le titre contient déjà une année ailleurs
        season_full = season if season else ''
        season_short = ''
        if season_full and re.match(r'20\d{2}-20\d{2}', season_full):
            # Transformer 2024-2025 -> 24/25 pour affichage titre
            season_short = f"{season_full[2:4]}/{season_full[7:9]}"
        elif season_full:
            season_short = season_full
        if season_short:
            parts.append(season_short)
        if team:
            parts.append(team)
        parts.append(cat_label)
        if size:
            parts.append(size)
        french_title = ' '.join(parts).strip() or 'Maillot Palestine'
        logger.info(f"Parse titre: '{original}' -> '{french_title}' (season_full={season_full}, team={team}, category={category}, size={size}, expected_images={expected_image_count})")
        return {
            'season_full': season_full,
            'season': season_full,  # compat
            'season_short': season_short,
            'team': team or 'Palestine',
            'category': category,
            'size': size,
            'colors': colors,
            'remainder': remainder,
            'title': french_title,
            'expected_image_count': expected_image_count
        }

    def standardize_category(self, parsed: dict) -> str:
        return parsed.get('category', 'home')
    
    def determine_category_from_title(self, title: str) -> str:
        """Ancienne méthode conservée pour fallback, renvoie catégories normalisées"""
        title_lower = title.lower()
        if any(k in title_lower for k in ['gardien', 'goalkeeper', 'gk']):
            return 'keeper'
        if any(k in title_lower for k in ['extérieur', 'exterieur', 'away', 'troisième']):
            return 'away'
        if any(k in title_lower for k in ['rétro', 'retro', 'vintage', 'classique']):
            return 'vintage'
        if any(k in title_lower for k in ['spéciale', 'edition', 'édition', 'special']):
            return 'special'
        return 'home'
    
    def download_image(self, image_url: str, jersey_id: str, image_index: int) -> str:
        """Télécharge une image et retourne uniquement le nom de fichier (frontend prefixe)."""
        try:
            # Nettoyer l'URL
            if not image_url.startswith('http'):
                image_url = 'https:' + image_url if image_url.startswith('//') else f"https://{image_url}"
            
            # Créer un nom de fichier unique
            file_extension = '.jpg'  # Extension par défaut
            try:
                parsed_url = urlparse(image_url)
                if '.' in parsed_url.path:
                    file_extension = '.' + parsed_url.path.split('.')[-1]
            except:
                pass
            
            filename = f"{jersey_id}_{image_index}{file_extension}"
            local_path = self.images_dir / filename
            
            # Télécharger l'image
            logger.info(f"Telechargement: {image_url} -> {filename}")
            
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Referer': self.base_url,
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
            }
            
            if not self.dry_run:
                response = requests.get(image_url, headers=headers, timeout=30)
                response.raise_for_status()
                with open(local_path, 'wb') as f:
                    f.write(response.content)
            
            self.downloaded_images += 1
            logger.info(f"Image telechargee: {filename}")
            
            # Retourner le chemin relatif
            return filename
            
        except Exception as e:
            logger.error(f"Erreur telechargement image {image_url}: {e}")
            return "placeholder.jpg"  # Image par défaut
    
    def extract_cover_image(self, soup: BeautifulSoup, album_url: str) -> str:
        """Extrait l'image de couverture/présentation (celle à côté du titre en haut sur Yupoo)"""
        
        # Sélecteurs Yupoo corrects basés sur l'analyse HTML réelle
        cover_selectors = [
            '.showalbumheader__gallerycover img',  # Sélecteur principal trouvé
            '.showalbumheader__gallerycover .autocover',
            '.album__cover img',
            '.showalbum__cover img', 
            '.album-cover img'
        ]
        
        for selector in cover_selectors:
            cover_elem = soup.select_one(selector)
            if cover_elem:
                img_url = cover_elem.get('data-src') or cover_elem.get('src') or cover_elem.get('data-original')
                if img_url and 'photo' in img_url.lower():
                    # Normaliser l'URL
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif not img_url.startswith('http'):
                        img_url = urljoin(album_url, img_url)
                    
                    # Garder medium (bonne qualité accessible), améliorer small/square vers medium
                    img_url = img_url.replace('/small.jpg', '/medium.jpg').replace('/square.jpg', '/medium.jpg')
                    
                    logger.info(f"✅ Image de couverture trouvée via {selector}: {img_url}")
                    return img_url
        
        logger.warning("⚠️ Image de couverture introuvable, utilisation de la première image de galerie")
        return None

    def extract_images_from_album(self, soup: BeautifulSoup, album_url: str) -> list:
        """Extrait toutes les images d'un album Yupoo"""
        images = []
        
        # Sélecteurs pour les images Yupoo
        image_selectors = [
            'img[data-src]',
            'img[src*="yupoo"]',
            '.image img',
            '.photo img', 
            '.album-photo img',
            'img[src*="photo"]',
            'img[alt*="photo"]'
        ]
        
        found_imgs = []
        for selector in image_selectors:
            found_imgs.extend(soup.select(selector))
        
        # Extraire seulement les images principales de l'album
        for img in found_imgs:
            img_url = img.get('data-src') or img.get('src') or img.get('data-original')
            if img_url and 'yupoo' in img_url:
                # Nettoyer et normaliser l'URL
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                elif not img_url.startswith('http'):
                    img_url = urljoin(album_url, img_url)
                
                # Prendre seulement les images qui ont "photo" dans l'URL (vraies photos)
                if 'photo' not in img_url:
                    continue
                    
                # Ignorer les éléments du site (pas les photos de produit)
                if any(x in img_url for x in ['website', 'logo', 'layout']):
                    continue

                # Éviter les doublons
                if img_url not in images:
                    images.append(img_url)
                    
                # Limiter à 6 images max pour éviter les excès
                if len(images) >= 6:
                    break
        
        # Fonction pour vérifier si une image est de haute qualité
        def is_high_quality(url: str) -> bool:
            """Garder seulement les images raw, big, ou large (pas medium, small, square)"""
            url_lower = url.lower()
            # Exclure les basses qualités
            if any(x in url_lower for x in ['medium', 'small', 'square']):
                return False
            # Inclure les hautes qualités
            return any(x in url_lower for x in ['raw', 'big', 'large'])
        
        # Filtrer pour garder uniquement les images haute qualité
        high_quality_images = [img for img in images if is_high_quality(img)]
        
        # Grouper par nom de base pour éviter les doublons de la même image
        from collections import defaultdict
        import re
        grouped = defaultdict(list)
        for img_url in high_quality_images:
            # Extraire l'identifiant de base (avant .jpg, .png, etc.)
            base_name = re.sub(r'_(raw|big|large|medium|small|square)\.(jpg|jpeg|png|webp)', '', img_url.lower())
            grouped[base_name].append(img_url)
        
        # Prendre la meilleure qualité de chaque groupe
        final_images = []
        for base_name, urls in grouped.items():
            # Trier par qualité (raw > big > large)
            def quality_rank(u: str):
                u_low = u.lower()
                if 'raw' in u_low: return 0
                if 'big' in u_low: return 1
                if 'large' in u_low: return 2
                return 3
            urls.sort(key=quality_rank)
            final_images.append(urls[0])  # Prendre la meilleure
        
        logger.info(f"Trouvé {len(images)} images totales → {len(high_quality_images)} haute qualité → {len(final_images)} uniques")
        return final_images
    
    def scrape_album_page(self, album_url: str, album_title: str = None) -> dict:
        """Scrape un album Yupoo individuel avec titre pré-extrait"""
        try:
            logger.info(f"Scraping album: {album_url}")
            
            # Récupérer la page de l'album
            response = self.session.get(album_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Utiliser le titre depuis categories ou fallback
            title = album_title
            if not title:
                title_selectors = ['h1', '.album-title', '.photo-title', 'title', '.title']
                for selector in title_selectors:
                    title_elem = soup.select_one(selector)
                    if title_elem and title_elem.get_text().strip():
                        title = title_elem.get_text().strip()
                        break
            
            if not title:
                title = "Maillot FC Palestina"
            
            # Parsing structuré + traduction
            raw_title = title
            parsed = self.parse_and_translate(title)
            category_std = self.standardize_category(parsed)
            translated_title = parsed['title']
            # Unicité si titre trop générique
            if translated_title.lower() in ['', 'maillot palestine'] or translated_title.strip() == 'Maillot Palestine':
                translated_title = f"{parsed.get('season_short') or parsed.get('season_full')} {parsed.get('team')} {category_std}".strip()
            if translated_title in self.generated_titles:
                translated_title = f"{translated_title} #{len(self.generated_titles)+1}"
            self.generated_titles.add(translated_title)

            # Filtre d'exclusion : ne pas importer Barcelone ou Real Madrid
            exclude_clubs = ['barcelone', 'barcelona', 'real madrid']
            title_check = (translated_title or '').lower() + ' ' + (raw_title or '').lower()
            if any(club in title_check for club in exclude_clubs):
                logger.info(f"⚠️ Maillot exclu (club filtré): {translated_title}")
                return None
            
            # Extraire l'image de couverture Yupoo (présentation en haut)
            cover_image_url = self.extract_cover_image(soup, album_url)
            
            # Extraire les images de la galerie
            image_urls = self.extract_images_from_album(soup, album_url)
            
            if not image_urls:
                logger.warning(f"Aucune image trouvée pour {album_url}")
                return None
            
            # Limiter au nombre d'images attendu si spécifié dans le titre
            expected_count = parsed.get('expected_image_count')
            if expected_count and len(image_urls) > expected_count:
                logger.info(f"Limitation des images: {len(image_urls)} → {expected_count} (selon titre)")
                image_urls = image_urls[:expected_count]
            
            # Générer un ID unique
            jersey_id = hashlib.md5(f"{translated_title}{album_url}".encode()).hexdigest()[:12]
            
            # Télécharger l'image de couverture (présentation Yupoo)
            cover_image_name = None
            if cover_image_url:
                cover_image_name = self.download_image(cover_image_url, jersey_id, 'cover')
                time.sleep(0.5)
            
            # Télécharger les images de la galerie
            local_images = []
            for i, img_url in enumerate(image_urls):
                local_name = self.download_image(img_url, jersey_id, i)
                local_images.append(local_name)
                time.sleep(0.5)  # Pause entre téléchargements

            # Utiliser l'image de couverture comme thumbnail, sinon première galerie
            thumbnail = cover_image_name if (cover_image_name and cover_image_name != "placeholder.jpg") else (local_images[0] if local_images else "placeholder.jpg")

            # Créer l'objet maillot
            jersey = {
                'id': jersey_id,
                'raw_title': raw_title,
                'title': translated_title,
                'name': translated_title,  # certains scripts utilisent name
                'description': f"Maillot officiel FC Palestina - {translated_title}" if 'Maillot officiel FC Palestina' not in translated_title else translated_title,
                'category': category_std,
                'price': None,
                'images': local_images,  # liste de noms simples, pas de placeholder
                'thumbnail': thumbnail,
                'tags': self.generate_tags(translated_title, category_std, parsed),
                'expected_image_count': expected_count or len(local_images),
                'views': random.randint(100, 1500),
                'featured': 'Palestine' in translated_title or random.random() > 0.9,
                'source_url': album_url,
                'last_updated': datetime.now().isoformat()
            }
            
            self.processed_jerseys += 1
            logger.info(f"Maillot cree: {translated_title} ({category_std})")
            
            return jersey
            
        except Exception as e:
            logger.error(f"Erreur scraping {album_url}: {e}")
            return None
    
    def extract_year_from_title(self, title: str) -> str:
        """Extrait l'année du titre"""
        # Chercher des patterns d'année
        year_patterns = [
            r'20\d{2}[-–]20\d{2}',  # 2024-2025
            r'20\d{2}',             # 2024
            r'\d{4}[-–]\d{4}',      # 2425 -> 2024-2025
        ]
        
        for pattern in year_patterns:
            match = re.search(pattern, title)
            if match:
                year = match.group()
                # Convertir 2425 en 2024-2025
                if len(year) == 4 and year.isdigit():
                    return f"20{year[:2]}-20{year[2:]}"
                return year
        
        return "2024-2025"  # Année par défaut
    
    def generate_tags(self, title: str, category: str, parsed: dict) -> list:
        """Génère des tags en respectant la liste blanche depuis tags.json"""
        # Liste blanche connue côté frontend
        valid = {'fcpalestina', 'new', 'popular', 'classic', 'home', 'away', 'keeper'}
        tags = set(['fcpalestina'])
        if category in valid:
            tags.add(category)
        # Vintage -> classic si présent
        if category == 'vintage' and 'classic' in valid:
            tags.add('classic')
        # Spécial / third souvent mises en avant
        if category in ('special', 'third') and 'popular' in valid:
            tags.add('popular')
        # Saison la plus récente -> new
        current_year = datetime.now().year
        season_full = parsed.get('season_full') or ''
        if re.match(r'20\d{2}-20\d{2}', season_full):
            end_year = int(season_full.split('-')[1])
            if end_year >= current_year and 'new' in valid:
                tags.add('new')
        return list(tags)
    
    def get_all_album_links(self) -> list:
        """Récupère tous les liens d'albums depuis les pages categories"""
        album_links = []
        try:
            logger.info(f"Recuperation des albums depuis {self.base_url}/categories")
            # Parcourir les pages jusqu'à ce qu'il n'y ait plus d'albums (avec garde-fou)
            page = 1
            max_pages = 30  # sécurité
            while page <= max_pages:
                try:
                    page_url = f"{self.base_url}/categories/?page={page}"
                    response = self.session.get(page_url, timeout=30)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Chercher les liens d'albums
                    links = soup.select('a[href*=\"/albums/\"]')
                    page_albums = []
                    for link in links:
                        href = link.get('href')
                        title_attr = link.get('title', '').strip()
                        if href and title_attr:
                            full_url = urljoin(self.base_url, href)
                            parsed = urlparse(full_url)
                            path = parsed.path
                            if re.search(r'^/albums/\d+', path):
                                album_info = (full_url, title_attr)
                                if album_info not in album_links:
                                    album_links.append(album_info)
                                    page_albums.append(album_info)
                    logger.info(f"Page {page}: {len(page_albums)} albums trouves")
                    if not page_albums:
                        break
                    page += 1
                    time.sleep(1)
                except Exception as e:
                    logger.error(f"Erreur page {page}: {e}")
                    break
            logger.info(f"Total: {len(album_links)} albums trouves")
            return album_links
        except Exception as e:
            logger.error(f"Erreur recuperation albums: {e}")
            return []
    
    def scrape_all_jerseys(self, fresh: bool = False, limit: int = None) -> bool:
        """Lance le scraping complet de tous les maillots"""
        try:
            logger.info("Debut du scraping complet Yupoo")
            
            # Récupérer tous les liens d'albums
            album_links = self.get_all_album_links()
            if limit:
                album_links = album_links[:limit]
            
            if not album_links:
                logger.error("❌ Aucun album trouvé")
                return False
            
            logger.info(f"A traiter: {len(album_links)} albums")
            
            # Charger les maillots existants pour éviter les doublons
            existing_jerseys = []
            if not fresh and os.path.exists('data/jerseys.json'):
                try:
                    with open('data/jerseys.json', 'r', encoding='utf-8') as f:
                        existing_jerseys = json.load(f)
                    logger.info(f"📁 {len(existing_jerseys)} maillots existants chargés")
                except Exception as e:
                    logger.warning(f"Impossible de charger les maillots existants: {e}")
                    existing_jerseys = []
            elif fresh and os.path.exists('data/jerseys.json'):
                # Faire une sauvegarde explicite du fichier actuel avant de repartir de zéro
                try:
                    os.makedirs('data/backups', exist_ok=True)
                    backup_name = f"data/backups/jerseys_fresh_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    import shutil
                    shutil.copy2('data/jerseys.json', backup_name)
                    logger.info(f"Backup effectue: {backup_name}")
                except Exception as e:
                    logger.warning(f"Echec backup avant fresh: {e}")
            
            existing_ids = {jersey.get('id') for jersey in existing_jerseys}
            
            # Scraper chaque album
            new_jerseys = []
            
            for i, album_info in enumerate(album_links, 1):
                try:
                    # Gérer les formats (url, title) ou url seul
                    if isinstance(album_info, tuple):
                        album_url, album_title = album_info
                    else:
                        album_url = album_info
                        album_title = None
                    
                    logger.info(f"Traitement {i}/{len(album_links)}: {album_url}")
                    if album_title:
                        logger.info(f"Titre extrait: {album_title}")
                    
                    jersey = self.scrape_album_page(album_url, album_title)
                    
                    if jersey and jersey['id'] not in existing_ids:
                        new_jerseys.append(jersey)
                        existing_ids.add(jersey['id'])
                        logger.info(f"Nouveau maillot ajoute: {jersey['title']}")
                    elif jersey:
                        logger.info(f"Maillot deja existant: {jersey['title']}")
                    
                    # Pause entre requêtes
                    time.sleep(random.uniform(1, 3))
                    
                    # Sauvegarder régulièrement
                    if len(new_jerseys) % 10 == 0:
                        self.save_jerseys(existing_jerseys + new_jerseys)
                        logger.info(f"Sauvegarde intermediaire: {len(existing_jerseys + new_jerseys)} maillots")
                    
                except Exception as e:
                    logger.error(f"❌ Erreur album {album_url}: {e}")
                    continue
            
            # Nettoyage des entrees invalides (anciennes erreurs de pagination)
            def is_valid_entry(j):
                src = j.get('source_url', '')
                if 'page=' in src and not re.search(r'/(albums|photos)/\d+', src):
                    return False
                return True

            cleaned_existing = [j for j in existing_jerseys if is_valid_entry(j)]
            removed = len(existing_jerseys) - len(cleaned_existing)
            if removed:
                logger.info(f"Nettoyage: {removed} entrees invalides supprimees")

            # Sauvegarde finale
            all_jerseys = (cleaned_existing + new_jerseys) if not fresh else new_jerseys
            success = self.save_jerseys(all_jerseys)
            
            if success:
                logger.info(f"Scraping termine avec succes")
                logger.info(f"Statistiques:")
                logger.info(f"  - Nouveaux maillots: {len(new_jerseys)}")
                logger.info(f"  - Total maillots: {len(all_jerseys)}")
                logger.info(f"  - Images telechargees: {self.downloaded_images}")
                return True
            else:
                logger.error("Erreur lors de la sauvegarde finale")
                return False
            
        except Exception as e:
            logger.error(f"Erreur scraping general: {e}")
            return False
    
    def save_jerseys(self, jerseys: list) -> bool:
        """Sauvegarde les maillots en JSON"""
        try:
            # Créer le dossier data s'il n'existe pas
            os.makedirs('data', exist_ok=True)
            
            # Faire une sauvegarde de l'ancien fichier
            if os.path.exists('data/jerseys.json'):
                backup_name = f"data/backups/jerseys_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                os.makedirs('data/backups', exist_ok=True)
                import shutil
                shutil.copy2('data/jerseys.json', backup_name)
            
            # Sauvegarder les nouveaux jerseys
            with open('data/jerseys.json', 'w', encoding='utf-8') as f:
                json.dump(jerseys, f, ensure_ascii=False, indent=2)
            
            logger.info(f"{len(jerseys)} maillots sauvegardes dans data/jerseys.json")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde: {e}")
            return False

def main():
    """Fonction principale"""
    print("Scraper Yupoo Complet - FC Palestina")
    print("=" * 50)
    print("Fonctionnalites:")
    print("  - Traduction chinois -> francais")
    print("  - Telechargement d'images reelles")
    print("  - Categorisation automatique")
    print("  - Extraction complete (200+ maillots)")
    print()
    parser = argparse.ArgumentParser(description="Scraper Yupoo Complet FC Palestina")
    parser.add_argument('--fresh', action='store_true', help='Ignore les maillots existants et repart de zéro')
    parser.add_argument('--limit', type=int, help='Limite le nombre dalbums a traiter (debug)')
    parser.add_argument('--dry-run', action='store_true', help="Ne telecharge ni n'enregistre, simule seulement")
    args = parser.parse_args()

    scraper = YupooCompleteScraper()
    scraper.dry_run = args.dry_run
    
    success = scraper.scrape_all_jerseys(fresh=args.fresh, limit=args.limit)
    
    if success:
        print("\nScraping termine avec succes!")
        print("Rechargez votre site pour voir les nouveaux maillots")
    else:
        print("\nErreur lors du scraping")
        print("Consultez le fichier yupoo_scraper_complet.log pour plus de details")

if __name__ == "__main__":
    main()