# 🏆 Portfolio FC Palestina

Un portfolio moderne et professionnel pour la collection de maillots FC Palestina, avec synchronisation automatique depuis Yupoo.

## ✨ Fonctionnalités

### 🎨 Interface Utilisateur
- **Design moderne et responsive** - S'adapte à tous les écrans
- **Galerie interactive** - Filtres par catégorie, recherche, tri
- **Modal de visualisation** - Affichage détaillé des maillots
- **Animations fluides** - Transitions et effets visuels
- **Navigation intuitive** - Menu responsive et navigation fluide

### 🔧 Fonctionnalités Techniques
- **Synchronisation automatique** - Mise à jour depuis Yupoo
- **Système de cache** - Performance optimisée
- **Lazy loading** - Chargement progressif des images
- **API REST** - Gestion des données des maillots
- **Responsive design** - Compatible mobile/tablet/desktop

### 📱 Responsive Design
- **Mobile First** - Optimisé pour les appareils mobiles
- **Breakpoints adaptatifs** - 480px, 768px, 1200px, 1400px
- **Navigation tactile** - Support des gestes tactiles
- **Images optimisées** - Différentes tailles selon l'écran

## 🚀 Installation

### Prérequis
- Python 3.8+
- Navigateur web moderne
- Serveur web (Apache, Nginx, ou serveur de développement)

### Installation des dépendances

```bash
# Installer les dépendances Python
pip install -r scripts/requirements.txt

# Ou avec pip3
pip3 install -r scripts/requirements.txt
```

### Configuration

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd FCpalestina
```

2. **Configurer le scraper**
```python
# Modifier scripts/scraper.py
BASE_URL = "https://shixingtiyu.x.yupoo.com"  # Votre URL Yupoo
```

3. **Lancer le serveur**
```bash
# Serveur Python simple
python -m http.server 8000

# Ou avec Node.js
npx serve .

# Ou avec PHP
php -S localhost:8000
```

## 📁 Structure du Projet

```
FCpalestina/
├── 📁 assets/
│   ├── 📁 css/
│   │   ├── main.css              # Styles principaux
│   │   ├── 📁 components/        # Styles des composants
│   │   │   ├── header.css
│   │   │   ├── gallery.css
│   │   │   ├── modal.css
│   │   │   └── footer.css
│   │   └── responsive.css        # Media queries
│   ├── 📁 js/
│   │   ├── main.js              # Script principal
│   │   ├── 📁 modules/          # Modules JavaScript
│   │   │   ├── gallery.js
│   │   │   ├── modal.js
│   │   │   └── api.js
│   │   └── 📁 utils/            # Utilitaires
│   │       └── helpers.js
│   ├── 📁 images/
│   │   ├── 📁 jerseys/          # Images des maillots
│   │   ├── 📁 thumbnails/       # Miniatures
│   │   └── 📁 icons/            # Icônes
│   └── 📁 fonts/                # Polices personnalisées
├── 📁 data/
│   ├── jerseys.json             # Données des maillots
│   └── config.json              # Configuration
├── 📁 scripts/
│   ├── scraper.py               # Script de scraping Yupoo
│   ├── update_data.py           # Mise à jour automatique
│   └── requirements.txt         # Dépendances Python
├── index.html                   # Page principale
└── README.md                    # Documentation
```

## 🔄 Synchronisation avec Yupoo

### Scraping Manuel

```bash
# Mise à jour manuelle
python scripts/scraper.py

# Ou avec le script de mise à jour
python scripts/update_data.py update
```

### Synchronisation Automatique

```bash
# Démarrer le planificateur
python scripts/update_data.py start
```

Le système effectue automatiquement :
- **Mise à jour toutes les 2 heures**
- **Mise à jour quotidienne à 9h et 21h**
- **Détection des nouveaux maillots**
- **Fusion intelligente des données**

### Configuration du Scraper

```python
# Dans scripts/scraper.py
class YupooScraper:
    def __init__(self, base_url: str = "https://votre-site.yupoo.com"):
        self.base_url = base_url
        # Configuration des headers, délais, etc.
```

## 🎨 Personnalisation

### Couleurs et Thème

```css
/* Dans assets/css/main.css */
:root {
    --primary-color: #2c5530;      /* Couleur principale */
    --secondary-color: #d4af37;     /* Couleur secondaire */
    --accent-color: #ff6b35;        /* Couleur d'accent */
    /* ... autres variables */
}
```

### Ajout de Nouvelles Catégories

```javascript
// Dans assets/js/modules/api.js
getCategoryDisplayName(category) {
    const names = {
        'home': 'Domicile',
        'away': 'Extérieur',
        'special': 'Spéciaux',
        'vintage': 'Vintage',
        'keeper': 'Gardien',
        'nouvelle-categorie': 'Nouvelle Catégorie'  // Ajouter ici
    };
    return names[category] || category;
}
```

### Modification des Filtres

```html
<!-- Dans index.html -->
<div class="gallery-filters">
    <button class="filter-btn active" data-filter="all">Tous</button>
    <button class="filter-btn" data-filter="home">Domicile</button>
    <button class="filter-btn" data-filter="away">Extérieur</button>
    <button class="filter-btn" data-filter="special">Spéciaux</button>
    <button class="filter-btn" data-filter="vintage">Vintage</button>
    <!-- Ajouter de nouveaux filtres ici -->
</div>
```

## 📊 Gestion des Données

### Structure d'un Maillot

```json
{
    "id": "jersey-unique-id",
    "title": "Titre du maillot",
    "description": "Description détaillée",
    "category": "home|away|special|vintage|keeper",
    "year": 2024,
    "price": 89.99,
    "images": ["image1.jpg", "image2.jpg"],
    "thumbnail": "thumbnail.jpg",
    "tags": ["tag1", "tag2"],
    "date": "2024-01-15",
    "views": 1250,
    "featured": true,
    "source_url": "https://yupoo.com/album/...",
    "last_updated": "2024-01-15T10:30:00"
}
```

### Ajout Manuel de Maillots

```javascript
// Ajouter un maillot via l'API
const newJersey = {
    id: 'jersey-custom-1',
    title: 'Mon Maillot Personnalisé',
    description: 'Description du maillot',
    category: 'home',
    year: 2024,
    images: ['mon-maillot.jpg'],
    thumbnail: 'mon-maillot-thumb.jpg',
    tags: ['personnalisé', '2024'],
    date: new Date().toISOString(),
    views: 0,
    featured: false
};

// Ajouter à la galerie
jerseyAPI.addJersey(newJersey);
```

## 🚀 Déploiement

### Hébergement Statique

1. **Netlify/Vercel**
   - Connecter votre repository
   - Configuration automatique
   - Déploiement continu

2. **GitHub Pages**
   ```bash
   # Activer GitHub Pages dans les paramètres du repo
   # Le site sera disponible à : https://username.github.io/FCpalestina
   ```

3. **Serveur Web**
   ```bash
   # Copier les fichiers sur votre serveur
   scp -r . user@server:/var/www/html/
   ```

### Configuration du Serveur

```nginx
# Configuration Nginx
server {
    listen 80;
    server_name votre-domaine.com;
    root /var/www/html;
    index index.html;
    
    # Cache pour les assets
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Compression
    gzip on;
    gzip_types text/css application/javascript image/svg+xml;
}
```

## 🔧 Maintenance

### Mise à Jour Régulière

```bash
# Mise à jour des dépendances
pip install -r scripts/requirements.txt --upgrade

# Nettoyage du cache
rm -rf data/cache/*

# Redémarrage du scraper
python scripts/update_data.py update
```

### Monitoring

```bash
# Vérifier les logs
tail -f scraper.log
tail -f update.log

# Vérifier l'état du système
python scripts/update_data.py check
```

### Sauvegarde

```bash
# Sauvegarder les données
cp data/jerseys.json backup/jerseys-$(date +%Y%m%d).json

# Sauvegarder les images
tar -czf backup/images-$(date +%Y%m%d).tar.gz assets/images/
```

## 🐛 Dépannage

### Problèmes Courants

1. **Le scraper ne fonctionne pas**
   ```bash
   # Vérifier les dépendances
   pip install -r scripts/requirements.txt
   
   # Vérifier la connectivité
   python -c "import requests; print(requests.get('https://yupoo.com').status_code)"
   ```

2. **Images ne s'affichent pas**
   ```bash
   # Vérifier les permissions
   chmod -R 755 assets/images/
   
   # Vérifier les chemins
   ls -la assets/images/jerseys/
   ```

3. **JavaScript ne fonctionne pas**
   ```bash
   # Vérifier la console du navigateur
   # Ouvrir les outils de développement (F12)
   # Regarder l'onglet Console
   ```

### Logs et Debug

```javascript
// Activer le mode debug
localStorage.setItem('debug', 'true');

// Vérifier les données
console.log(jerseyAPI.getJerseys());

// Vérifier la galerie
console.log(gallery.getStats());
```

## 📈 Performance

### Optimisations

1. **Images**
   - Utiliser des formats modernes (WebP, AVIF)
   - Compresser les images
   - Lazy loading activé

2. **CSS/JS**
   - Minification en production
   - Compression gzip
   - Cache des assets

3. **Données**
   - Pagination des résultats
   - Cache intelligent
   - Mise à jour incrémentale

### Métriques

```javascript
// Vérifier les performances
performance.getEntriesByType('navigation')[0];

// Temps de chargement
console.log('Load time:', performance.now());
```

## 🤝 Contribution

### Comment Contribuer

1. Fork le projet
2. Créer une branche feature
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

### Guidelines

- Code en français (commentaires)
- Respecter la structure existante
- Tester vos modifications
- Documenter les nouvelles fonctionnalités

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- **FC Palestina** - Pour l'inspiration
- **Yupoo** - Pour la plateforme
- **Communauté Open Source** - Pour les outils utilisés

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/votre-repo/issues)
- **Email** : support@fcpalestina.com
- **Documentation** : [Wiki du projet](https://github.com/votre-repo/wiki)

---

**Fait avec ❤️ pour FC Palestina**
