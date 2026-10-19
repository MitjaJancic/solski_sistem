# Skripta poišče in izpiše trenutni javni HTTPS naslov Cloudflare tunela
$logs = docker compose logs tunel 2>&1 | Out-String
if ($logs -match "https://[a-zA-Z0-9-]+\.trycloudflare\.com") {
    $url = $matches[0]
    Write-Host ""
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host "  JAVNA DOMENA DELUJE (Cloudflare Tunnel):" -ForegroundColor Green
    Write-Host "  $url" -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host "Povezavo lahko odprete na telefonu ali jo posredujete mentorju."
    Write-Host ""
} else {
    Write-Host "Tunel se še zaganja ali ni zagnan. Zaženite: docker compose up -d" -ForegroundColor Yellow
}
