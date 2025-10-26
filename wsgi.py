"""
WSGI Configuration pour PythonAnywhere
Fichier à utiliser dans la configuration Web App de PythonAnywhere
"""

import sys
import os

# === CONFIGURATION À ADAPTER ===
# Remplace <USERNAME> par ton username PythonAnywhere
# Exemple: si ton username est "MaillotsduPeuple", mets:
# project_home = '/home/MaillotsduPeuple/FCpalestina'
project_home = '/home/<USERNAME>/FCpalestina'

# Ajouter le projet au path Python
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Changer le working directory pour les chemins relatifs
os.chdir(project_home)

# Variables d'environnement (MIEUX: utiliser l'interface Web de PythonAnywhere)
# Ces valeurs peuvent être définies dans Web > Environment variables
# os.environ['SECRET_KEY'] = 'your-secret-key-here'
# os.environ['FLASK_DEBUG'] = 'false'

# Import de l'application Flask
# Notre app s'appelle "app" dans production_backend.py
from scripts.production_backend import app as application

# PythonAnywhere cherche automatiquement "application"
