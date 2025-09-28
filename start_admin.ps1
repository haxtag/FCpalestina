Write-Host "🚀 Démarrage du serveur d'administration FC Palestina..." -ForegroundColor Green
Write-Host ""
Write-Host "📱 Interface admin: http://localhost:8001/admin-login.html" -ForegroundColor Cyan
Write-Host "🔑 Identifiants: admin / fcpalestina2024" -ForegroundColor Yellow
Write-Host ""
Write-Host "🛑 Appuyez sur Ctrl+C pour arrêter" -ForegroundColor Red
Write-Host ""

python scripts/admin_server.py 8001

Read-Host "Appuyez sur Entrée pour fermer"
