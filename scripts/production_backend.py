#!/usr/bin/env python3
"""
Backend Flask de production pour FC Palestina
Comprend authentification, sécurité, gestion des erreurs
"""

import json
import os
import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS
import bcrypt

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend_production.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
JERSEYS_FILE = os.path.join(DATA_DIR, 'jerseys.json')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.json')
TAGS_FILE = os.path.join(DATA_DIR, 'tags.json')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.json')
CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')

# Créer l'application Flask
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Configuration CORS pour accepter les requêtes depuis Render et localhost
allowed_origins = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://fcpalestina.onrender.com',
    'http://fcpalestina.onrender.com'
]

CORS(app, 
     supports_credentials=True,
     origins=allowed_origins,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Configuration par défaut
DEFAULT_CONFIG = {
    "admin": {
        "username": "Badis",
        "password_hash": "$2b$12$mCDainvOZJaDYH7HSRaKg.LMXnCIzV8mxVHlLmJIjiozR8sh.3e0S",  # "MagikALi104"
        "session_timeout": 3600  # 1 heure
    },
    "site": {
        "name": "FC Palestina",
        "domain": "",
    "email": "contact@maillotsdupeuple.com",
        "maintenance_mode": False
    },
    "scraping": {
        "vinted_auto_update": True,
        "yupoo_auto_update": False,
        "update_time": "02:00"  # 2h du matin
    }
}

def load_config():
    """Charger la configuration"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
    except Exception as e:
        logger.error(f"Erreur chargement config: {e}")
        return DEFAULT_CONFIG

def save_config(config):
    """Sauvegarder la configuration"""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Erreur sauvegarde config: {e}")
        return False

def load_json_file(filepath, default=None):
    """Charger un fichier JSON"""
    if default is None:
        default = []
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    except Exception as e:
        logger.error(f"Erreur chargement {filepath}: {e}")
        return default

def save_json_file(filepath, data):
    """Sauvegarder des données JSON"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Erreur sauvegarde {filepath}: {e}")
        return False

def require_auth(f):
    """Décorateur pour vérifier l'authentification"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({"error": "Authentication required"}), 401
        
        # Vérifier l'expiration de la session
        if 'login_time' in session:
            config = load_config()
            timeout = config.get('admin', {}).get('session_timeout', 3600)
            if datetime.now().timestamp() - session['login_time'] > timeout:
                session.clear()
                return jsonify({"error": "Session expired"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

# Routes d'authentification
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authentification administrateur"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({"error": "Username et password requis"}), 400
        
        config = load_config()
        admin_config = config.get('admin', {})
        
        # Vérifier les identifiants
        if (username == admin_config.get('username') and 
            bcrypt.checkpw(password.encode('utf-8'), admin_config.get('password_hash', '').encode('utf-8'))):
            
            session['authenticated'] = True
            session['username'] = username
            session['login_time'] = datetime.now().timestamp()
            
            logger.info(f"Connexion admin réussie: {username}")
            return jsonify({
                "success": True,
                "message": "Connexion réussie",
                "user": username
            })
        else:
            logger.warning(f"Tentative de connexion échouée: {username}")
            return jsonify({"error": "Identifiants invalides"}), 401
            
    except Exception as e:
        logger.error(f"Erreur login: {e}")
        return jsonify({"error": "Erreur serveur"}), 500

@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def logout():
    """Déconnexion"""
    username = session.get('username')
    session.clear()
    logger.info(f"Déconnexion: {username}")
    return jsonify({"success": True, "message": "Déconnexion réussie"})

@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Vérifier le statut d'authentification"""
    return jsonify({
        "authenticated": session.get('authenticated', False),
        "username": session.get('username')
    })

# Routes publiques (site web)
@app.route('/api/jerseys', methods=['GET'])
def get_jerseys():
    """Récupérer les maillots (public)"""
    jerseys = load_json_file(JERSEYS_FILE, [])
    # Filtrer les maillots actifs uniquement
    active_jerseys = [j for j in jerseys if j.get('active', True)]
    return jsonify(active_jerseys)

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    """Récupérer les avis (public)"""
    reviews_data = load_json_file(REVIEWS_FILE, {"reviews": []})
    return jsonify(reviews_data)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Récupérer les catégories (public)"""
    categories = load_json_file(CATEGORIES_FILE, [
        {"id": "domicile", "name": "Domicile", "color": "#8B1538"},
        {"id": "exterieur", "name": "Extérieur", "color": "#000000"},
        {"id": "speciaux", "name": "Spéciaux", "color": "#FFD700"}
    ])
    return jsonify(categories)

# Routes administrateur
@app.route('/api/admin/jerseys', methods=['GET'])
@require_auth
def admin_get_jerseys():
    """Récupérer tous les maillots (admin)"""
    jerseys = load_json_file(JERSEYS_FILE, [])
    return jsonify(jerseys)

@app.route('/api/admin/jerseys', methods=['POST'])
@require_auth
def admin_add_jersey():
    """Ajouter un maillot"""
    try:
        data = request.get_json()
        jerseys = load_json_file(JERSEYS_FILE, [])
        
        # Générer un nouvel ID
        max_id = max([int(j.get('id', 0)) for j in jerseys] + [0])
        
        new_jersey = {
            "id": str(max_id + 1),
            "name": data.get('name', ''),
            "title": data.get('title', data.get('name', '')),
            "description": data.get('description', ''),
            "category": data.get('category', ''),
            "categories": data.get('categories', []),
            "tags": data.get('tags', []),
            "year": data.get('year', ''),
            "size": data.get('size', 'M'),
            "price": data.get('price', 19.90),
            "images": data.get('images', []),
            "thumbnail": data.get('thumbnail', ''),
            "active": data.get('active', True),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        jerseys.append(new_jersey)
        
        if save_json_file(JERSEYS_FILE, jerseys):
            logger.info(f"Maillot ajouté: {new_jersey['name']}")
            return jsonify({"success": True, "jersey": new_jersey})
        else:
            return jsonify({"error": "Erreur sauvegarde"}), 500
            
    except Exception as e:
        logger.error(f"Erreur ajout maillot: {e}")
        return jsonify({"error": "Erreur serveur"}), 500

@app.route('/api/admin/jerseys/<jersey_id>', methods=['PUT'])
@require_auth
def admin_update_jersey(jersey_id):
    """Mettre à jour un maillot"""
    try:
        data = request.get_json()
        jerseys = load_json_file(JERSEYS_FILE, [])
        
        for i, jersey in enumerate(jerseys):
            if jersey.get('id') == jersey_id:
                # Mettre à jour les champs
                jerseys[i].update({
                    'name': data.get('name', jersey.get('name')),
                    'title': data.get('title', data.get('name', jersey.get('title'))),
                    'description': data.get('description', jersey.get('description')),
                    'category': data.get('category', jersey.get('category')),
                    'categories': data.get('categories', jersey.get('categories', [])),
                    'tags': data.get('tags', jersey.get('tags', [])),
                    'year': data.get('year', jersey.get('year')),
                    'size': data.get('size', jersey.get('size')),
                    'price': data.get('price', jersey.get('price')),
                    'active': data.get('active', jersey.get('active', True)),
                    'updated_at': datetime.now().isoformat()
                })
                
                if save_json_file(JERSEYS_FILE, jerseys):
                    logger.info(f"Maillot mis à jour: {jersey_id}")
                    return jsonify({"success": True, "jersey": jerseys[i]})
                else:
                    return jsonify({"error": "Erreur sauvegarde"}), 500
        
        return jsonify({"error": "Maillot non trouvé"}), 404
        
    except Exception as e:
        logger.error(f"Erreur mise à jour maillot: {e}")
        return jsonify({"error": "Erreur serveur"}), 500

@app.route('/api/admin/jerseys/<jersey_id>', methods=['DELETE'])
@require_auth
def admin_delete_jersey(jersey_id):
    """Supprimer un maillot"""
    try:
        jerseys = load_json_file(JERSEYS_FILE, [])
        
        for i, jersey in enumerate(jerseys):
            if jersey.get('id') == jersey_id:
                deleted_jersey = jerseys.pop(i)
                
                if save_json_file(JERSEYS_FILE, jerseys):
                    logger.info(f"Maillot supprimé: {jersey_id}")
                    return jsonify({"success": True, "deleted": deleted_jersey})
                else:
                    return jsonify({"error": "Erreur sauvegarde"}), 500
        
        return jsonify({"error": "Maillot non trouvé"}), 404
        
    except Exception as e:
        logger.error(f"Erreur suppression maillot: {e}")
        return jsonify({"error": "Erreur serveur"}), 500

@app.route('/api/admin/config', methods=['GET'])
@require_auth
def admin_get_config():
    """Récupérer la configuration"""
    config = load_config()
    # Ne pas retourner le hash du mot de passe
    safe_config = config.copy()
    if 'admin' in safe_config and 'password_hash' in safe_config['admin']:
        del safe_config['admin']['password_hash']
    return jsonify(safe_config)

@app.route('/api/admin/config', methods=['POST'])
@require_auth
def admin_update_config():
    """Mettre à jour la configuration"""
    try:
        data = request.get_json()
        config = load_config()
        
        # Mettre à jour les sections autorisées
        if 'site' in data:
            config['site'].update(data['site'])
        if 'scraping' in data:
            config['scraping'].update(data['scraping'])
        
        if save_config(config):
            logger.info("Configuration mise à jour")
            return jsonify({"success": True, "config": config})
        else:
            return jsonify({"error": "Erreur sauvegarde"}), 500
            
    except Exception as e:
        logger.error(f"Erreur mise à jour config: {e}")
        return jsonify({"error": "Erreur serveur"}), 500

@app.route('/api/admin/stats', methods=['GET'])
@require_auth
def admin_get_stats():
    """Récupérer les statistiques"""
    try:
        jerseys = load_json_file(JERSEYS_FILE, [])
        reviews_data = load_json_file(REVIEWS_FILE, {"reviews": []})
        reviews = reviews_data.get('reviews', [])
        
        stats = {
            "jerseys": {
                "total": len(jerseys),
                "active": len([j for j in jerseys if j.get('active', True)]),
                "inactive": len([j for j in jerseys if not j.get('active', True)])
            },
            "reviews": {
                "total": len(reviews),
                "average_rating": sum([r.get('rating', 5) for r in reviews]) / len(reviews) if reviews else 0,
                "last_updated": reviews_data.get('last_updated', 'Jamais')
            },
            "server": {
                "uptime": "En ligne",
                "last_backup": datetime.now().isoformat()
            }
        }
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Erreur récupération stats: {e}")
        return jsonify({"error": "Erreur serveur"}), 500

# Routes spécifiques compatibles avec simple_backend
@app.route('/api/jerseys/update', methods=['POST'])
@require_auth
def update_jersey_simple():
    """Mettre à jour un maillot (compatible simple_backend)"""
    try:
        data = request.get_json()
        jersey_id = data.get('jersey_id')
        
        if not jersey_id:
            return jsonify({"error": "jersey_id manquant"}), 400
        
        jerseys = load_json_file(JERSEYS_FILE, [])
        
        updated = False
        for i, jersey in enumerate(jerseys):
            if jersey.get('id') == jersey_id:
                # Récupérer les catégories (peut être envoyé en "category" ou "categories")
                cats = data.get('category', data.get('categories', jersey.get('categories', [])))
                if isinstance(cats, str):
                    cats = [cats] if cats else []
                
                jerseys[i].update({
                    'name': data.get('name', jersey.get('name', '')),
                    'title': data.get('name', jersey.get('title', '')),
                    'description': data.get('description', jersey.get('description', '')),
                    'category': cats,  # Array de catégories
                    'categories': cats,  # Compatibilité
                    'tags': data.get('tags', jersey.get('tags', [])),
                    'year': data.get('year', jersey.get('year', '')),
                    'size': data.get('size', jersey.get('size', '')),
                    'price': data.get('price', jersey.get('price', '')),
                    'updated_at': datetime.now().isoformat()
                })
                updated = True
                break
        
        if not updated:
            return jsonify({"error": "Maillot non trouvé"}), 404
        
        if save_json_file(JERSEYS_FILE, jerseys):
            return jsonify({"success": True, "message": "Maillot mis à jour"})
        else:
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la mise à jour: {str(e)}"}), 500

@app.route('/api/jerseys/update-cover', methods=['POST'])
@require_auth
def update_cover_simple():
    """Mettre à jour l'image de couverture (compatible simple_backend)"""
    try:
        data = request.get_json()
        jersey_id = data.get('jersey_id')
        cover_image = data.get('cover_image')
        
        if not jersey_id or not cover_image:
            return jsonify({"error": "jersey_id et cover_image requis"}), 400
        
        jerseys = load_json_file(JERSEYS_FILE, [])
        
        updated = False
        for i, jersey in enumerate(jerseys):
            if jersey.get('id') == jersey_id:
                jerseys[i]['thumbnail'] = cover_image
                jerseys[i]['updated_at'] = datetime.now().isoformat()
                updated = True
                break
        
        if not updated:
            return jsonify({"error": "Maillot non trouvé"}), 404
        
        if save_json_file(JERSEYS_FILE, jerseys):
            return jsonify({"success": True, "message": "Image de couverture mise à jour"})
        else:
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la mise à jour: {str(e)}"}), 500

@app.route('/api/tags', methods=['GET'])
def get_tags():
    """Récupérer tous les tags (public)"""
    tags = load_json_file(TAGS_FILE, [
        {"id": "tag_1", "name": "Nouveau", "color": "#00FF00"},
        {"id": "tag_2", "name": "Populaire", "color": "#FF6B6B"},
        {"id": "tag_3", "name": "Limité", "color": "#FFD700"}
    ])
    return jsonify(tags)

@app.route('/api/categories/create', methods=['POST'])
@require_auth
def create_category():
    """Créer une nouvelle catégorie"""
    try:
        data = request.get_json()
        categories = load_json_file(CATEGORIES_FILE, [])
        
        # Générer un ID basé sur le nom (slug)
        name = data.get('name', '').strip()
        if not name:
            return jsonify({"error": "Le nom est requis"}), 400
        
        # Créer un slug (ID) à partir du nom
        import re
        import unicodedata
        
        # Normaliser et retirer les accents
        slug = unicodedata.normalize('NFKD', name.lower())
        slug = slug.encode('ascii', 'ignore').decode('ascii')
        # Remplacer les espaces et caractères spéciaux par des underscores
        slug = re.sub(r'[^a-z0-9]+', '_', slug)
        slug = slug.strip('_')
        
        # Si le slug est vide, utiliser un ID générique
        if not slug:
            slug = f"cat_{len(categories) + 1}"
        
        # Vérifier l'unicité de l'ID
        base_slug = slug
        counter = 1
        while any(cat['id'] == slug for cat in categories):
            slug = f"{base_slug}_{counter}"
            counter += 1
        
        new_category = {
            "id": slug,
            "name": name,
            "color": data.get('color', '#8B1538')
        }
        
        categories.append(new_category)
        
        if save_json_file(CATEGORIES_FILE, categories):
            return jsonify({"success": True, "category": new_category})
        else:
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
            
    except Exception as e:
        logger.error(f"Erreur création catégorie: {e}")
        return jsonify({"error": f"Erreur lors de la création: {str(e)}"}), 500

@app.route('/api/tags/create', methods=['POST'])
@require_auth
def create_tag():
    """Créer un nouveau tag"""
    try:
        data = request.get_json()
        tags = load_json_file(TAGS_FILE, [])
        
        # Générer un ID basé sur le nom (slug)
        name = data.get('name', '').strip()
        if not name:
            return jsonify({"error": "Le nom est requis"}), 400
        
        # Créer un slug (ID) à partir du nom
        import re
        import unicodedata
        
        # Normaliser et retirer les accents
        slug = unicodedata.normalize('NFKD', name.lower())
        slug = slug.encode('ascii', 'ignore').decode('ascii')
        # Remplacer les espaces et caractères spéciaux par des underscores
        slug = re.sub(r'[^a-z0-9]+', '_', slug)
        slug = slug.strip('_')
        
        # Si le slug est vide, utiliser un ID générique
        if not slug:
            slug = f"tag_{len(tags) + 1}"
        
        # Vérifier l'unicité de l'ID
        base_slug = slug
        counter = 1
        while any(tag['id'] == slug for tag in tags):
            slug = f"{base_slug}_{counter}"
            counter += 1
        
        new_tag = {
            "id": slug,
            "name": name,
            "color": data.get('color', '#00FF00')
        }
        
        tags.append(new_tag)
        
        if save_json_file(TAGS_FILE, tags):
            return jsonify({"success": True, "tag": new_tag})
        else:
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
            
    except Exception as e:
        logger.error(f"Erreur création tag: {e}")
        return jsonify({"error": f"Erreur lors de la création: {str(e)}"}), 500

@app.route('/api/categories/update', methods=['POST'])
@require_auth
def update_category():
    """Mettre à jour une catégorie existante"""
    try:
        data = request.get_json()
        category_id = data.get('id')
        name = data.get('name')
        color = data.get('color')
        
        if not category_id or not name:
            return jsonify({"error": "ID et nom requis"}), 400
            
        categories = load_json_file(CATEGORIES_FILE, [])
        
        for i, cat in enumerate(categories):
            if cat['id'] == category_id:
                categories[i]['name'] = name
                categories[i]['color'] = color
                break
        else:
            return jsonify({"error": "Catégorie non trouvée"}), 404
        
        if save_json_file(CATEGORIES_FILE, categories):
            return jsonify({"success": True, "message": "Catégorie mise à jour"})
        else:
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la mise à jour: {str(e)}"}), 500

@app.route('/api/categories/delete', methods=['POST'])
@require_auth
def delete_category():
    """Supprimer une catégorie"""
    try:
        data = request.get_json()
        category_id = data.get('id')
        
        if not category_id:
            return jsonify({"error": "ID requis"}), 400
            
        categories = load_json_file(CATEGORIES_FILE, [])
        categories = [cat for cat in categories if cat['id'] != category_id]
        
        if save_json_file(CATEGORIES_FILE, categories):
            return jsonify({"success": True, "message": "Catégorie supprimée"})
        else:
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la suppression: {str(e)}"}), 500

@app.route('/api/tags/update', methods=['POST'])
@require_auth
def update_tag():
    """Mettre à jour un tag existant"""
    try:
        data = request.get_json()
        tag_id = data.get('id')
        name = data.get('name')
        color = data.get('color')
        
        if not tag_id or not name:
            return jsonify({"error": "ID et nom requis"}), 400
            
        tags = load_json_file(TAGS_FILE, [])
        
        for i, tag in enumerate(tags):
            if tag['id'] == tag_id:
                tags[i]['name'] = name
                tags[i]['color'] = color
                break
        else:
            return jsonify({"error": "Tag non trouvé"}), 404
        
        if save_json_file(TAGS_FILE, tags):
            return jsonify({"success": True, "message": "Tag mis à jour"})
        else:
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la mise à jour: {str(e)}"}), 500

@app.route('/api/tags/delete', methods=['POST'])
@require_auth
def delete_tag():
    """Supprimer un tag"""
    try:
        data = request.get_json()
        tag_id = data.get('id')
        
        if not tag_id:
            return jsonify({"error": "ID requis"}), 400
            
        tags = load_json_file(TAGS_FILE, [])
        tags = [tag for tag in tags if tag['id'] != tag_id]
        
        jerseys = load_json_file(JERSEYS_FILE, [])
        for jersey in jerseys:
            if 'tags' in jersey and isinstance(jersey['tags'], list):
                jersey['tags'] = [t for t in jersey['tags'] if t != tag_id]
        
        if save_json_file(TAGS_FILE, tags) and save_json_file(JERSEYS_FILE, jerseys):
            return jsonify({"success": True, "message": "Tag supprimé"})
        else:
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la suppression: {str(e)}"}), 500

@app.route('/api/jerseys', methods=['POST'])
@require_auth
def save_jerseys_bulk():
    """Sauvegarder tous les maillots en masse"""
    try:
        data = request.get_json()
        jerseys = data.get('jerseys', [])
        
        if not jerseys:
            return jsonify({'error': 'Aucun maillot fourni'}), 400
        
        if save_json_file(JERSEYS_FILE, jerseys):
            return jsonify({'success': True, 'message': f'{len(jerseys)} maillots sauvegardés'})
        else:
            return jsonify({'error': 'Erreur sauvegarde'}), 500
        
    except Exception as e:
        logger.error(f"Erreur save_jerseys: {e}")
        return jsonify({'error': str(e)}), 500

# Route temporaire pour télécharger les images (démo uniquement)
@app.route('/api/admin/download-images', methods=['POST'])
@require_auth
def download_images():
    """Télécharge les images manquantes depuis les URLs dans jerseys.json"""
    try:
        import subprocess
        import sys
        
        # Lancer le script de téléchargement
        script_path = os.path.join(os.path.dirname(__file__), 'download_images.py')
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max
        )
        
        logger.info(f"Script download_images terminé: {result.returncode}")
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Téléchargement des images lancé avec succès',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Erreur lors du téléchargement',
                'output': result.stderr
            }), 500
            
    except Exception as e:
        logger.error(f"Erreur download_images: {e}")
        return jsonify({'error': str(e)}), 500


# Gestion des erreurs
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erreur interne: {error}")
    return jsonify({"error": "Internal server error"}), 500

# Servir les fichiers statiques en production
@app.route('/')
def serve_index():
    return send_from_directory(os.path.dirname(os.path.dirname(__file__)), 'index.html')

@app.route('/login')
def serve_login():
    return send_from_directory(os.path.dirname(os.path.dirname(__file__)), 'login.html')

@app.route('/admin')
def serve_admin():
    return send_from_directory(os.path.dirname(os.path.dirname(__file__)), 'admin_production.html')

@app.route('/merci')
def serve_merci():
    return send_from_directory(os.path.dirname(os.path.dirname(__file__)), 'merci.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.dirname(os.path.dirname(__file__)), filename)

if __name__ == '__main__':
    # S'assurer que les dossiers existent
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Charger/créer la configuration
    config = load_config()
    
    logger.info("🚀 Démarrage du serveur de production FC Palestina")
    logger.info(f"📁 Dossier données: {DATA_DIR}")
    logger.info(f"🔐 Authentification activée")
    
    # Démarrer le serveur
    port = int(os.environ.get('PORT', 8001))
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Backend Flask démarré sur le port {port}")
    print(f"📱 API disponible sur: http://localhost:{port}/api/")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        threaded=True
    )