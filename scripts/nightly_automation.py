#!/usr/bin/env python3
"""
Script d'automatisation nocturne pour FC Palestina
- Met à jour les avis Vinted chaque nuit
- Vérifie l'intégrité des données
- Crée des sauvegardes automatiques
"""

import os
import sys
import json
import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
DATA_DIR = BASE_DIR / "data"
BACKUP_DIR = DATA_DIR / "backups"
LOG_FILE = BASE_DIR / "automation.log"

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NightlyAutomation:
    def __init__(self):
        self.success_count = 0
        self.error_count = 0
        self.start_time = datetime.now()
        
    def run(self):
        """Exécute toutes les tâches nocturnes"""
        logger.info("=" * 50)
        logger.info("🌙 DÉMARRAGE AUTOMATISATION NOCTURNE")
        logger.info("=" * 50)
        
        try:
            # 1. Vérification des prérequis
            self.check_prerequisites()
            
            # 2. Sauvegarde préventive
            self.backup_data()
            
            # 3. Mise à jour des avis Vinted
            self.update_vinted_reviews()
            
            # 4. Nettoyage des anciens logs
            self.cleanup_old_files()
            
            # 5. Vérification de l'intégrité
            self.verify_data_integrity()
            
            # Résumé final
            self.print_summary()
            
        except Exception as e:
            logger.error(f"❌ Erreur critique dans l'automatisation: {e}")
            self.error_count += 1
    
    def check_prerequisites(self):
        """Vérifie que tous les fichiers nécessaires sont présents"""
        logger.info("🔍 Vérification des prérequis...")
        
        required_dirs = [DATA_DIR, BACKUP_DIR]
        for dir_path in required_dirs:
            if not dir_path.exists():
                logger.info(f"📁 Création du dossier: {dir_path}")
                dir_path.mkdir(parents=True, exist_ok=True)
        
        required_scripts = [
            SCRIPT_DIR / "complete_vinted_scraper.py",
        ]
        
        missing_scripts = []
        for script in required_scripts:
            if not script.exists():
                missing_scripts.append(script.name)
        
        if missing_scripts:
            logger.warning(f"⚠️ Scripts manquants: {', '.join(missing_scripts)}")
        else:
            logger.info("✅ Tous les scripts requis sont présents")
            self.success_count += 1
    
    def backup_data(self):
        """Crée une sauvegarde des données avant les mises à jour"""
        logger.info("💾 Création de la sauvegarde préventive...")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Sauvegarder les fichiers JSON principaux
            files_to_backup = [
                DATA_DIR / "jerseys.json",
                DATA_DIR / "reviews.json",
                DATA_DIR / "categories.json",
                BASE_DIR / "CONFIG_FILE"
            ]
            
            backup_count = 0
            for file_path in files_to_backup:
                if file_path.exists():
                    backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
                    backup_path = BACKUP_DIR / backup_name
                    
                    import shutil
                    shutil.copy2(file_path, backup_path)
                    logger.info(f"📁 Sauvegarde: {file_path.name} → {backup_name}")
                    backup_count += 1
            
            logger.info(f"✅ {backup_count} fichiers sauvegardés")
            self.success_count += 1
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde: {e}")
            self.error_count += 1
    
    def update_vinted_reviews(self):
        """Met à jour les avis Vinted"""
        logger.info("⭐ Mise à jour des avis Vinted...")
        
        try:
            vinted_scraper = SCRIPT_DIR / "complete_vinted_scraper.py"
            
            if not vinted_scraper.exists():
                logger.warning("⚠️ Script complete_vinted_scraper.py introuvable")
                return
            
            # Exécuter le scraper Vinted
            result = subprocess.run([
                sys.executable, str(vinted_scraper)
            ], 
            capture_output=True, 
            text=True, 
            timeout=300  # 5 minutes max
            )
            
            if result.returncode == 0:
                logger.info("✅ Avis Vinted mis à jour avec succès")
                
                # Vérifier le nombre d'avis importés
                reviews_file = DATA_DIR / "reviews.json"
                if reviews_file.exists():
                    with open(reviews_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        reviews_count = len(data.get('reviews', []))
                        logger.info(f"📊 Total avis Vinted: {reviews_count}")
                
                self.success_count += 1
            else:
                logger.error(f"❌ Erreur scraper Vinted: {result.stderr}")
                self.error_count += 1
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Timeout du scraper Vinted (5 minutes)")
            self.error_count += 1
        except Exception as e:
            logger.error(f"❌ Erreur mise à jour Vinted: {e}")
            self.error_count += 1
    
    def cleanup_old_files(self):
        """Nettoie les anciens fichiers de logs et sauvegardes"""
        logger.info("🧹 Nettoyage des anciens fichiers...")
        
        try:
            # Nettoyer les anciennes sauvegardes (garder 30 jours)
            cutoff_date = datetime.now() - timedelta(days=30)
            
            cleaned_count = 0
            if BACKUP_DIR.exists():
                for backup_file in BACKUP_DIR.glob("*_backup_*.json"):
                    if backup_file.stat().st_mtime < cutoff_date.timestamp():
                        backup_file.unlink()
                        cleaned_count += 1
            
            # Nettoyer les anciens logs
            for log_file in BASE_DIR.glob("*.log"):
                if log_file.name != "automation.log":  # Garder le log principal
                    if log_file.stat().st_mtime < cutoff_date.timestamp():
                        log_file.unlink()
                        cleaned_count += 1
            
            logger.info(f"🗑️ {cleaned_count} anciens fichiers supprimés")
            self.success_count += 1
            
        except Exception as e:
            logger.error(f"❌ Erreur nettoyage: {e}")
            self.error_count += 1
    
    def verify_data_integrity(self):
        """Vérifie l'intégrité des données JSON"""
        logger.info("🔍 Vérification de l'intégrité des données...")
        
        try:
            files_to_check = [
                DATA_DIR / "jerseys.json",
                DATA_DIR / "reviews.json",
                DATA_DIR / "categories.json"
            ]
            
            for file_path in files_to_check:
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                        if file_path.name == "jerseys.json":
                            if isinstance(data, list):
                                logger.info(f"✅ {file_path.name}: {len(data)} maillots")
                            else:
                                logger.warning(f"⚠️ {file_path.name}: format inattendu")
                                
                        elif file_path.name == "reviews.json":
                            reviews = data.get('reviews', [])
                            logger.info(f"✅ {file_path.name}: {len(reviews)} avis")
                            
                        else:
                            logger.info(f"✅ {file_path.name}: JSON valide")
                            
                    except json.JSONDecodeError as e:
                        logger.error(f"❌ {file_path.name}: JSON invalide - {e}")
                        self.error_count += 1
                        continue
                        
                else:
                    logger.info(f"ℹ️ {file_path.name}: fichier absent")
            
            self.success_count += 1
            
        except Exception as e:
            logger.error(f"❌ Erreur vérification intégrité: {e}")
            self.error_count += 1
    
    def print_summary(self):
        """Affiche le résumé de l'exécution"""
        duration = datetime.now() - self.start_time
        
        logger.info("=" * 50)
        logger.info("📊 RÉSUMÉ DE L'AUTOMATISATION NOCTURNE")
        logger.info("=" * 50)
        logger.info(f"⏱️ Durée: {duration}")
        logger.info(f"✅ Succès: {self.success_count}")
        logger.info(f"❌ Erreurs: {self.error_count}")
        
        if self.error_count == 0:
            logger.info("🎉 Automatisation terminée avec succès !")
        else:
            logger.warning(f"⚠️ Automatisation terminée avec {self.error_count} erreurs")
        
        logger.info("=" * 50)

def main():
    """Point d'entrée principal"""
    automation = NightlyAutomation()
    automation.run()

if __name__ == "__main__":
    main()