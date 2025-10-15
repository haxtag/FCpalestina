# 🚀 Guide de Déploiement FC Palestina

## 📋 Préparation du Projet

### 1. Nettoyage du Projet
```bash
# Nettoyer les fichiers de développement
python clean_project.py
```

### 2. Import des Maillots Yupoo (RECOMMANDÉ EN LOCAL)

⚠️ **IMPORTANT**: Faire l'import Yupoo **AVANT** le déploiement

```bash
# Tester d'abord la connexion
python scripts/test_scraper.py

# Lancer l'import complet (peut prendre 15-30 minutes)
python scripts/yupoo_scraper.py
```

**Pourquoi en local ?**
- ✅ Connexion internet stable
- ✅ Pas de limitations serveur
- ✅ Peut déboguer facilement
- ✅ Évite les timeouts hébergeur

## 🌐 Déploiement sur Hébergeur

### Option 1: Hébergeur avec Python (Recommandé)

**Hébergeurs supportant Python:**
- **PythonAnywhere** (gratuit avec limitations)
- **Heroku** (payant maintenant)
- **DigitalOcean App Platform**
- **Railway**
- **Render** (gratuit tier disponible)

#### Structure à uploader:
```
FCpalestina/
├── index.html                 # Page principale
├── admin.html                # Interface admin
├── assets/                   # CSS, JS, images
├── data/                     # JSON avec maillots importés
├── scripts/
│   ├── simple_backend.py     # API Flask
│   ├── requirements.txt      # Dépendances Python
│   └── yupoo_scraper.py      # Pour maintenance
└── run_scraper.py           # Scripts utilitaires
```

#### Commandes déploiement:
```bash
# 1. Installer dépendances
pip install -r scripts/requirements.txt

# 2. Lancer le backend
python scripts/simple_backend.py

# 3. Servir les fichiers statiques (selon hébergeur)
```

### Option 2: Hébergeur Statique + API Externe

**Hébergeurs statiques:**
- **Netlify** (gratuit)
- **Vercel** (gratuit)
- **GitHub Pages**
- **Surge.sh**

#### Configuration:
1. **Frontend**: Déployer `index.html` + `assets/` + `data/`
2. **Backend**: Déployer `scripts/simple_backend.py` séparément
3. **Modifier** `assets/js/config.js` avec nouvelle URL API

## ⚙️ Configuration Production

### 1. Modifier les URLs dans `assets/js/config.js`
```javascript
const CONFIG = {
    API_BASE_URL: 'https://votre-api.herokuapp.com',  // URL de votre API
    IMAGES_BASE_URL: 'assets/images/jerseys'
};
```

### 2. Variables d'environnement (si applicable)
```bash
# Pour hébergeurs cloud
FLASK_ENV=production
PORT=5000
```

## 🔧 Maintenance Post-Déploiement

### Ajouter de nouveaux maillots:
```bash
# En local seulement
python scripts/yupoo_scraper.py

# Puis re-uploader data/jerseys.json
```

### Backup automatique:
- Les backups se créent automatiquement dans `data/backups/`
- Télécharger régulièrement ces fichiers

## 🎯 Checklist de Déploiement

### Avant déploiement:
- [ ] ✅ Scraper testé et fonctionnel
- [ ] ✅ Import Yupoo terminé (100+ maillots)
- [ ] ✅ Projet nettoyé (`clean_project.py`)
- [ ] ✅ Admin testé localement
- [ ] ✅ Pagination fonctionnelle (12/page)
- [ ] ✅ Modal réparé
- [ ] ✅ Mode sombre opérationnel

### Après déploiement:
- [ ] ✅ Site accessible
- [ ] ✅ Images chargent correctement
- [ ] ✅ Admin fonctionne
- [ ] ✅ Sauvegarde opérationnelle
- [ ] ✅ Responsif mobile
- [ ] ✅ Modes clair/sombre

## 📞 Contact et Support

### Liens utiles:
- **TikTok**: [@maillots.du.peuple](https://www.tiktok.com/@maillots.du.peuple)
- **Vinted**: [fc.palestina](https://www.vinted.fr/member/223176724)

### Fichiers essentiels à sauvegarder:
1. `data/jerseys.json` (maillots)
2. `data/categories.json` (catégories)
3. `data/tags.json` (tags)
4. `assets/images/jerseys/` (images)

---
🏆 **Bon déploiement FC Palestina!** 🇵🇸