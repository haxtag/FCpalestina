#!/usr/bin/env python3
"""
Uploader d'images vers un stockage S3-compatible (S3, Cloudflare R2, Backblaze B2, MinIO).

Pré-requis (variables d'environnement):
- S3_ENDPOINT_URL (ex: https://<account>.r2.cloudflarestorage.com ou https://s3.amazonaws.com)
- S3_BUCKET (ex: maillots-du-peuple)
- S3_REGION (ex: auto ou eu-west-3)
- S3_ACCESS_KEY
- S3_SECRET_KEY
- PUBLIC_BASE_URL (ex: https://cdn.example.com/jerseys ou https://<bucket>.r2.dev/jerseys)

Usage (local):
- Placez vos images réelles dans assets/images/jerseys/<fichiers> (comme en localhost)
- python scripts/upload_to_s3.py
=> Uploade tous les fichiers référencés dans data/jerseys.json s'ils existent localement
=> Affiche l'URL publique de base à copier dans data/config.json (site.images_base_url)
"""
import os
import sys
import json
from pathlib import Path

try:
    import boto3
    from botocore.config import Config
    from botocore.exceptions import BotoCoreError, ClientError
except Exception as e:
    print("boto3 manquant. Installez-le (pip install boto3) ou laissez requirements.txt le faire.")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
JERSEYS_JSON = BASE_DIR / 'data' / 'jerseys.json'
IMAGES_DIR = BASE_DIR / 'assets' / 'images' / 'jerseys'

ENDPOINT_URL = os.environ.get('S3_ENDPOINT_URL')
BUCKET = os.environ.get('S3_BUCKET')
REGION = os.environ.get('S3_REGION', 'auto')
ACCESS_KEY = os.environ.get('S3_ACCESS_KEY')
SECRET_KEY = os.environ.get('S3_SECRET_KEY')
PUBLIC_BASE_URL = os.environ.get('PUBLIC_BASE_URL')

missing_env = [k for k,v in {
    'S3_ENDPOINT_URL': ENDPOINT_URL,
    'S3_BUCKET': BUCKET,
    'S3_ACCESS_KEY': ACCESS_KEY,
    'S3_SECRET_KEY': SECRET_KEY,
    'PUBLIC_BASE_URL': PUBLIC_BASE_URL,
}.items() if not v]

if missing_env:
    print("Variables d'environnement manquantes:", ', '.join(missing_env))
    print("Veuillez définir ces variables avant de lancer le script.")
    sys.exit(2)

if not JERSEYS_JSON.exists():
    print(f"Fichier {JERSEYS_JSON} introuvable.")
    sys.exit(3)

session = boto3.session.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION,
)
s3 = session.client('s3', endpoint_url=ENDPOINT_URL, config=Config(s3={'addressing_style':'virtual'}))

with open(JERSEYS_JSON, 'r', encoding='utf-8') as f:
    jerseys = json.load(f)

expected = []
for j in jerseys:
    thumb = j.get('thumbnail')
    imgs = j.get('images') or []
    if isinstance(thumb, str) and thumb:
        expected.append(thumb)
    if isinstance(imgs, list):
        expected.extend([n for n in imgs if isinstance(n, str) and n])

expected = list(dict.fromkeys(expected))  # unique

uploaded = 0
missing_local = 0
errors = 0

for name in expected:
    local = IMAGES_DIR / name
    if not local.exists():
        missing_local += 1
        continue
    key = f"jerseys/{name}"
    try:
        print(f"Upload: {local.name} -> s3://{BUCKET}/{key}")
        with open(local, 'rb') as fh:
            s3.put_object(Bucket=BUCKET, Key=key, Body=fh, ContentType='image/jpeg', ACL='public-read')
        uploaded += 1
    except (BotoCoreError, ClientError) as e:
        print(f"Erreur upload {name}: {e}")
        errors += 1

print(f"Terminé: {uploaded} envoyées, {missing_local} absentes en local, {errors} erreurs")
print("Base publique suggérée pour config:", PUBLIC_BASE_URL)
print("Exemple d'URL: ", f"{PUBLIC_BASE_URL}/{expected[0]}" if expected else PUBLIC_BASE_URL)
