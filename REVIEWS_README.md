# 🌟 Système d'Avis - FC Palestina

## Vue d'ensemble

Le système d'avis permet de collecter, afficher et gérer les avis clients de manière automatique et élégante.

## 🚀 Fonctionnalités

### ✅ Scraper Vinted
- **Fichier**: `scripts/vinted_reviews_scraper.py`
- **Fonction**: Récupère les avis depuis le profil Vinted
- **Fallback**: Avis de démonstration si le scraping échoue
- **Format**: Sauvegarde en JSON dans `data/reviews.json`

### ✅ Section Reviews Complète
- **Navigation**: Bouton "Avis" ajouté entre "À Propos" et "Contact"
- **Affichage**: Grille responsive avec pagination (6 avis par page)
- **Statistiques**: Moyenne des notes et nombre total d'avis
- **Design**: Cartes avec animations et thème rose

### ✅ Carousel d'Avis (Section About)
- **Remplacement**: L'image de la section About est remplacée par un carousel
- **Animation**: Défilement automatique toutes les 4 secondes
- **Contenu**: Affiche aléatoirement les avis avec étoiles

## 📁 Structure des Fichiers

```
├── scripts/
│   └── vinted_reviews_scraper.py    # Scraper principal
├── assets/
│   ├── css/components/
│   │   └── reviews.css              # Styles pour les avis
│   └── js/modules/
│       └── reviews.js               # Logique JavaScript
├── data/
│   └── reviews.json                 # Base de données des avis
├── test_reviews.html                # Page de test
└── manage_reviews.py               # Script de gestion
```

## 🎨 Design

### Couleurs
- **Accent**: Rose (#ff69b4) pour cohérence avec le thème
- **Étoiles**: Jaune doré (#ffc107)
- **Cartes**: Arrière-plan avec bordures subtiles

### Responsive
- **Desktop**: Grille de 3 colonnes
- **Tablet**: Grille de 2 colonnes  
- **Mobile**: Grille de 1 colonne

### Animations
- **Cartes**: Apparition en fondu avec décalage
- **Hover**: Élévation et bordure colorée
- **Carousel**: Transition fluide entre avis

## 🔧 Utilisation

### Scraper les Avis
```bash
python scripts/vinted_reviews_scraper.py
```

### Test Rapide
```bash
python manage_reviews.py
```

### Ouvrir Page de Test
- Double-cliquer sur `test_reviews.html`
- Ou utiliser le gestionnaire: `python manage_reviews.py` → option 3

## 📊 Format des Données

### Structure JSON (`data/reviews.json`)
```json
{
  "reviews": [
    {
      "id": "review-1",
      "text": "Excellent service!",
      "rating": 5,
      "author": "Sophie_M",
      "date": "il y a 5 jours"
    }
  ],
  "total_count": 8,
  "last_updated": "2024-09-28T23:31:27",
  "source": "Vinted",
  "profile_url": "https://www.vinted.fr/member/287196181-maillotsdupeuple?tab=feedback"
}
```

## 🛠️ Configuration

### Nombre d'Avis par Page
Dans `assets/js/modules/reviews.js`:
```javascript
this.reviewsPerPage = 6; // Modifier ici
```

### Vitesse du Carousel
Dans `assets/js/modules/reviews.js`:
```javascript
this.carouselInterval = setInterval(() => {
    this.nextCarouselReview();
}, 4000); // Modifier le délai ici (ms)
```

## 🎯 Intégration

### Navigation
Le bouton "Avis" est automatiquement ajouté à:
- Menu de navigation principal
- Footer (liens rapides)

### JavaScript
Le module se charge automatiquement:
```javascript
document.addEventListener('DOMContentLoaded', () => {
    reviewsManager = new ReviewsManager();
});
```

## 🚨 Gestion d'Erreurs

### Scraper
- **Timeout réseau**: 30 secondes
- **Échec de parsing**: Avis de démonstration
- **Anti-bot**: User-agents aléatoires et délais

### Frontend
- **Fichier manquant**: Avis de fallback
- **Erreur réseau**: Gestion gracieuse
- **DOM non trouvé**: Vérifications de sécurité

## 📱 Compatibilité

- **Navigateurs**: Chrome, Firefox, Safari, Edge
- **Thèmes**: Clair et sombre
- **Responsive**: Mobile, tablette, desktop
- **JavaScript**: ES6+ avec fallbacks

## 🔄 Mise à Jour

### Nouveaux Avis
1. Exécuter le scraper: `python scripts/vinted_reviews_scraper.py`
2. Les avis sont automatiquement mis à jour sur le site
3. Le carousel et les statistiques se mettent à jour

### Maintenance
- **Logs**: Consultez `vinted_reviews_scraper.log`
- **Backup**: Les anciens avis sont conservés
- **Test**: Utilisez `test_reviews.html` pour vérifier

---

🎉 **Le système d'avis est maintenant entièrement fonctionnel et intégré au site FC Palestina!**