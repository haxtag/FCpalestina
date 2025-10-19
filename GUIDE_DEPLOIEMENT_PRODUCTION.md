# 🚀 GUIDE DE DÉPLOIEMENT - FC Palestina

## ⚠️ CHECKLIST SÉCURITÉ (À FAIRE AVANT LE LANCEMENT)

### 1. Changer les identifiants admin
```bash
# Générer un nouveau mot de passe fort
python generate_password_hash.py
# Puis mettre à jour data/config.json
```

**Recommandé**: Mot de passe de 16+ caractères avec majuscules, minuscules, chiffres, symboles

---

### 2. Variables d'environnement

**Ne JAMAIS commiter** les secrets dans Git!

Créer un fichier `.env` (à ajouter au `.gitignore`):
```bash
SECRET_KEY=votre_secret_key_tres_longue_et_aleatoire
ADMIN_USERNAME=VotreUsername
ADMIN_PASSWORD_HASH=votre_hash_bcrypt
FLASK_ENV=production
```

**Modifier `production_backend.py`**:
```python
from dotenv import load_dotenv
load_dotenv()

app.secret_key = os.environ.get('SECRET_KEY')
```

---

### 3. Configuration Production

#### A. HTTPS Obligatoire
```python
# Dans production_backend.py
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS seulement
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Protection XSS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protection CSRF
```

#### B. CORS Production
```python
# Remplacer localhost par votre domaine
CORS(app, 
     supports_credentials=True,
     origins=['https://votre-domaine.com'],  # Pas localhost!
     allow_headers=['Content-Type'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
```

#### C. Debug Mode OFF
```python
# Ligne de lancement
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False)  # debug=False!
```

---

## 📦 DÉPLOIEMENT VPS (Recommandé)

### Étape 1: Préparer les fichiers

```bash
# Créer requirements.txt
pip freeze > requirements.txt

# Créer .gitignore
cat > .gitignore << EOF
__pycache__/
*.pyc
*.log
.env
venv/
data/config.json
*.swp
.DS_Store
EOF

# Créer structure
.
├── assets/
├── data/
├── scripts/
├── index.html
├── admin_production.html
├── login.html
├── requirements.txt
├── .env (ne pas commiter!)
└── README.md
```

---

### Étape 2: Configuration serveur

#### Installation sur Ubuntu/Debian
```bash
# Se connecter au VPS
ssh root@votre-ip

# Mettre à jour
apt update && apt upgrade -y

# Installer Python et dépendances
apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# Créer utilisateur
adduser fcpalestina
usermod -aG sudo fcpalestina
su - fcpalestina
```

#### Installer l'application
```bash
# Cloner ou uploader les fichiers
cd /home/fcpalestina
git clone votre-repo.git site
# OU
# scp -r FCpalestina/ fcpalestina@votre-ip:/home/fcpalestina/site

cd site

# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install -r requirements.txt
```

---

### Étape 3: Nginx + Gunicorn

#### A. Installer Gunicorn
```bash
pip install gunicorn
```

#### B. Créer service systemd
```bash
sudo nano /etc/systemd/system/fcpalestina.service
```

Contenu:
```ini
[Unit]
Description=FC Palestina Backend
After=network.target

[Service]
User=fcpalestina
WorkingDirectory=/home/fcpalestina/site
Environment="PATH=/home/fcpalestina/site/venv/bin"
ExecStart=/home/fcpalestina/site/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8001 scripts.production_backend:app

[Install]
WantedBy=multi-user.target
```

#### C. Configuration Nginx
```bash
sudo nano /etc/nginx/sites-available/fcpalestina
```

Contenu:
```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;

    # Frontend (fichiers statiques)
    location / {
        root /home/fcpalestina/site;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Assets
    location /assets {
        root /home/fcpalestina/site;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

#### D. Activer et démarrer
```bash
# Activer site
sudo ln -s /etc/nginx/sites-available/fcpalestina /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Démarrer backend
sudo systemctl start fcpalestina
sudo systemctl enable fcpalestina
sudo systemctl status fcpalestina
```

---

### Étape 4: HTTPS avec Let's Encrypt

```bash
# Obtenir certificat SSL gratuit
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com

# Renouvellement automatique (déjà configuré)
sudo certbot renew --dry-run
```

---

## 🔧 MAINTENANCE

### Logs
```bash
# Backend
sudo journalctl -u fcpalestina -f

# Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Application
tail -f /home/fcpalestina/site/backend_production.log
```

### Redémarrer services
```bash
# Backend
sudo systemctl restart fcpalestina

# Nginx
sudo systemctl reload nginx
```

### Mise à jour du code
```bash
cd /home/fcpalestina/site
git pull  # ou upload nouveaux fichiers
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart fcpalestina
```

---

## 📊 MONITORING (Optionnel mais recommandé)

### Uptime monitoring
- **UptimeRobot** (gratuit) - Alerte si le site tombe
- **Pingdom** (gratuit jusqu'à 50 checks)

### Analytics
- **Google Analytics** (gratuit)
- **Matomo** (open source, auto-hébergé)

---

## 🔐 BACKUP AUTOMATIQUE

```bash
# Créer script de backup
nano /home/fcpalestina/backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/fcpalestina/backups"
mkdir -p $BACKUP_DIR

# Backup data
tar -czf $BACKUP_DIR/data_$DATE.tar.gz /home/fcpalestina/site/data/

# Garder seulement les 7 derniers backups
find $BACKUP_DIR -name "data_*.tar.gz" -mtime +7 -delete
```

```bash
# Rendre exécutable
chmod +x /home/fcpalestina/backup.sh

# Ajouter au cron (tous les jours à 3h du matin)
crontab -e
0 3 * * * /home/fcpalestina/backup.sh
```

---

## ✅ CHECKLIST FINALE AVANT LANCEMENT

- [ ] Identifiants admin changés (mot de passe fort)
- [ ] Variables d'environnement configurées (.env)
- [ ] Debug mode = False
- [ ] HTTPS activé (Let's Encrypt)
- [ ] CORS configuré avec le bon domaine
- [ ] Cookies sécurisés (Secure, HttpOnly, SameSite)
- [ ] Firewall configuré (ufw)
- [ ] Backup automatique configuré
- [ ] Monitoring actif (UptimeRobot)
- [ ] DNS configuré (A records)
- [ ] Testé sur mobile et desktop
- [ ] Testé login/logout
- [ ] Testé CRUD admin
- [ ] Logs vérifiés

---

## 🆘 TROUBLESHOOTING

### Backend ne démarre pas
```bash
sudo systemctl status fcpalestina
sudo journalctl -u fcpalestina -n 50
```

### Erreur 502 Bad Gateway
```bash
# Vérifier que le backend tourne
curl http://127.0.0.1:8001/api/auth/status
```

### CORS errors
- Vérifier que l'origin dans production_backend.py correspond à votre domaine HTTPS

### Session ne persiste pas
- Vérifier que les cookies sont activés
- Vérifier SESSION_COOKIE_SECURE en HTTPS

---

## 📞 SUPPORT

### Ressources utiles
- Documentation Flask: https://flask.palletsprojects.com/
- Nginx: https://nginx.org/en/docs/
- Let's Encrypt: https://letsencrypt.org/docs/
- DigitalOcean Tutorials: https://www.digitalocean.com/community/tutorials

---

**Bon lancement! 🚀🇵🇸**
