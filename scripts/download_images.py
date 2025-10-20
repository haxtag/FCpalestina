#!/usr/bin/env python3
"""
Script pour télécharger les images manquantes depuis les URLs dans jerseys.json
Utilisé temporairement pour les démos Render
"""

import json
import os
import shutil
from pathlib import Path
import logging

import requests
try:
    from PIL import Image, ImageDraw, ImageFont  # type: ignore
    PIL_AVAILABLE = True
except Exception:
    # Pillow non disponible (ex: avant installation) -> on tombera sur un fallback
    PIL_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def _ensure_placeholder_images(base_dir: Path) -> tuple[Path, Path]:
    """Crée un placeholder lisible si absent, et retourne ses 2 emplacements:
    - assets/img/placeholder.jpg
    - assets/images/jerseys/placeholder.jpg
    Utilise Pillow si dispo, sinon tente un fallback via une petite image distante.
    """
    placeholder_ui = base_dir / 'assets' / 'img' / 'placeholder.jpg'
    placeholder_jerseys = base_dir / 'assets' / 'images' / 'jerseys' / 'placeholder.jpg'

    # Créer dossiers
    placeholder_ui.parent.mkdir(parents=True, exist_ok=True)
    placeholder_jerseys.parent.mkdir(parents=True, exist_ok=True)

    def _generate_with_pillow(path: Path):
        # Image simple 400x400 avec cadre et texte
        img = Image.new('RGB', (400, 400), (44, 85, 48))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(10, 10), (390, 390)], outline=(141, 21, 56), width=10)
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except Exception:
            font = ImageFont.load_default()
        text = "MAILLOTS DU PEUPLE"
        bbox = draw.textbbox((0, 0), text, font=font)
        x = (400 - (bbox[2] - bbox[0])) // 2
        y = (400 - (bbox[3] - bbox[1])) // 2
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        img.save(path, 'JPEG', quality=85)

    # Générer le fichier principal s'il manque
    if not placeholder_ui.exists():
        try:
            if PIL_AVAILABLE:
                _generate_with_pillow(placeholder_ui)
                logger.info(f"Placeholder UI généré: {placeholder_ui}")
            else:
                # Fallback: télécharger une petite image de placeholder
                url = 'https://via.placeholder.com/400x400/2c5530/ffffff.jpg?text=Maillots+Du+Peuple'
                r = requests.get(url, timeout=20)
                r.raise_for_status()
                with open(placeholder_ui, 'wb') as f:
                    f.write(r.content)
                logger.info(f"Placeholder UI téléchargé: {placeholder_ui}")
        except Exception as e:
            logger.error(f"Impossible de créer le placeholder UI ({e})")

    # Dupliquer dans le dossier jerseys s'il manque
    if not placeholder_jerseys.exists():
        try:
            shutil.copyfile(placeholder_ui, placeholder_jerseys)
        except Exception as e:
            logger.error(f"Impossible de copier le placeholder vers jerseys ({e})")

    return placeholder_ui, placeholder_jerseys


def download_missing_images():
    """Complète les images manquantes pour la démo Render.
    Règles:
    - Si 'image_url' et 'image' sont fournis, télécharge depuis l'URL.
    - Sinon, pour chaque maillot, crée des fichiers placeholders pour
      'thumbnail' et les entrées de 'images' absentes dans assets/images/jerseys.
    """
    base_dir = Path.cwd()
    jerseys_file = base_dir / 'data' / 'jerseys.json'
    images_dir = base_dir / 'assets' / 'images' / 'jerseys'

    # Logs de contexte
    logger.info(f"Base directory: {base_dir}")
    logger.info(f"Jerseys file: {jerseys_file}")
    logger.info(f"Images directory: {images_dir}")

    # Vérifier que le fichier jerseys existe
    if not jerseys_file.exists():
        logger.error(f"Fichier jerseys.json introuvable: {jerseys_file}")
        return {"downloaded": 0, "placeholders": 0, "skipped": 0, "errors": 1}

    # Préparer les dossiers
    images_dir.mkdir(parents=True, exist_ok=True)

    # Assurer l'existence d'un placeholder unique à répliquer
    placeholder_ui, placeholder_jerseys = _ensure_placeholder_images(base_dir)

    # Charger les maillots
    with open(jerseys_file, 'r', encoding='utf-8') as f:
        jerseys = json.load(f)

    downloaded = 0
    placeholders_created = 0
    skipped = 0
    errors = 0

    logger.info(f"Vérification de {len(jerseys)} maillots...")

    for jersey in jerseys:
        # 1) Cas ancien schéma: 'image_url' + 'image'
        image_url = jersey.get('image_url')
        image_path = jersey.get('image')
        if image_url and image_path:
            local_image = base_dir / image_path.lstrip('/')
            if local_image.exists():
                skipped += 1
            else:
                try:
                    logger.info(f"Téléchargement: {local_image.name}")
                    response = requests.get(image_url, timeout=30)
                    response.raise_for_status()
                    local_image.parent.mkdir(parents=True, exist_ok=True)
                    with open(local_image, 'wb') as f:
                        f.write(response.content)
                    downloaded += 1
                except Exception as e:
                    logger.error(f"Erreur pour {local_image.name}: {e}")
                    errors += 1
            # On traite aussi le reste du schéma moderne ci-dessous

        # 2) Schéma actuel: 'thumbnail' (str) + 'images' (liste de noms)
        thumb = jersey.get('thumbnail')
        imgs = jersey.get('images') or []

        # Construire la liste de tous les fichiers attendus
        expected_files = []
        if isinstance(thumb, str) and thumb:
            expected_files.append(thumb)
        if isinstance(imgs, list):
            expected_files.extend([n for n in imgs if isinstance(n, str) and n])

        for name in expected_files:
            target_path = images_dir / name
            if target_path.exists():
                skipped += 1
                continue
            try:
                # Créer un fichier placeholder en copiant l'image placeholder jerseys
                shutil.copyfile(placeholder_jerseys, target_path)
                placeholders_created += 1
            except Exception as e:
                logger.error(f"Erreur création placeholder pour {name}: {e}")
                errors += 1

    logger.info(
        f"Terminé: {downloaded} téléchargées, {placeholders_created} placeholders créés, {skipped} existantes, {errors} erreurs"
    )
    return {
        "downloaded": downloaded,
        "placeholders": placeholders_created,
        "skipped": skipped,
        "errors": errors,
    }

if __name__ == '__main__':
    download_missing_images()
