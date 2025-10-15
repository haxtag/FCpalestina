Write-Host "🚀 Démarrage du backend d'administration (Flask) et utilisation de l'admin ultra-simple..." -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Ouvrez ensuite: http://localhost:8000/index.html?admin=true" -ForegroundColor Cyan
Write-Host "   (Le panneau admin ultra-simple s'ouvrira sur la page principale)" -ForegroundColor DarkCyan
Write-Host ""
Write-Host "🛑 Appuyez sur Ctrl+C pour arrêter" -ForegroundColor Red
Write-Host ""

python scripts/simple_backend.py

Read-Host "Appuyez sur Entrée pour fermer"
