#!/usr/bin/env python3
"""
Scraper Yupoo optimisé avec déduplication pour FC Palestina
Version améliorée qui évite l'importation de doublons
"""

import json
import os
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional

# Configuration
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
BACKUP_DIR = DATA_DIR / "backups"
JERSEYS_FILE = DATA_DIR / "jerseys.json"

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / 'yupoo_deduplication.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class JerseyDeduplicator:
    """Système de déduplication des maillots"""
    
    def __init__(self):
        self.existing_jerseys: List[Dict] = []
        self.existing_signatures: Set[str] = set()
        self.load_existing_jerseys()
    
    def load_existing_jerseys(self) -> None:
        """Charger les maillots existants"""
        try:
            if JERSEYS_FILE.exists():
                with open(JERSEYS_FILE, 'r', encoding='utf-8') as f:
                    self.existing_jerseys = json.load(f)
                
                # Créer les signatures pour la déduplication
                for jersey in self.existing_jerseys:
                    signature = self.create_jersey_signature(jersey)
                    self.existing_signatures.add(signature)
                
                logger.info(f"📄 {len(self.existing_jerseys)} maillots existants chargés")
                logger.info(f"🔑 {len(self.existing_signatures)} signatures créées")
            else:
                logger.info("📄 Aucun fichier jerseys.json existant - nouveau catalogue")
                
        except Exception as e:
            logger.error(f"❌ Erreur chargement jerseys existants: {e}")
            self.existing_jerseys = []
            self.existing_signatures = set()
    
    def create_jersey_signature(self, jersey: Dict) -> str:
        """Créer une signature unique pour un maillot"""
        # Normaliser le titre
        title = self.normalize_title(jersey.get('title', ''))
        
        # Normaliser la catégorie
        category = jersey.get('category', 'home').lower()
        
        # Année
        year = str(jersey.get('year', '2024'))
        
        # Créer une signature basée sur ces éléments
        signature_text = f"{title}|{category}|{year}".lower()
        
        # Hasher pour obtenir une signature courte
        signature = hashlib.md5(signature_text.encode('utf-8')).hexdigest()[:12]
        
        return signature
    
    def normalize_title(self, title: str) -> str:
        """Normaliser un titre pour la comparaison"""
        if not title:
            return "maillot"
        
        # Convertir en minuscules
        normalized = title.lower()
        
        # Supprimer les caractères spéciaux et espaces multiples
        import re
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)
        normalized = normalized.strip()
        
        # Remplacer les synonymes
        synonyms = {
            'fc palestina': 'palestina',
            'palestine fc': 'palestina',
            'palestine': 'palestina',
            'maillot': '',
            'jersey': '',
            'shirt': '',
            'kit': '',
            'tshirt': '',
            't-shirt': '',
        }
        
        for synonym, replacement in synonyms.items():
            normalized = normalized.replace(synonym, replacement)
        
        # Nettoyer les espaces
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized or "maillot"
    
    def is_duplicate(self, new_jersey: Dict) -> Optional[Dict]:
        """Vérifier si un maillot est un doublon"""
        new_signature = self.create_jersey_signature(new_jersey)
        
        # Vérification par signature
        if new_signature in self.existing_signatures:
            # Trouver le maillot existant
            for existing in self.existing_jerseys:
                if self.create_jersey_signature(existing) == new_signature:
                    return existing
        
        # Vérification par titre similaire
        new_title_normalized = self.normalize_title(new_jersey.get('title', ''))
        
        for existing in self.existing_jerseys:
            existing_title_normalized = self.normalize_title(existing.get('title', ''))
            
            # Si les titres normalisés sont très similaires
            if self.are_titles_similar(new_title_normalized, existing_title_normalized):
                # Et même catégorie/année
                if (existing.get('category') == new_jersey.get('category') and
                    existing.get('year') == new_jersey.get('year')):
                    return existing
        
        return None
    
    def are_titles_similar(self, title1: str, title2: str, threshold: float = 0.8) -> bool:
        """Vérifier si deux titres sont similaires"""
        if not title1 or not title2:
            return False
        
        # Calcul de similarité simple
        words1 = set(title1.split())
        words2 = set(title2.split())
        
        if not words1 or not words2:
            return False
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        similarity = intersection / union if union > 0 else 0
        
        return similarity >= threshold
    
    def merge_jersey_data(self, existing: Dict, new_jersey: Dict) -> Dict:
        """Fusionner les données de deux maillots similaires"""
        merged = existing.copy()
        
        # Mettre à jour la date de modification
        merged['updated_at'] = datetime.now().isoformat()
        
        # Fusionner les images (éviter les doublons)
        existing_images = set(existing.get('images', []))
        new_images = set(new_jersey.get('images', []))
        all_images = list(existing_images | new_images)
        
        if all_images:
            merged['images'] = all_images
            # Mettre à jour la thumbnail si nécessaire
            if not merged.get('thumbnail') and new_jersey.get('thumbnail'):
                merged['thumbnail'] = new_jersey['thumbnail']
        
        # Fusionner les tags
        existing_tags = set(existing.get('tags', []))
        new_tags = set(new_jersey.get('tags', []))
        merged['tags'] = list(existing_tags | new_tags)
        
        # Mettre à jour les URLs source
        source_urls = []
        if existing.get('source_url'):
            source_urls.append(existing['source_url'])
        if new_jersey.get('source_url'):
            source_urls.append(new_jersey['source_url'])
        
        if source_urls:
            merged['source_urls'] = list(set(source_urls))
        
        return merged
    
    def add_jersey(self, new_jersey: Dict) -> bool:
        """Ajouter un maillot en évitant les doublons"""
        # Vérifier si c'est un doublon
        existing = self.is_duplicate(new_jersey)
        
        if existing:
            logger.info(f"🔄 Doublon détecté: '{new_jersey.get('title')}' -> Fusion avec maillot existant")
            
            # Fusionner les données
            merged = self.merge_jersey_data(existing, new_jersey)
            
            # Remplacer dans la liste
            for i, jersey in enumerate(self.existing_jerseys):
                if self.create_jersey_signature(jersey) == self.create_jersey_signature(existing):
                    self.existing_jerseys[i] = merged
                    break
            
            return False  # Pas d'ajout, mais fusion
        
        else:
            logger.info(f"✅ Nouveau maillot: '{new_jersey.get('title')}'")
            
            # Ajouter le nouveau maillot
            self.existing_jerseys.append(new_jersey)
            signature = self.create_jersey_signature(new_jersey)
            self.existing_signatures.add(signature)
            
            return True  # Nouveau ajout
    
    def save_jerseys(self) -> bool:
        """Sauvegarder les maillots"""
        try:
            # Créer une sauvegarde si le fichier existe
            if JERSEYS_FILE.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = BACKUP_DIR / f"jerseys_backup_{timestamp}.json"
                BACKUP_DIR.mkdir(exist_ok=True)
                
                import shutil
                shutil.copy2(JERSEYS_FILE, backup_file)
                logger.info(f"💾 Sauvegarde créée: {backup_file.name}")
            
            # Sauvegarder le nouveau fichier
            DATA_DIR.mkdir(exist_ok=True)
            with open(JERSEYS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.existing_jerseys, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ {len(self.existing_jerseys)} maillots sauvegardés")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde: {e}")
            return False

class YupooDeduplicationScraper:
    """Scraper Yupoo avec déduplication intégrée"""
    
    def __init__(self):
        self.deduplicator = JerseyDeduplicator()
        self.stats = {
            'processed': 0,
            'new_added': 0,
            'duplicates_merged': 0,
            'errors': 0
        }
    
    def process_jerseys_from_scraper(self, scraped_jerseys: List[Dict]) -> Dict:
        """Traiter une liste de maillots scrapés"""
        logger.info(f"🔍 Traitement de {len(scraped_jerseys)} maillots scrapés...")
        
        for jersey in scraped_jerseys:
            try:
                self.stats['processed'] += 1
                
                # Ajouter le maillot (avec déduplication)
                is_new = self.deduplicator.add_jersey(jersey)
                
                if is_new:
                    self.stats['new_added'] += 1
                else:
                    self.stats['duplicates_merged'] += 1
                
            except Exception as e:
                logger.error(f"❌ Erreur traitement maillot: {e}")
                self.stats['errors'] += 1
        
        # Sauvegarder les résultats
        if self.deduplicator.save_jerseys():
            logger.info("💾 Sauvegarde réussie")
        else:
            logger.error("❌ Erreur sauvegarde")
        
        return self.get_stats()
    
    def get_stats(self) -> Dict:
        """Obtenir les statistiques de traitement"""
        return {
            **self.stats,
            'total_jerseys': len(self.deduplicator.existing_jerseys),
            'success_rate': (self.stats['processed'] - self.stats['errors']) / max(1, self.stats['processed'])
        }
    
    def print_summary(self) -> None:
        """Afficher le résumé"""
        stats = self.get_stats()
        
        logger.info("=" * 50)
        logger.info("📊 RÉSUMÉ DE L'IMPORT YUPOO")
        logger.info("=" * 50)
        logger.info(f"🔍 Maillots traités: {stats['processed']}")
        logger.info(f"✅ Nouveaux ajoutés: {stats['new_added']}")
        logger.info(f"🔄 Doublons fusionnés: {stats['duplicates_merged']}")
        logger.info(f"❌ Erreurs: {stats['errors']}")
        logger.info(f"📊 Total dans le catalogue: {stats['total_jerseys']}")
        logger.info(f"✅ Taux de succès: {stats['success_rate']:.1%}")
        logger.info("=" * 50)

def main():
    """Test de déduplication"""
    logger.info("🧪 Test du système de déduplication")
    
    # Créer des maillots de test
    test_jerseys = [
        {
            'id': 'test1',
            'title': 'Maillot FC Palestina Domicile 2024',
            'category': 'home',
            'year': '2024',
            'images': ['https://example.com/image1.jpg'],
            'tags': ['home', 'palestina']
        },
        {
            'id': 'test2', 
            'title': 'FC Palestina Home Jersey 2024',  # Similaire au premier
            'category': 'home',
            'year': '2024',
            'images': ['https://example.com/image2.jpg'],
            'tags': ['home', 'fc palestina']
        },
        {
            'id': 'test3',
            'title': 'Maillot Palestine Extérieur 2024',
            'category': 'away',
            'year': '2024',
            'images': ['https://example.com/image3.jpg'],
            'tags': ['away', 'palestina']
        }
    ]
    
    # Traiter avec déduplication
    scraper = YupooDeduplicationScraper()
    scraper.process_jerseys_from_scraper(test_jerseys)
    scraper.print_summary()

if __name__ == "__main__":
    main()