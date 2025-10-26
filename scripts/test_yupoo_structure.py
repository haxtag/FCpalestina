#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour analyser la structure HTML d'une page Yupoo
et trouver les bons sélecteurs pour l'image de couverture
"""

import requests
from bs4 import BeautifulSoup
import json

def analyze_yupoo_page(url):
    """Analyse la structure HTML d'une page album Yupoo"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"\n🔍 Analyse de: {url}\n")
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print("=" * 80)
    print("ANALYSE DES IMAGES")
    print("=" * 80)
    
    # Trouver toutes les balises img
    all_images = soup.find_all('img')
    print(f"\n📊 Total d'images trouvées: {len(all_images)}\n")
    
    for i, img in enumerate(all_images[:10], 1):  # Afficher les 10 premières
        src = img.get('src') or img.get('data-src') or img.get('data-original')
        classes = img.get('class', [])
        parent = img.parent
        parent_classes = parent.get('class', []) if parent else []
        
        print(f"\n--- Image {i} ---")
        print(f"  URL: {src[:100] if src else 'None'}...")
        print(f"  Classes img: {classes}")
        print(f"  Parent: {parent.name if parent else 'None'}")
        print(f"  Classes parent: {parent_classes}")
        
        # Remonter la hiérarchie
        if parent:
            grandparent = parent.parent
            if grandparent:
                print(f"  Grand-parent: {grandparent.name}")
                print(f"  Classes grand-parent: {grandparent.get('class', [])}")
    
    print("\n" + "=" * 80)
    print("ANALYSE DES DIV AVEC CLASSES 'COVER', 'ALBUM', 'HEADER', 'THUMB'")
    print("=" * 80)
    
    # Chercher des divs spécifiques
    keywords = ['cover', 'album', 'header', 'thumb', 'showalbum', 'photo']
    for keyword in keywords:
        elements = soup.find_all(class_=lambda x: x and keyword in x.lower())
        if elements:
            print(f"\n🎯 Éléments avec '{keyword}' dans la classe: {len(elements)}")
            for elem in elements[:3]:
                print(f"  - {elem.name}.{elem.get('class')}")
                # Chercher des images dans cet élément
                imgs_in_elem = elem.find_all('img')
                if imgs_in_elem:
                    print(f"    └─ Contient {len(imgs_in_elem)} image(s)")
                    for img in imgs_in_elem[:2]:
                        src = img.get('src') or img.get('data-src')
                        print(f"       └─ {src[:80] if src else 'No src'}...")
    
    print("\n" + "=" * 80)
    print("STRUCTURE DU TITRE ET ZONE ADJACENTE")
    print("=" * 80)
    
    # Trouver le titre
    title_selectors = ['h1', '.album-title', '.showalbum__title', 'title']
    for selector in title_selectors:
        title_elem = soup.select_one(selector)
        if title_elem:
            print(f"\n✅ Titre trouvé avec: {selector}")
            print(f"   Texte: {title_elem.get_text().strip()}")
            
            # Chercher les éléments suivants (siblings)
            next_sibling = title_elem.find_next_sibling()
            if next_sibling:
                print(f"   Sibling suivant: {next_sibling.name}.{next_sibling.get('class')}")
                imgs = next_sibling.find_all('img')
                if imgs:
                    print(f"   └─ Contient {len(imgs)} image(s)")
            
            # Chercher dans le parent
            parent = title_elem.parent
            if parent:
                print(f"   Parent: {parent.name}.{parent.get('class')}")
                imgs_in_parent = parent.find_all('img')
                if imgs_in_parent:
                    print(f"   └─ Parent contient {len(imgs_in_parent)} image(s)")
                    for img in imgs_in_parent[:2]:
                        src = img.get('src') or img.get('data-src')
                        print(f"      └─ {src[:80] if src else 'No src'}...")
            break
    
    print("\n" + "=" * 80)
    print("RECHERCHE IMAGES HAUTE QUALITÉ")
    print("=" * 80)
    
    # Images avec 'photo' dans l'URL (haute qualité Yupoo)
    photo_images = []
    for img in all_images:
        src = img.get('src') or img.get('data-src') or img.get('data-original')
        if src and 'photo' in src.lower():
            photo_images.append({
                'src': src,
                'classes': img.get('class', []),
                'parent_class': img.parent.get('class', []) if img.parent else []
            })
    
    print(f"\n📸 Images avec 'photo' dans l'URL: {len(photo_images)}")
    for i, img_data in enumerate(photo_images[:5], 1):
        print(f"\n  {i}. {img_data['src'][:100]}...")
        print(f"     Classes: {img_data['classes']}")
        print(f"     Parent: {img_data['parent_class']}")

if __name__ == '__main__':
    # Test avec l'URL fournie
    test_url = "https://shixingtiyu.x.yupoo.com/albums/214566765?uid=1&isSubCate=false&referrercate="
    
    try:
        analyze_yupoo_page(test_url)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
