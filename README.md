# FC Palestina - Portfolio de Maillots

Portfolio web pour la collection de maillots FC Palestina avec galerie interactive et système d'importation automatique.

## Aperçu

Site vitrine présentant une collection de maillots de football avec :
- Galerie filtrable par catégorie
- Recherche en temps réel
- Avis clients (Vinted)
- Interface admin pour gestion du contenu

## Installation

```bash
# Cloner le repo
git clone https://github.com/haxtag/MaillotsDuPeuple.git
cd MaillotsDuPeuple

# Installer les dépendances Python
pip install -r scripts/requirements.txt

# Lancer le site
python launch_site.py
```

Le site sera accessible sur `http://localhost:8000`

## Structure

```
MaillotsDuPeuple/
├── assets/           # CSS, JS, images
├── data/            # Données JSON (maillots, avis)
├── scripts/         # Scripts Python (scraping, imports)
└── index.html       # Page principale
```

## Fonctionnalités

### Galerie
- Filtres par catégorie (Domicile, Extérieur, Vintage...)
- Recherche dynamique
- Tri personnalisable
- Modal de visualisation détaillée

### Import automatique
Le scraper récupère les maillots depuis Yupoo :

```bash
python scripts/yupoo_scraper_complet.py --limit 50
```

Options disponibles :
- `--limit N` : Limiter à N maillots
- `--fresh` : Import complet (écrase les données)

### Avis clients
Import des avis depuis Vinted :

```bash
python scripts/complete_vinted_scraper.py
```

## Administration

Interface admin accessible via `http://localhost:8000/admin_production.html`

Fonctionnalités :
- Ajout/modification/suppression de maillots
- Upload d'images
- Gestion des catégories et tags
- Vue d'ensemble des statistiques

## Configuration

### Chemins d'images
Modifier `assets/js/config.js` :

```javascript
window.CONFIG = {
    IMAGES_BASE_URL: '/assets/images/jerseys'
};
```

### Backend API
Le backend Flask tourne sur le port 8001 :
- `GET /api/jerseys` - Liste des maillots
- `POST /api/jerseys` - Ajouter un maillot
- `PUT /api/jerseys/:id` - Modifier
- `DELETE /api/jerseys/:id` - Supprimer

## Technologies

- **Frontend** : HTML, CSS (vanilla), JavaScript (ES6+)
- **Backend** : Python + Flask
- **Scraping** : BeautifulSoup, Requests
- **Stockage** : JSON (backups automatiques)

## Notes

- Les backups sont créés automatiquement dans `data/backups/`
- Les images sont téléchargées en haute qualité uniquement
- Barcelone et Real Madrid sont exclus de l'import

## License

Projet personnel - FC Palestina
