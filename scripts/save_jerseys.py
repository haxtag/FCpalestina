#!/usr/bin/env python3
"""
Script pour sauvegarder les modifications des maillots dans le fichier JSON
"""

import json
import sys
import os

def save_jerseys(jerseys_data):
    """Sauvegarde les données des maillots dans le fichier JSON"""
    try:
        # Chemin vers le fichier jerseys.json
        jerseys_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'jerseys.json')
        
        # Sauvegarder avec indentation pour la lisibilité
        with open(jerseys_file, 'w', encoding='utf-8') as f:
            json.dump(jerseys_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {len(jerseys_data)} maillots sauvegardés dans {jerseys_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Si des données JSON sont passées en argument
        try:
            jerseys_data = json.loads(sys.argv[1])
            save_jerseys(jerseys_data)
        except json.JSONDecodeError as e:
            print(f"❌ Erreur de format JSON: {e}")
    else:
        print("Usage: python save_jerseys.py <json_data>")
