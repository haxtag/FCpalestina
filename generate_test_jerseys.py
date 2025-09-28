#!/usr/bin/env python3
"""
Générateur de maillots de test pour valider la pagination
"""

import json
import os
from datetime import datetime
import random

def generate_test_jerseys(count=25):
    """Génère des maillots de test pour valider la pagination"""
    
    jerseys = []
    
    # Types de maillots
    jersey_types = [
        {"name": "Domicile", "category": "home"},
        {"name": "Extérieur", "category": "away"},
        {"name": "Troisième", "category": "third"},
        {"name": "Gardien", "category": "keeper"},
        {"name": "Spécial", "category": "special"},
        {"name": "Vintage", "category": "vintage"}
    ]
    
    # Équipes et années pour variation
    teams = ["FC Palestina", "Palestine National", "Gaza United", "Westbank FC"]
    years = ["2020", "2021", "2022", "2023", "2024", "2025"]
    
    for i in range(count):
        jersey_type = random.choice(jersey_types)
        team = random.choice(teams)
        year = random.choice(years)
        
        jersey_id = f"test-jersey-{i+1:03d}"
        
        jersey = {
            "id": jersey_id,
            "title": f"{team} {jersey_type['name']} {year}",
            "name": f"{team} {jersey_type['name']} {year}",
            "description": f"Maillot {jersey_type['name'].lower()} officiel {team} saison {year}",
            "category": jersey_type["category"],
            "categories": [jersey_type["category"]],
            "year": year,
            "images": [
                f"{jersey_id}-hd-0.jpg",
                f"{jersey_id}-hd-1.jpg",
                f"{jersey_id}-hd-2.jpg"
            ],
            "thumbnail": f"{jersey_id}-hd-0.jpg",
            "price": None,
            "size": random.choice(["S-XL", "M-XXL", "L-2XL"]),
            "availability": True,
            "tags": [
                "fcpalestina",
                random.choice(["new", "popular", "classic"]),
                jersey_type["category"]
            ],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "source_url": f"https://test.com/album/{jersey_id}"
        }
        
        jerseys.append(jersey)
    
    return jerseys

def save_test_data():
    """Sauvegarde les données de test"""
    
    # Générer les maillots de test
    jerseys = generate_test_jerseys(25)  # 25 maillots pour tester pagination sur 2 pages
    
    # Chemin du fichier
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    jerseys_file = os.path.join(data_dir, 'jerseys.json')
    
    # Sauvegarder
    with open(jerseys_file, 'w', encoding='utf-8') as f:
        json.dump(jerseys, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(jerseys)} maillots de test générés dans {jerseys_file}")
    print(f"📄 Pagination attendue: {len(jerseys)} maillots = {(len(jerseys)-1)//20 + 1} pages (20 par page)")
    
    # Mettre à jour les catégories
    categories = [
        {"id": "home", "name": "Domicile", "description": "Maillots domicile"},
        {"id": "away", "name": "Extérieur", "description": "Maillots extérieur"},
        {"id": "third", "name": "Troisième", "description": "Troisièmes maillots"},
        {"id": "keeper", "name": "Gardien", "description": "Maillots de gardien"},
        {"id": "special", "name": "Spéciaux", "description": "Éditions spéciales"},
        {"id": "vintage", "name": "Vintage", "description": "Maillots vintage"}
    ]
    
    categories_file = os.path.join(data_dir, 'categories.json')
    with open(categories_file, 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(categories)} catégories mises à jour")
    
    # Mettre à jour les tags
    tags = [
        {"id": "fcpalestina", "name": "FC Palestina", "color": "#8B1538"},
        {"id": "new", "name": "Nouveau", "color": "#28a745"},
        {"id": "popular", "name": "Populaire", "color": "#007bff"},
        {"id": "classic", "name": "Classique", "color": "#6f42c1"},
        {"id": "home", "name": "Domicile", "color": "#8B1538"},
        {"id": "away", "name": "Extérieur", "color": "#6c757d"},
        {"id": "keeper", "name": "Gardien", "color": "#ffc107"}
    ]
    
    tags_file = os.path.join(data_dir, 'tags.json')
    with open(tags_file, 'w', encoding='utf-8') as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(tags)} tags mis à jour")
    print("\n🎯 PRÊT POUR LE TEST !")
    print("   1. Lance le backend: python scripts/simple_backend.py")
    print("   2. Lance le site: index.html")
    print("   3. Vérifie la pagination avec 25 maillots sur 2 pages")

if __name__ == "__main__":
    save_test_data()