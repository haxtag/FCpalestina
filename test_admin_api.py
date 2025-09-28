#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour l'API d'administration
"""

import requests
import json

def test_api():
    base_url = "http://localhost:8001/api"
    
    print("🧪 Test de l'API d'administration...")
    
    try:
        # Test des catégories
        print("\n📂 Test des catégories...")
        response = requests.get(f"{base_url}/categories")
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Catégories récupérées: {len(categories)}")
            for cat in categories:
                print(f"  - {cat['name']} ({cat['id']})")
        else:
            print(f"❌ Erreur catégories: {response.status_code}")
        
        # Test des tags
        print("\n🏷️ Test des tags...")
        response = requests.get(f"{base_url}/tags")
        if response.status_code == 200:
            tags = response.json()
            print(f"✅ Tags récupérés: {len(tags)}")
            for tag in tags:
                print(f"  - {tag['name']} ({tag['id']})")
        else:
            print(f"❌ Erreur tags: {response.status_code}")
        
        # Test des maillots
        print("\n👕 Test des maillots...")
        response = requests.get(f"{base_url}/jerseys")
        if response.status_code == 200:
            jerseys = response.json()
            print(f"✅ Maillots récupérés: {len(jerseys)}")
            for jersey in jerseys[:3]:  # Afficher seulement les 3 premiers
                print(f"  - {jersey['name']} ({jersey['id']})")
        else:
            print(f"❌ Erreur maillots: {response.status_code}")
        
        print("\n🎉 Tests terminés!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au backend admin sur le port 8001")
        print("💡 Assurez-vous que le backend est lancé avec: python start_admin_backend.py")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    test_api()