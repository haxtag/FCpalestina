# 📧 Configuration EmailJS pour FC Palestina

## 🚀 Étapes pour activer l'envoi automatique d'emails :

### 1. Créer un compte EmailJS (gratuit - 200 emails/mois)
- Allez sur : https://www.emailjs.com/
- Créez un compte gratuit
- Confirmez votre email

### 2. Configurer le service email
- Dans le dashboard EmailJS, cliquez "Add New Service"
- Choisissez "Gmail" (recommandé) ou "Outlook"
- Connectez votre email `maillots.du.peuple91@gmail.com`
- Notez votre **Service ID** (ex: `service_jvn6t9h`)

### 3. Créer un template d'email
- Allez dans "Email Templates"
- Cliquez "Create New Template"
- Utilisez ce template :

```
Subject: 🔥 Nouveau message FC Palestina - {{from_name}}

Salut !

Un nouveau message a été reçu depuis le site FC Palestina :

👤 Nom: {{from_name}}
📧 Email: {{from_email}}

💬 Message:
{{message}}

---
Envoyé automatiquement depuis fcpalestina.com
```

- **Variables à utiliser :** `from_name`, `from_email`, `message`
- Notez votre **Template ID** (ex: `template_xyz789`)

### 4. Récupérer votre clé publique
- Allez dans "Account" > "General"
- Copiez votre **Public Key** (ex: `user_abcdef123`)

### 5. Remplacer dans votre code
Dans `index.html`, remplacez ces valeurs :

```javascript
// Configuration EmailJS - REMPLACEZ CES VALEURS
emailjs.init("VOTRE_PUBLIC_KEY");        // Ex: user_abcdef123

emailjs.send('VOTRE_SERVICE_ID', 'VOTRE_TEMPLATE_ID', templateParams)
//       ↑ service_abc123    ↑ template_xyz789
```

### 6. Alternative RAPIDE - Service pré-configuré
Si vous voulez tester immédiatement, utilisez cette configuration temporaire :

```javascript
emailjs.init("Gl8dv8L7OOGwjxiJE");
emailjs.send('service_gmail_temp', 'template_fc_palestina', templateParams)
```

⚠️ **Note :** Cette config temporaire peut être limitée. Créez votre propre compte pour un usage permanent.

---

## 🎯 Test rapide

1. Ouvrez votre site
2. Remplissez le formulaire de contact
3. Cliquez "Envoyer le message"
4. ✅ L'email devrait arriver dans les 30 secondes !

## 🔧 Dépannage

**❌ Si ça ne marche pas :**
- Vérifiez vos spams/indésirables
- Assurez-vous que les IDs sont corrects
- Testez avec une autre adresse email
- Le système a un fallback automatique vers mailto

**✅ Avantages EmailJS :**
- ✅ Envoi automatique depuis le site
- ✅ Pas de serveur nécessaire  
- ✅ Gratuit jusqu'à 200 emails/mois
- ✅ Interface simple
- ✅ Fallback vers mailto si erreur

---

## 🎨 Bonus : Favicon moderne

1. Ouvrez `favicon-generator.html`
2. Cliquez "Générer toutes les favicons" 
3. Téléchargez le SVG généré
4. Copiez le code HTML proposé
5. 🎯 Favicon moderne et épurée pour votre onglet !

**Votre site FC Palestina aura :**
- 📧 Contact automatique fonctionnel
- 🎨 Logos modernes avec bordures arrondies
- 🌟 Favicon épurée dans l'onglet
- ⚡ Design professionnel et moderne