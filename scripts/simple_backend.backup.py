#!/usr/bin/env python3
"""
Backend Flask simple pour l'administration FC Palestine
"""

import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

# Configuration
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
JERSEYS_FILE = os.path.join(DATA_DIR, 'jerseys.json')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.json')
TAGS_FILE = os.path.join(DATA_DIR, 'tags.json')

# Créer l'application Flask
app = Flask(__name__)
CORS(app)  # Autoriser les requêtes cross-origin

def load_json_file(filepath, default=[]):
    """Charger un fichier JSON ou retourner une valeur par défaut"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    except Exception as e:
        print(f"❌ Erreur lors du chargement de {filepath}: {e}")
        return default

def save_json_file(filepath, data):
    """Sauvegarder des données dans un fichier JSON"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde de {filepath}: {e}")
        return False

@app.route('/api/jerseys', methods=['GET'])
def get_jerseys():
    """Récupérer tous les maillots"""
    jerseys = load_json_file(JERSEYS_FILE, [])
    return jsonify(jerseys)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Récupérer toutes les catégories"""
    categories = load_json_file(CATEGORIES_FILE, [
        {"id": "cat_1", "name": "Domicile", "color": "#8B1538"},
        {"id": "cat_2", "name": "Extérieur", "color": "#000000"},
        {"id": "cat_3", "name": "Spéciaux", "color": "#FFD700"}
    ])
    return jsonify(categories)

@app.route('/api/tags', methods=['GET'])
def get_tags():
    """Récupérer tous les tags"""
    tags = load_json_file(TAGS_FILE, [
        {"id": "tag_1", "name": "Nouveau", "color": "#00FF00"},
        {"id": "tag_2", "name": "Populaire", "color": "#FF6B6B"},
        {"id": "tag_3", "name": "Limité", "color": "#FFD700"}
    ])
    return jsonify(tags)

@app.route('/api/jerseys/update', methods=['POST'])
def update_jersey():
    """Mettre à jour un maillot"""
    try:
        data = request.get_json()
        print(f"🔍 Données reçues: {data}")
        
        jersey_id = data.get('jersey_id')
        print(f"🔍 Jersey ID: {jersey_id}")
        
        if not jersey_id:
            print("❌ jersey_id manquant")
            return jsonify({"error": "jersey_id manquant"}), 400
        
        # Charger les maillots existants
        jerseys = load_json_file(JERSEYS_FILE, [])
        
        # Trouver et mettre à jour le maillot
        updated = False
        for i, jersey in enumerate(jerseys):
            if jersey.get('id') == jersey_id:
                # Mettre à jour les champs
                jerseys[i].update({
                    'name': data.get('name', jersey.get('name', '')),
                    'title': data.get('name', jersey.get('title', '')),
                    'description': data.get('description', jersey.get('description', '')),
                    'category': data.get('category', jersey.get('category', '')),
                    'categories': data.get('categories', jersey.get('categories', [])),
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
        
        # Sauvegarder
        if save_json_file(JERSEYS_FILE, jerseys):
            return jsonify({"success": True, "message": "Maillot mis à jour"})
        else:
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la mise à jour: {str(e)}"}), 500

@app.route('/api/jerseys/update-cover', methods=['POST'])
def update_cover():
    """Mettre à jour l'image de couverture d'un maillot"""
    try:
        data = request.get_json()
        jersey_id = data.get('jersey_id')
        cover_image = data.get('cover_image')
        
        if not jersey_id or not cover_image:
            return jsonify({"error": "jersey_id et cover_image requis"}), 400
        
        # Charger les maillots existants
        jerseys = load_json_file(JERSEYS_FILE, [])
        
        # Trouver et mettre à jour le maillot
        updated = False
        for i, jersey in enumerate(jerseys):
            if jersey.get('id') == jersey_id:
                jerseys[i]['thumbnail'] = cover_image
                jerseys[i]['updated_at'] = datetime.now().isoformat()
                updated = True
                break
        
        if not updated:
            return jsonify({"error": "Maillot non trouvé"}), 404
        
        # Sauvegarder
        if save_json_file(JERSEYS_FILE, jerseys):
            return jsonify({"success": True, "message": "Image de couverture mise à jour"})
        else:
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la mise à jour: {str(e)}"}), 500

@app.route('/api/categories/create', methods=['POST'])
def create_category():
    """Créer une nouvelle catégorie"""
    try:
        data = request.get_json()
        categories = load_json_file(CATEGORIES_FILE, [])
        
        new_category = {
            "id": f"cat_{len(categories) + 1}",
            "name": data.get('name', ''),
            "color": data.get('color', '#8B1538')
        }
        
        categories.append(new_category)
        
        if save_json_file(CATEGORIES_FILE, categories):
            return jsonify({"success": True, "category": new_category})
        else:
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la création: {str(e)}"}), 500

@app.route('/api/tags/create', methods=['POST'])
def create_tag():
    """Créer un nouveau tag"""
    try:
        data = request.get_json()
        tags = load_json_file(TAGS_FILE, [])
        
        new_tag = {
            "id": f"tag_{len(tags) + 1}",
            "name": data.get('name', ''),
            "color": data.get('color', '#00FF00')
        }
        
        tags.append(new_tag)
        
        if save_json_file(TAGS_FILE, tags):
            return jsonify({"success": True, "tag": new_tag})
        else:
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la création: {str(e)}"}), 500

@app.route('/api/categories/update', methods=['POST'])
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
def delete_tag():
    """Supprimer un tag"""
    try:
        data = request.get_json()
        tag_id = data.get('id')
        
        if not tag_id:
            return jsonify({"error": "ID requis"}), 400
            
        # Charger et supprimer le tag
        tags = load_json_file(TAGS_FILE, [])
        tags = [tag for tag in tags if tag['id'] != tag_id]
        
        # Nettoyer les maillots (retirer ce tag de tous les maillots)
        jerseys = load_json_file(JERSEYS_FILE, [])
        for jersey in jerseys:
            if 'tags' in jersey and isinstance(jersey['tags'], list):
                jersey['tags'] = [t for t in jersey['tags'] if t != tag_id]
        
        # Sauvegarder les deux fichiers
        if save_json_file(TAGS_FILE, tags) and save_json_file(JERSEYS_FILE, jerseys):
            return jsonify({"success": True, "message": "Tag supprimé"})
        else:
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la suppression: {str(e)}"}), 500

@app.route('/api/jerseys', methods=['POST'])
def save_jerseys():
    """Sauvegarder tous les maillots"""
    try:
        data = request.get_json()
        jerseys = data.get('jerseys', [])
        
        if not jerseys:
            return jsonify({'error': 'Aucun maillot fourni'}), 400
        
        # Sauvegarder
        save_json_file(JERSEYS_FILE, jerseys)
        
        return jsonify({'success': True, 'message': f'{len(jerseys)} maillots sauvegardés'})
        
    except Exception as e:
        print(f"❌ Erreur save_jerseys: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Backend Flask démarré sur le port 8001")
    print("📱 API disponible sur: http://localhost:8001/api/")
    app.run(host='0.0.0.0', port=8001, debug=True)
