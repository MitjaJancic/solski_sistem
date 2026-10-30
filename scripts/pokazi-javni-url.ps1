# Skripta poišče in izpiše ZADNJI veljavni javni HTTPS naslov Cloudflare tunela
$logs = docker compose logs tunel 2>&1 | Out-String
$allMatches = [regex]::Matches($logs, "https://[a-zA-Z0-9-]+\.trycloudflare\.com")
if ($allMatches.Count -gt 0) {
    $url = $allMatches[$allMatches.Count - 1].Value
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
