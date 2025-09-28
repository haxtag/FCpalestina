@echo off
echo 🚀 Démarrage du serveur d'administration FC Palestina...
echo.
echo 📱 Interface admin: http://localhost:8001/admin-login.html
echo 🔑 Identifiants: admin / fcpalestina2024
echo.
echo 🛑 Appuyez sur Ctrl+C pour arrêter
echo.

python scripts/admin_server.py 8001

pause
