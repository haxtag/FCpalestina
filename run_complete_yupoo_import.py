#!/usr/bin/env python3
"""
Script de lancement du scraper Yupoo pour import complet
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import logging

# Ajouter le répertoire scripts au path pour importer les modules
scripts_dir = Path(__file__).parent / "scripts"
sys.path.append(str(scripts_dir))

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import des modules avec gestion d'erreur améliorée
# Import simplifié sans erreurs
try:
    import subprocess
    import requests
    from bs4 import BeautifulSoup
    print("✅ Modules de base importés")
except ImportError as e:
    print(f"❌ Erreur import modules de base: {e}")
    sys.exit(1)

def run_complete_yupoo_import():
    """Lance l'import complet Yupoo avec déduplication"""
    print("🚀 IMPORT COMPLET YUPOO - FC PALESTINA")
    print("=" * 50)
    
    # Utiliser le script d'import simplifié qui fonctionne
    try:
        print("📡 Lancement du script d'import simplifié...")
        
        # Exécuter le script d'import qui fonctionne
        import_script = Path(__file__).parent / "import_yupoo_simple.py"
        
        if not import_script.exists():
            print("❌ Script import_yupoo_simple.py introuvable")
            return False
        
        # Exécuter le script
        result = subprocess.run([
            sys.executable, str(import_script)
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Import réussi !")
            print(result.stdout)
            
            # Vérifier le résultat
            data_dir = Path(__file__).parent / "data" 
            jerseys_file = data_dir / "jerseys.json"
            
            if jerseys_file.exists():
                with open(jerseys_file, 'r', encoding='utf-8') as f:
                    final_jerseys = json.load(f)
                
                print(f"📊 Total final: {len(final_jerseys)} maillots dans le catalogue")
                return len(final_jerseys) > 0
            else:
                print("⚠️ Fichier jerseys.json non trouvé")
                return False
        else:
            print("❌ Erreur lors de l'import:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur d'exécution: {e}")
        return False

if __name__ == "__main__":
    success = run_complete_yupoo_import()
    if success:
        print("\n🎉 Votre catalogue de maillots est prêt pour la production !")
    else:
        print("\n❌ L'import a échoué")
        sys.exit(1)