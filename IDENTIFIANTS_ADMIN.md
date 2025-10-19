# 🔐 Identifiants Admin - FC Palestina

## Connexion Admin

**URL**: http://localhost:8000/login.html

### Identifiants
- **Nom d'utilisateur**: `Badis`
- **Mot de passe**: `MagikALi104`

## ⚠️ IMPORTANT - SÉCURITÉ

### En Production
1. **Changez immédiatement le mot de passe** après le déploiement
2. **Utilisez HTTPS** (pas HTTP)
3. **Activez un firewall** pour limiter l'accès au backend

### Comment changer le mot de passe

#### Méthode 1: Via le script
```bash
python generate_password_hash.py
# Modifier le mot de passe dans le script, puis copier le hash généré
```

#### Méthode 2: Modifier directement config.json
```json
{
  "admin": {
    "username": "VotreNouveauNom",
    "password_hash": "VOTRE_HASH_BCRYPT",
    "session_timeout": 3600
  }
}
```

#### Méthode 3: Via Python
```python
import bcrypt
password = "VotreNouveauMotDePasse"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode('utf-8'))
```

## 📁 Fichiers de Configuration

### Fichiers modifiés
- `data/config.json` - Configuration active
- `scripts/production_backend.py` - Configuration par défaut (ligne 47-52)
- `admin_production.html` - Affichage du nom d'utilisateur

### Hash bcrypt actuel
```
$2b$12$mCDainvOZJaDYH7HSRaKg.LMXnCIzV8mxVHlLmJIjiozR8sh.3e0S
```

## 🔄 Session

- **Durée**: 1 heure (3600 secondes)
- **Type**: Cookie de session Flask
- **Sécurité**: Authentification requise via décorateur `@require_auth`

## 📝 Logs

Les tentatives de connexion sont enregistrées dans:
- `backend_production.log`

### Messages de log
- ✅ Connexion réussie: `Connexion admin réussie: Badis`
- ❌ Échec: `Tentative de connexion échouée: username`

## 🎯 Fonctionnalités Admin

Après connexion, vous avez accès à:
- ✅ Gestion des maillots (1152 items)
- ✅ Gestion des catégories
- ✅ Gestion des tags
- ✅ Statistiques
- ✅ Modification des images de couverture
- ✅ Assignation multiple de catégories/tags

---

**Date de création**: 19 octobre 2025
**Dernière modification**: 19 octobre 2025
