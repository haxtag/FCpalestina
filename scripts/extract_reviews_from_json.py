#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extracteur d'avis Vinted depuis les données JavaScript embarquées
"""

import json
import re
import logging
from pathlib import Path
import sys

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('extract_reviews_json.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def extract_javascript_data(html_content):
    """Extrait les données JavaScript de la page HTML"""
    logger.info("🔍 Recherche des données JavaScript...")
    
    # Patterns pour trouver les données JSON
    patterns = [
        r'__NEXT_DATA__["\']?\s*:\s*({.+?})\s*[,}]',
        r'window\.__NEXT_DATA__\s*=\s*({.+?});',
        r'self\.__next_f\.push\(\[1,\s*"([^"]+)"\]\)',
        r'"feedback"[^}]*}[^}]*}',
        r'"user_feedbacks?"[^}]*{[^}]*}',
        r'"reviews?"[^}]*{[^}]*}',
    ]
    
    all_data = []
    
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
        if matches:
            logger.info(f"✅ Pattern trouvé: {pattern[:50]}... - {len(matches)} matches")
            all_data.extend(matches)
    
    return all_data

def search_feedback_data(html_content):
    """Recherche spécifiquement les données de feedback"""
    logger.info("🎯 Recherche spécifique des données de feedback...")
    
    # Chercher des patterns spécifiques aux avis
    feedback_patterns = [
        r'"feedback[s]?"[^{]*{[^}]*"[^"]*"[^}]*}',
        r'"review[s]?"[^{]*{[^}]*"[^"]*"[^}]*}',
        r'"rating"[^:]*:[^,]*,',
        r'"comment"[^:]*:[^,}]*[,}]',
        r'"user"[^{]*{[^}]*"username"[^,}]*[,}]',
        r'rosiecol3|sosso3440|stunning|qualité',
        r'"14[^"]*évaluations?"',
    ]
    
    results = {}
    
    for pattern in feedback_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE | re.MULTILINE)
        if matches:
            results[pattern[:30]] = matches
            logger.info(f"📝 Pattern '{pattern[:30]}...' trouvé {len(matches)} fois")
    
    return results

def analyze_json_structure(data_string):
    """Analyse la structure JSON pour trouver les avis"""
    logger.info(f"🔬 Analyse de la structure JSON...")
    
    try:
        # Essayer de décoder le JSON
        if data_string.startswith('"') and data_string.endswith('"'):
            # C'est probablement une string encodée
            data_string = json.loads(data_string)
        
        data = json.loads(data_string)
        
        # Chercher récursivement les avis
        def find_reviews_recursive(obj, path=""):
            results = []
            
            if isinstance(obj, dict):
                # Chercher des clés liées aux avis
                review_keys = ['feedback', 'feedbacks', 'review', 'reviews', 'rating', 'comment', 'user_feedback']
                
                for key in review_keys:
                    if key in obj:
                        results.append(f"Trouvé '{key}' dans {path}")
                        logger.info(f"🎯 Clé '{key}' trouvée: {path}.{key}")
                
                # Continuer la recherche récursive
                for key, value in obj.items():
                    if key.lower() in ['feedback', 'review', 'rating', 'user'] or 'feedback' in key.lower():
                        results.extend(find_reviews_recursive(value, f"{path}.{key}"))
                    elif isinstance(value, (dict, list)) and len(str(value)) > 100:  # Seulement les gros objets
                        results.extend(find_reviews_recursive(value, f"{path}.{key}"))
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, (dict, list)):
                        results.extend(find_reviews_recursive(item, f"{path}[{i}]"))
            
            return results
        
        return find_reviews_recursive(data)
    
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'analyse JSON: {e}")
        return []

def main():
    """Fonction principale"""
    logger.info("🚀 Démarrage de l'extraction d'avis depuis les données JSON...")
    
    # Charger le fichier HTML
    html_file = Path("debug_vinted_page.html")
    if not html_file.exists():
        logger.error("❌ Fichier debug_vinted_page.html introuvable")
        return
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        logger.info(f"📄 Fichier HTML chargé: {len(html_content)} caractères")
        
        # 1. Extraire les données JavaScript
        js_data = extract_javascript_data(html_content)
        logger.info(f"📦 {len(js_data)} structures JavaScript trouvées")
        
        # 2. Recherche spécifique des feedbacks
        feedback_data = search_feedback_data(html_content)
        
        if feedback_data:
            logger.info("📋 Données de feedback trouvées:")
            for pattern, matches in feedback_data.items():
                logger.info(f"  - {pattern}: {len(matches)} matches")
                for match in matches[:3]:  # Afficher les 3 premiers
                    logger.info(f"    • {match[:100]}...")
        
        # 3. Analyser les structures JSON
        all_results = []
        for i, data in enumerate(js_data[:5]):  # Analyser les 5 premiers
            logger.info(f"🔍 Analyse de la structure {i+1}/{min(5, len(js_data))}...")
            results = analyze_json_structure(data)
            all_results.extend(results)
        
        if all_results:
            logger.info("✅ Résultats de l'analyse:")
            for result in all_results:
                logger.info(f"  📌 {result}")
        else:
            logger.warning("⚠️ Aucune structure de feedback trouvée dans les données JSON")
        
        # 4. Recherche directe des noms d'utilisateurs
        logger.info("🔎 Recherche directe des utilisateurs mentionnés...")
        usernames = ['rosiecol3', 'sosso3440']
        for username in usernames:
            if username in html_content:
                logger.info(f"✅ Utilisateur '{username}' trouvé dans le HTML!")
                # Extraire le contexte
                pos = html_content.find(username)
                context = html_content[max(0, pos-200):pos+200]
                logger.info(f"📝 Contexte: ...{context}...")
            else:
                logger.info(f"❌ Utilisateur '{username}' non trouvé")
        
        # 5. Recherche des termes d'avis
        review_terms = ['stunning', 'qualité', 'recommande']
        for term in review_terms:
            count = html_content.lower().count(term.lower())
            if count > 0:
                logger.info(f"✅ Terme '{term}' trouvé {count} fois")
                # Extraire quelques contextes
                pos = html_content.lower().find(term.lower())
                if pos != -1:
                    context = html_content[max(0, pos-100):pos+100]
                    logger.info(f"📝 Contexte: ...{context}...")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du traitement: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()