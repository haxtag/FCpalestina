#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic des avis Vinted - Vérification de l'intégrité des données
"""

import json
from pathlib import Path

def diagnose_reviews():
    print("🔍 DIAGNOSTIC DES AVIS VINTED")
    print("="*50)
    
    # Vérifier l'existence du fichier
    reviews_file = Path("data/reviews.json")
    if not reviews_file.exists():
        print("❌ Fichier reviews.json introuvable")
        return
    
    # Charger et analyser les données
    try:
        with open(reviews_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Fichier chargé avec succès")
        print(f"📊 Total des avis: {data.get('total_reviews', 0)}")
        print(f"🕐 Dernière mise à jour: {data.get('last_updated', 'Inconnue')}")
        print(f"🔗 Source: {data.get('source', 'Inconnue')}")
        print()
        
        reviews = data.get('reviews', [])
        if not reviews:
            print("❌ Aucun avis trouvé dans le fichier")
            return
        
        print(f"🎯 Analyse de {len(reviews)} avis:")
        print("-" * 30)
        
        for i, review in enumerate(reviews, 1):
            print(f"Avis #{i}:")
            print(f"  ID: {review.get('id', 'Manquant')}")
            print(f"  Utilisateur: {review.get('username', 'MANQUANT')}")
            print(f"  Commentaire: {review.get('comment', 'MANQUANT')}")
            print(f"  Note: {review.get('rating', 'Manquante')}/5")
            print(f"  Date: {review.get('date', 'Manquante')}")
            print(f"  Source: {review.get('source', 'Manquante')}")
            print()
        
        # Vérification de cohérence
        print("🧪 VÉRIFICATION DE COHÉRENCE:")
        print("-" * 30)
        
        issues = []
        
        for i, review in enumerate(reviews):
            if not review.get('username'):
                issues.append(f"Avis #{i+1}: Nom d'utilisateur manquant")
            if not review.get('comment'):
                issues.append(f"Avis #{i+1}: Commentaire manquant")
            if not review.get('rating'):
                issues.append(f"Avis #{i+1}: Note manquante")
        
        if issues:
            print("⚠️ Problèmes détectés:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("✅ Tous les avis ont des données complètes")
        
        print()
        print("💡 PREVIEW HTML:")
        print("-" * 30)
        
        # Générer un aperçu HTML des avis
        html_preview = []
        for review in reviews[:3]:  # Seulement les 3 premiers
            html_preview.append(f"""
<div class="avis">
  <div class="auteur">{review.get('username', 'Anonyme')}</div>
  <div class="commentaire">"{review.get('comment', 'Pas de commentaire')}"</div>
  <div class="meta">{review.get('rating', 0)}/5 ⭐ - {review.get('date', 'Date inconnue')}</div>
</div>""")
        
        for preview in html_preview:
            print(preview)
        
        print()
        print("🎉 DIAGNOSTIC TERMINÉ")
        
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    diagnose_reviews()