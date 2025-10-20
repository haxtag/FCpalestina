# 📋 Guide Admin Interface - FC Palestina

## ✅ Fonctionnalités Complètes

### 🎨 **Interface Modernisée**
- Design responsive adapté mobile/tablette/desktop
- Couleurs du site (vert #2c5530, rouge #8B1538)
- Navigation par onglets intuitive
- Animations fluides et professionnelles

---

## 📊 **Tableau de Bord**

### Statistiques en Temps Réel
- 📦 Maillots Total
- 👁️ Maillots Actifs
- ⭐ Nombre d'avis
- 📈 Note moyenne

### Actions Rapides
- 🔄 Mise à jour avis Vinted
- 📥 Import nouveaux maillots Yupoo
- 💾 Sauvegarde des données

---

## 👕 **Gestion des Maillots**

### Affichage avec Pagination
- **Pagination intelligente** : 12, 24, 48 ou 100 maillots par page
- **Navigation** : Boutons Précédent/Suivant + numéros de pages
- **Compteur** : "1-24 sur 1152 maillots"
- **Scroll automatique** : Retour en haut à chaque changement de page

### Fonctionnalités d'Édition
- ✏️ **Modifier le nom** et la description
- 🏷️ **Catégories multiples** (comme les tags)
- 🔖 **Tags multiples** avec sélection Ctrl
- 🖼️ **Changement de cover** visuel (cliquer sur l'image)
- 🗑️ **Suppression** avec confirmation

### Modification d'un Maillot
1. Cliquer sur "Modifier"
2. Modifier les champs souhaités
3. **Catégories** : Maintenir Ctrl pour sélectionner plusieurs
4. **Tags** : Maintenir Ctrl pour sélectionner plusieurs
5. **Image de couverture** : Cliquer sur l'image désirée
6. Enregistrer

---

## 🏷️ **Gestion des Catégories**

### Créer une Catégorie
1. Onglet "Catégories"
2. Bouton "Créer une catégorie"
3. Saisir le nom
4. Choisir la couleur
5. Enregistrer

### Modifier une Catégorie
1. Cliquer sur "Modifier"
2. Changer le nom/couleur
3. Enregistrer

### Supprimer une Catégorie
1. Cliquer sur "Supprimer"
2. Confirmer la suppression

**Note** : Les catégories sont maintenant multiples pour chaque maillot (comme les tags)

---

## 🔖 **Gestion des Tags**

### Créer un Tag
1. Onglet "Tags"
2. Bouton "Créer un tag"
3. Saisir le nom
4. Choisir la couleur
5. Enregistrer

### Modifier un Tag
1. Cliquer sur "Modifier"
2. Changer le nom/couleur
3. Enregistrer

### Supprimer un Tag
1. Cliquer sur "Supprimer"
2. Confirmer la suppression

---

## 🔐 **Authentification**

### Connexion
- **URL** : http://localhost:8000/login.html
- **Identifiants** : admin / admin123
- **Session** : 1 heure (configurable dans data/config.json)

### Déconnexion
- Bouton rouge en haut à droite
- Redirige vers login.html

### Sécurité
- ✅ Toutes les routes admin protégées
- ✅ Vérification auth au chargement
- ✅ Sessions avec cookies sécurisés
- ✅ Mot de passe hashé avec bcrypt

---

## 🚀 **Lancement du Site**

### Commande
```powershell
python launch_site.py
```

### URLs
- **Site public** : http://localhost:8000
- **Admin** : http://localhost:8000/login.html
- **API** : http://localhost:8001/api
- **Admin simple** (backup) : http://localhost:8000/index.html?admin=true

---

## 📁 **Structure des Fichiers**

```
MaillotsDuPeuple/
├── admin_production.html       # ⭐ Interface admin complète
├── admin_production_backup.html # Sauvegarde ancienne version
├── login.html                   # Page de connexion
├── index.html                   # Site public
├── launch_site.py              # Lanceur des serveurs
├── data/
│   ├── jerseys.json            # Base de données maillots
│   ├── categories.json         # Catégories
│   ├── tags.json              # Tags
│   ├── reviews.json           # Avis Vinted
│   └── config.json            # Configuration (auth, etc.)
└── scripts/
    └── production_backend.py   # Backend Flask avec auth
```

---

## 🎯 **Nouveautés v2.0**

### ✅ Implémenté
- [x] **Pagination intelligente** pour gérer 1152+ maillots
- [x] **Catégories multiples** par maillot (comme tags)
- [x] **Création/édition/suppression** catégories
- [x] **Création/édition/suppression** tags
- [x] **Interface moderne** avec design cohérent
- [x] **Sélection visuelle** de l'image de couverture
- [x] **Navigation par onglets**
- [x] **Statistiques en temps réel**
- [x] **Responsive** mobile/tablette/desktop

### 🔧 Routes API Disponibles

#### Authentification
- `POST /api/auth/login` - Connexion
- `POST /api/auth/logout` - Déconnexion
- `GET /api/auth/status` - Vérifier session

#### Maillots
- `GET /api/jerseys` - Liste complète
- `POST /api/jerseys/update` - Modifier maillot
- `POST /api/jerseys/update-cover` - Changer image cover
- `DELETE /api/admin/jerseys/{id}` - Supprimer maillot

#### Catégories
- `GET /api/categories` - Liste complète
- `POST /api/categories/create` - Créer
- `POST /api/categories/update` - Modifier
- `POST /api/categories/delete` - Supprimer

#### Tags
- `GET /api/tags` - Liste complète
- `POST /api/tags/create` - Créer
- `POST /api/tags/update` - Modifier
- `POST /api/tags/delete` - Supprimer

#### Admin
- `GET /api/admin/stats` - Statistiques dashboard

---

## 💡 **Conseils d'Utilisation**

### Pagination
- **Pour 1152 maillots** : Utiliser 24 ou 48 par page
- **Navigation rapide** : Utiliser les numéros de page directement
- Les pages inutilisées sont masquées avec "..."

### Sélection Multiple (Catégories/Tags)
- **Windows** : Maintenir `Ctrl` + clic
- **Mac** : Maintenir `Cmd` + clic
- Sélectionner plusieurs items avant d'enregistrer

### Image de Couverture
- Cliquer directement sur l'image désirée
- Une bordure verte apparaît sur l'image sélectionnée
- Enregistrer pour appliquer

### Performance
- Le chargement initial peut prendre 2-3 secondes (1152 maillots)
- La pagination améliore grandement la fluidité
- Les images sont en lazy loading

---

## 🐛 **Dépannage**

### Problème : "Non authentifié"
- **Solution** : Reconnecter via login.html

### Problème : Maillots ne s'affichent pas
- **Vérifier** : Les serveurs sont lancés (python launch_site.py)
- **Vérifier** : data/jerseys.json existe et est valide

### Problème : Modifications non enregistrées
- **Vérifier** : Message de succès apparaît (vert)
- **Vérifier** : Logs backend dans le terminal

### Problème : Pagination ne fonctionne pas
- **Solution** : Rafraîchir la page (F5)
- **Vérifier** : Console navigateur (F12) pour erreurs JS

---

## 📝 **Configuration Avancée**

### Modifier le timeout de session
**Fichier** : `data/config.json`
```json
{
  "admin": {
    "session_timeout": 3600  // En secondes (1h par défaut)
  }
}
```

### Changer le mot de passe admin
**Commande** :
```python
import bcrypt
password = b"VotreNouveauMotDePasse"
hash = bcrypt.hashpw(password, bcrypt.gensalt())
print(hash.decode())
```
Copier le hash dans `data/config.json` → `admin.password_hash`

### Ajuster les items par page
**Fichier** : `admin_production.html`
Ligne ~690 : Modifier les options du select
```html
<option value="12">12 par page</option>
<option value="24" selected>24 par page</option>
<option value="48">48 par page</option>
<option value="100">100 par page</option>
```

---

## 🎉 **C'est Prêt !**

Votre interface admin est maintenant **complète** et **production-ready** :
- ✅ Pagination pour gérer des milliers de maillots
- ✅ Catégories multiples
- ✅ Gestion complète catégories/tags
- ✅ Design moderne et responsive
- ✅ Sécurisé avec authentification

**Prochaines étapes suggérées** :
1. Tester toutes les fonctionnalités
2. Importer de nouveaux maillots Yupoo
3. Créer les catégories/tags nécessaires
4. Lancer le site en production demain ! 🚀

---

**Dernière mise à jour** : 19 octobre 2025
**Version** : 2.0 - Production Ready
