#!/usr/bin/env python3
"""
Script de traduction des noms de maillots chinois vers français
"""

import json
import os
from datetime import datetime

def translate_jersey_names():
    """Traduit les noms de maillots chinois vers français"""
    
    print("Traduction des noms de maillots chinois vers français")
    print("=" * 50)
    
    # Dictionnaire de traduction
    translations = {
        # Équipes
        '德国': 'Allemagne',
        '阿贾克斯': 'Ajax',
        '切尔西': 'Chelsea',
        '曼联': 'Manchester United',
        '洛杉矶': 'Los Angeles',
        '富勒姆': 'Fulham',
        '伯恩茅斯': 'Bournemouth',
        '朴茨茅斯': 'Portsmouth',
        
        # Types de maillots
        '主': 'Domicile',
        '客': 'Extérieur',
        '守门员': 'Gardien',
        '特别版': 'Édition Spéciale',
        '纪念版': 'Édition Commémorative',
        '涂鸦': 'Graffiti',
        '二客': 'Deuxième Extérieur',
        
        # Couleurs
        '黑': 'Noir',
        '白': 'Blanc',
        '红': 'Rouge',
        '蓝': 'Bleu',
        '绿': 'Vert',
        '黄': 'Jaune',
        '粉': 'Rose',
        
        # Autres
        '带星星': 'Avec Étoiles',
        '不带星星': 'Sans Étoiles',
        '反光标': 'Réfléchissant',
        '女神': 'Déesse',
        '耶稣': 'Jésus',
        '深绿': 'Vert Foncé',
        '白彩兰': 'Blanc Bleu',
        '三色': 'Tricolore',
        '正确版': 'Version Correcte',
        '周年': 'Anniversaire',
        '125': '125ème',
        '又拍图片管家': '',  # Supprimer ce texte
    }
    
    # Lire le fichier jerseys.json
    try:
        with open('data/jerseys.json', 'r', encoding='utf-8') as f:
            jerseys = json.load(f)
        
        print(f"Chargement de {len(jerseys)} maillots...")
        
        # Traduire chaque maillot
        for jersey in jerseys:
            original_title = jersey['title']
            translated_title = translate_title(original_title, translations)
            
            # Mettre à jour le titre et la description
            jersey['title'] = translated_title
            jersey['description'] = f"Maillot officiel FC Palestina - {translated_title}"
            
            print(f"  {original_title} → {translated_title}")
        
        # Sauvegarder les modifications
        with open('data/jerseys.json', 'w', encoding='utf-8') as f:
            json.dump(jerseys, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ {len(jerseys)} maillots traduits et sauvegardés !")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def translate_title(title, translations):
    """Traduit un titre en utilisant le dictionnaire de traduction"""
    
    translated = title
    
    # Appliquer les traductions
    for chinese, french in translations.items():
        if chinese in translated:
            translated = translated.replace(chinese, french)
    
    # Nettoyer le texte
    translated = translated.replace('  ', ' ')  # Supprimer les espaces doubles
    translated = translated.replace('S-4XL', 'Taille S-4XL')
    translated = translated.replace('S-2XL', 'Taille S-2XL')
    translated = translated.strip()
    
    # Si le titre est vide ou trop court, utiliser un titre par défaut
    if len(translated) < 5:
        translated = "Maillot FC Palestina"
    
    return translated

def main():
    """Fonction principale"""
    
    print("Traduction des noms de maillots")
    print("=" * 30)
    
    success = translate_jersey_names()
    
    if success:
        print("\n🎉 Traduction terminée !")
        print("Rechargez votre site pour voir les noms traduits")
    else:
        print("\n❌ Traduction échouée")

if __name__ == "__main__":
    main()
