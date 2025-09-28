# 🔐 Administration FC Palestina

## 📋 Accès à l'interface d'administration

### 🌐 URL d'accès
```
http://localhost:8001/admin-login.html
```

### 🔑 Identifiants de connexion
- **Nom d'utilisateur:** `admin`
- **Mot de passe:** `fcpalestina2024`

## 🚀 Démarrage du serveur d'administration

### Option 1: Script automatique (Windows)
```bash
# Double-cliquez sur le fichier
start_admin.bat

# Ou en ligne de commande
start_admin.ps1
```

### Option 2: Commande manuelle
```bash
python scripts/admin_server.py 8001
```

## 🛠️ Fonctionnalités d'administration

### 📊 Tableau de bord
- **Statistiques en temps réel** : nombre de maillots, catégories, vues totales
- **Vue d'ensemble** de tous les maillots avec overlay d'administration

### ✏️ Gestion des maillots

#### Modifier un maillot existant
1. **Survoler** un maillot pour voir les options d'administration
2. **Cliquer sur "Modifier"** pour ouvrir l'éditeur
3. **Modifier** les informations :
   - Titre
   - Description
   - Catégorie (Domicile, Extérieur, Gardien, Édition Spéciale)
   - Année
   - Tags (séparés par des virgules)
4. **Sauvegarder** les modifications

#### Changer l'image de couverture
1. **Survoler** un maillot
2. **Cliquer sur "Image"** pour voir toutes les images disponibles
3. **Cliquer sur une image** pour la sélectionner comme couverture
4. **L'image est automatiquement sauvegardée**

#### Ajouter un nouveau maillot
1. **Cliquer sur "Ajouter"** dans la barre d'administration
2. **Remplir** les informations du maillot
3. **Sauvegarder** pour créer le maillot

#### Supprimer un maillot
1. **Survoler** un maillot
2. **Cliquer sur "Supprimer"** (bouton rouge)
3. **Confirmer** la suppression

### 🏷️ Gestion des catégories
Les catégories disponibles sont :
- **Domicile** : Maillots à domicile
- **Extérieur** : Maillots extérieur
- **Gardien** : Maillots de gardien
- **Édition Spéciale** : Maillots spéciaux/commémoratifs

### 🏷️ Gestion des tags
- **Format** : séparés par des virgules
- **Exemples** : `home, FC Palestina, officiel, 2024`
- **Utilisation** : filtrage et recherche sur le site

## 🔧 Configuration technique

### 📁 Structure des fichiers
```
FCpalestina/
├── admin-login.html          # Page de connexion
├── admin.html               # Interface d'administration
├── scripts/
│   ├── admin_server.py      # Serveur API d'administration
│   └── optimize_cover_images.py  # Optimisation des images
├── data/
│   └── jerseys.json         # Base de données des maillots
└── assets/images/jerseys/   # Images des maillots
```

### 🌐 Ports utilisés
- **Site principal** : `http://localhost:8000`
- **Administration** : `http://localhost:8001`

### 🔒 Sécurité
- **Connexion requise** pour accéder à l'administration
- **Session** stockée dans le navigateur
- **Déconnexion automatique** si la session expire

## 📱 Interface utilisateur

### 🎨 Design
- **Interface moderne** avec overlay d'administration
- **Responsive** : fonctionne sur mobile et desktop
- **Intuitive** : survol pour voir les options

### ⌨️ Raccourcis
- **Échap** : fermer les modals
- **Clic extérieur** : fermer les modals
- **Actualiser** : recharger les données

## 🚨 Dépannage

### ❌ Problèmes courants

#### "Page non trouvée"
- Vérifiez que le serveur d'administration est démarré
- Vérifiez l'URL : `http://localhost:8001/admin-login.html`

#### "Connexion refusée"
- Vérifiez les identifiants : `admin` / `fcpalestina2024`
- Videz le cache du navigateur
- Vérifiez la console pour les erreurs

#### "Modifications non sauvegardées"
- Vérifiez que le fichier `data/jerseys.json` est accessible en écriture
- Vérifiez la console pour les erreurs
- Redémarrez le serveur d'administration

### 🔍 Logs et débogage
- **Console du navigateur** : F12 → Console
- **Logs du serveur** : affichés dans le terminal
- **Fichiers de données** : `data/jerseys.json`

## 📞 Support

Pour toute question ou problème :
1. Vérifiez cette documentation
2. Consultez les logs d'erreur
3. Vérifiez la configuration des ports
4. Redémarrez les serveurs si nécessaire

---

**🎉 Bonne administration de votre site FC Palestina !**
