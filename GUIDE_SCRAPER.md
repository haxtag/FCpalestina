# 🏆 Guide du Scraper Yupoo FC Palestina

## 🚀 Démarrage Rapide

### 1. **Installation des Dépendances**
```bash
# Installer les dépendances Python
pip install -r scripts/requirements.txt
```

### 2. **Test du Scraper**
```bash
# Tester le scraper
python run_scraper.py
# Choisir l'option 1 pour tester
```

### 3. **Lancement du Scraping**
```bash
# Lancer le scraping complet
python run_scraper.py
# Choisir l'option 2 pour scraper
```

## 📋 Options Disponibles

### **Option 1: Test du Scraper**
- Vérifie la connexion à Yupoo
- Teste l'extraction des liens d'albums
- Teste l'extraction des données d'un maillot

### **Option 2: Scraping Complet**
- Scrape les albums Yupoo
- Extrait les images et données
- Sauvegarde dans `data/jerseys.json`

### **Option 3: Données de Démonstration**
- Crée des maillots de test
- Permet de tester le site sans Yupoo

### **Option 4: Installation des Dépendances**
- Installe automatiquement les packages Python nécessaires

## 🔧 Configuration

### **URL Yupoo**
Par défaut: `https://shixingtiyu.x.yupoo.com`

Pour changer l'URL:
1. Lancez le scraper
2. Entrez votre URL Yupoo personnalisée

### **Nombre de Pages**
- Défaut: 3 pages
- Recommandé: 2-5 pages pour commencer
- Maximum: 10 pages (pour éviter d'être bloqué)

## 📁 Fichiers Générés

### **data/jerseys.json**
Contient tous les maillots extraits avec:
- Titre et description
- Images et miniatures
- Catégorie et tags
- Métadonnées (année, vues, etc.)

### **yupoo_scraper.log**
Logs détaillés du scraping:
- Connexions réussies/échouées
- Albums traités
- Erreurs rencontrées

## 🛠️ Dépannage

### **Erreur de Connexion**
```
❌ Erreur de connexion: [Errno 11001] getaddrinfo failed
```
**Solution:**
- Vérifiez votre connexion internet
- Vérifiez que l'URL Yupoo est correcte
- Essayez avec une autre URL Yupoo

### **Aucun Album Trouvé**
```
⚠️ Aucun album trouvé sur la page 1
```
**Solutions:**
- Vérifiez que l'URL pointe vers une page d'albums
- Essayez avec une URL différente
- Vérifiez que le site Yupoo est accessible

### **Erreur d'Installation**
```
❌ Erreur lors de l'installation: [Errno 2] No such file or directory
```
**Solutions:**
- Assurez-vous que Python est installé
- Utilisez `python3` au lieu de `python`
- Installez pip: `python -m ensurepip --upgrade`

### **Images Non Affichées**
**Solutions:**
1. Vérifiez que les images sont dans `assets/images/jerseys/`
2. Vérifiez les chemins dans `data/jerseys.json`
3. Rechargez la page web

## 🎯 Utilisation Avancée

### **Scraping Personnalisé**
```python
from scripts.yupoo_scraper import YupooSpecializedScraper

# Créer le scraper
scraper = YupooSpecializedScraper("https://votre-site.yupoo.com")

# Scraper 5 pages
jerseys = scraper.scrape_albums(max_pages=5)

# Sauvegarder
scraper.save_jerseys("data/mes_maillots.json")
```

### **Filtrage des Maillots**
```python
# Filtrer par catégorie
home_jerseys = [j for j in jerseys if j['category'] == 'home']

# Filtrer par année
jerseys_2024 = [j for j in jerseys if j['year'] == 2024]
```

### **Mise à Jour Automatique**
```python
# Utiliser le script de mise à jour
python scripts/update_data.py start
```

## 📊 Monitoring

### **Vérifier les Logs**
```bash
# Voir les logs en temps réel
tail -f yupoo_scraper.log

# Voir les dernières erreurs
grep "ERROR" yupoo_scraper.log
```

### **Statistiques**
```python
import json

# Charger les données
with open('data/jerseys.json', 'r') as f:
    jerseys = json.load(f)

# Statistiques
print(f"Total maillots: {len(jerseys)}")
print(f"Catégories: {set(j['category'] for j in jerseys)}")
print(f"Années: {set(j['year'] for j in jerseys)}")
```

## 🔒 Bonnes Pratiques

### **Respect des Sites**
- Utilisez des délais entre les requêtes
- Ne scrapez pas trop de pages d'un coup
- Respectez les conditions d'utilisation

### **Gestion des Erreurs**
- Vérifiez toujours les logs
- Testez d'abord avec peu de pages
- Gardez des sauvegardes des données

### **Performance**
- Limitez le nombre d'images par maillot
- Compressez les images si nécessaire
- Utilisez le cache du navigateur

## 🆘 Support

### **Problèmes Courants**
1. **Site ne se charge pas**: Vérifiez que le serveur local fonctionne
2. **Pas de maillots**: Lancez le scraper ou créez des données de démo
3. **Erreurs JavaScript**: Vérifiez la console du navigateur (F12)

### **Logs Utiles**
- `yupoo_scraper.log`: Logs du scraper
- Console du navigateur: Erreurs JavaScript
- Terminal: Erreurs Python

---

**🎯 Le scraper est maintenant prêt ! Lancez `python run_scraper.py` pour commencer.**
