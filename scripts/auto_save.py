#!/usr/bin/env python3
"""
Script pour sauvegarder automatiquement les modifications des maillots
"""

import json
import os
import sys
from datetime import datetime

def save_jerseys_to_file(jerseys_data, backup=True):
    """Sauvegarde les données des maillots dans le fichier JSON"""
    try:
        # Chemin vers le fichier jerseys.json
        jerseys_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'jerseys.json')
        
        # Créer une sauvegarde si demandé
        if backup:
            backup_file = jerseys_file.replace('.json', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            if os.path.exists(jerseys_file):
                import shutil
                shutil.copy2(jerseys_file, backup_file)
                print(f"📁 Sauvegarde créée: {backup_file}")
        
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
            save_jerseys_to_file(jerseys_data)
        except json.JSONDecodeError as e:
            print(f"❌ Erreur de format JSON: {e}")
    else:
        print("Usage: python auto_save.py <json_data>")
