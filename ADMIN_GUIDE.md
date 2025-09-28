# 🔧 Guide d'Administration FC Palestine

## 🚀 Démarrage du Système Admin

### 1. Lancer le Backend Admin
```bash
# Option 1: Script Python
python start_admin_backend.py

# Option 2: Script Batch (Windows)
start_admin_backend.bat

# Option 3: Direct
python scripts/admin_backend.py 8001
```

### 2. Lancer le Site Principal
```bash
python -m http.server 8000
```

### 3. Accéder au Mode Admin
- Ouvrir: `http://localhost:8000/?admin=true`
- Cliquer sur "🔧 Administration" dans la barre admin

## 🎯 Fonctionnalités Disponibles

### 📋 Gestion des Maillots
- **Voir tous les maillots** avec leurs informations
- **Modifier un maillot** :
  - Nom du maillot
  - Description détaillée
  - Catégorie (Domicile, Extérieur, etc.)
  - Année de sortie
  - Taille disponible
  - Prix
  - Tags associés
- **Changer l'image de couverture** :
  - Sélectionner parmi toutes les images du maillot
  - Prévisualisation en temps réel

### 🏷️ Gestion des Catégories
- **Créer une nouvelle catégorie** :
  - ID unique
  - Nom de la catégorie
  - Couleur d'affichage
- **Modifier une catégorie existante**
- **Supprimer une catégorie**

### 🏷️ Gestion des Tags
- **Créer un nouveau tag** :
  - ID unique
  - Nom du tag
  - Couleur d'affichage
- **Modifier un tag existant**
- **Supprimer un tag**

## 🔧 Interface Utilisateur

### Onglets Principaux
1. **Maillots** : Liste et édition des maillots
2. **Catégories** : Gestion des catégories
3. **Tags** : Gestion des tags

### Boutons d'Action
- **✏️ Modifier** : Éditer un élément
- **🖼️ Couverture** : Changer l'image de couverture
- **🗑️ Supprimer** : Supprimer un élément
- **💾 Sauvegarder** : Enregistrer les modifications
- **❌ Annuler** : Annuler les modifications

## 💾 Sauvegarde Automatique

### Backups
- **Sauvegarde automatique** avant chaque modification
- **Dossier de sauvegarde** : `data/backups/`
- **Format** : `{type}_backup_{timestamp}.json`

### Fichiers de Données
- **Maillots** : `data/jerseys.json`
- **Catégories** : `data/categories.json`
- **Tags** : `data/tags.json`

## 🌐 Compatibilité Hébergeur

### Configuration pour Production
1. **Modifier l'URL API** dans `assets/js/admin.js` :
   ```javascript
   this.apiBase = 'https://votre-domaine.com/api';
   ```

2. **Déployer le backend** sur votre hébergeur
3. **Configurer CORS** si nécessaire

### Serveur Web Requis
- **Python 3.6+** pour le backend
- **Serveur web** (Apache, Nginx) pour le frontend
- **Support des requêtes POST/PUT** pour l'API

## 🔒 Sécurité

### Accès Admin
- **URL secrète** : `?admin=true`
- **Pas de menu visible** pour les utilisateurs normaux
- **Backend séparé** sur port 8001

### Recommandations
- **Changer l'URL admin** en production
- **Ajouter une authentification** si nécessaire
- **Sauvegarder régulièrement** les données

## 🐛 Dépannage

### Problèmes Courants
1. **Backend non accessible** :
   - Vérifier que le port 8001 est libre
   - Vérifier les logs d'erreur

2. **Modifications non sauvegardées** :
   - Vérifier la connexion au backend
   - Vérifier les permissions d'écriture

3. **Images non affichées** :
   - Vérifier le chemin des images
   - Vérifier la configuration `CONFIG.IMAGES_BASE_URL`

### Logs
- **Backend** : Affichage dans la console
- **Frontend** : Console du navigateur (F12)

## 📞 Support

En cas de problème :
1. Vérifier les logs d'erreur
2. Tester la connexion API
3. Vérifier les permissions de fichiers
4. Redémarrer les serveurs

---

**🎉 Votre système d'administration est prêt !**
