# 🎨 Guide de Gestion des Couleurs de Catégories

## Vue d'ensemble

Les couleurs des boutons de filtrage sont maintenant **gérées dynamiquement** depuis le fichier `data/categories.json`. Vous pouvez changer les couleurs ou ajouter de nouvelles catégories sans toucher au code HTML, CSS ou JavaScript !

## Comment ça marche ?

1. **Au chargement de la page**, le module `categoryColors.js` :
   - Charge le fichier `data/categories.json`
   - Génère automatiquement le CSS pour chaque catégorie
   - Applique les styles aux boutons filtres

2. **Les couleurs sont définies dans** `data/categories.json` :
   ```json
   [
     {
       "id": "home",
       "name": "Domicile",
       "description": "Maillots domicile",
       "color": "#8B1538"
     },
     ...
   ]
   ```

3. **Le CSS est généré dynamiquement** :
   - État normal : contour coloré + texte coloré + fond transparent
   - État actif : fond coloré + texte blanc

## 🔄 Changer une couleur

1. Ouvrir le fichier `data/categories.json`
2. Trouver la catégorie à modifier (ex: `"id": "home"`)
3. Changer la valeur du champ `"color"` (ex: `"#FF0000"` pour rouge)
4. Sauvegarder le fichier
5. **Rafraîchir la page** (F5) → les nouvelles couleurs s'appliquent automatiquement !

### Exemple : Changer "Domicile" en rouge vif

**Avant :**
```json
{
  "id": "home",
  "name": "Domicile",
  "description": "Maillots domicile",
  "color": "#8B1538"
}
```

**Après :**
```json
{
  "id": "home",
  "name": "Domicile",
  "description": "Maillots domicile",
  "color": "#FF0000"
}
```

## ➕ Ajouter une nouvelle catégorie

### 1. Ajouter la catégorie dans `data/categories.json`

```json
{
  "id": "limited",
  "name": "Édition Limitée",
  "description": "Maillots en édition limitée",
  "color": "#9333EA"
}
```

### 2. Ajouter le bouton dans `index.html`

Trouver la section des filtres et ajouter :

```html
<button class="filter-btn" data-filter="limited">
    Édition Limitée
</button>
```

### 3. C'est tout ! 🎉

Rafraîchissez la page et le bouton aura automatiquement :
- Un contour violet (#9333EA)
- Un texte violet
- Un fond transparent
- Un fond violet + texte blanc quand actif

## 📋 Liste des catégories actuelles

| ID | Nom | Couleur Actuelle | Hex Code |
|----|-----|------------------|----------|
| `home` | Domicile | Bordeaux | `#8B1538` |
| `away` | Extérieur | Gris | `#6c757d` |
| `third` | Troisième | Noir | `#000000` |
| `keeper` | Gardien | Vert | `#28a745` |
| `special` | Spéciaux | Jaune | `#ffc107` |
| `vintage` | Vintage | Marron | `#8b4513` |

## 🎨 Choisir de bonnes couleurs

### Conseils :
- Utilisez des couleurs **contrastées** pour la lisibilité
- Évitez les couleurs trop claires (blanc, jaune pâle) → difficiles à lire
- Testez le contraste : https://webaim.org/resources/contrastchecker/

### Palette suggérée :
- **Rouge** : `#DC2626` (rouge vif)
- **Bleu** : `#2563EB` (bleu royal)
- **Vert** : `#16A34A` (vert émeraude)
- **Orange** : `#EA580C` (orange brûlé)
- **Violet** : `#9333EA` (violet profond)
- **Rose** : `#DB2777` (rose fuchsia)
- **Teal** : `#0D9488` (bleu-vert)
- **Indigo** : `#4F46E5` (indigo)

## 🔄 Rafraîchir manuellement les couleurs

Si vous modifiez `categories.json` pendant que la page est ouverte, vous pouvez rafraîchir les couleurs sans recharger la page entière :

**Dans la console du navigateur (F12) :**
```javascript
categoryColorManager.refresh()
```

## 🐛 Dépannage

### Les couleurs ne s'appliquent pas ?

1. **Vérifier que le fichier `categories.json` est valide** :
   - Ouvrir dans un éditeur
   - Vérifier qu'il n'y a pas d'erreur de syntaxe JSON
   - Utiliser un validateur JSON : https://jsonlint.com/

2. **Vérifier la console du navigateur** (F12 → Console) :
   - Chercher des erreurs rouges
   - Vérifier le message : `✅ Catégories chargées: ...`

3. **Vider le cache du navigateur** :
   - Chrome/Edge : `Ctrl+Shift+Delete`
   - Firefox : `Ctrl+Shift+Del`
   - Ou utilisez le mode navigation privée

### Le bouton existe mais n'a pas de couleur ?

Vérifier que :
- Le `data-filter` du bouton HTML correspond exactement à l'`id` dans JSON
- Exemple : `<button data-filter="home">` ↔ `"id": "home"`

### La couleur est trop claire / trop foncée ?

Ajuster la luminosité du code hex :
- Plus clair : augmenter les valeurs (ex: `#8B1538` → `#A61E47`)
- Plus foncé : diminuer les valeurs (ex: `#8B1538` → `#5C0E26`)

Outil utile : https://colordesigner.io/color-lightness

## 📁 Fichiers concernés

- **`data/categories.json`** → Définition des couleurs (MODIFIER ICI)
- **`assets/js/modules/categoryColors.js`** → Chargement dynamique (ne pas modifier)
- **`assets/css/components/gallery.css`** → Styles de base (ne plus toucher aux couleurs)
- **`index.html`** → Boutons de filtrage (ajouter/retirer des boutons)

## ✅ Avantages de ce système

- ✅ **Facile** : Modifier un simple fichier JSON
- ✅ **Maintenable** : Pas besoin de toucher au code CSS/JS
- ✅ **Flexible** : Ajouter/retirer des catégories facilement
- ✅ **Cohérent** : Une seule source de vérité pour les couleurs
- ✅ **Testable** : Changer les couleurs et voir le résultat instantanément
