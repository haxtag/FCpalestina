#!/usr/bin/env python3
"""
Script de configuration pour la synchronisation Yupoo
"""

import json
import os

def setup_yupoo_config():
    """Configurer la synchronisation Yupoo"""
    
    print("🔧 Configuration de la synchronisation Yupoo")
    print("=" * 50)
    
    # Demander l'URL Yupoo
    yupoo_url = input("Entrez l'URL de votre site Yupoo (ex: https://shixingtiyu.x.yupoo.com): ").strip()
    
    if not yupoo_url:
        yupoo_url = "https://shixingtiyu.x.yupoo.com"
        print(f"URL par défaut utilisée: {yupoo_url}")
    
    # Créer le fichier de configuration
    config = {
        "yupoo": {
            "base_url": yupoo_url,
            "albums_url": f"{yupoo_url}/albums",
            "max_pages": 5,
            "delay_between_requests": 2
        },
        "scraping": {
            "enabled": True,
            "auto_update": True,
            "update_interval_hours": 2
        },
        "images": {
            "download_enabled": False,  # Désactivé par défaut pour éviter les problèmes de droits
            "save_path": "assets/images/jerseys",
            "thumbnail_size": [300, 300]
        }
    }
    
    # Sauvegarder la configuration
    with open('data/config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Configuration sauvegardée dans data/config.json")
    print(f"📡 URL Yupoo: {yupoo_url}")
    print(f"🔄 Mise à jour automatique: {'Activée' if config['scraping']['auto_update'] else 'Désactivée'}")
    
    # Tester la connexion
    print("\n🧪 Test de connexion...")
    try:
        import requests
        response = requests.get(yupoo_url, timeout=10)
        if response.status_code == 200:
            print("✅ Connexion réussie !")
        else:
            print(f"⚠️  Connexion réussie mais code de statut: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print("💡 Vérifiez que l'URL est correcte et accessible")
    
    print("\n📋 Prochaines étapes:")
    print("1. Vérifiez que l'URL Yupoo est correcte")
    print("2. Lancez le scraper: python scripts/scraper.py")
    print("3. Vérifiez les résultats dans data/jerseys.json")

if __name__ == "__main__":
    setup_yupoo_config()
