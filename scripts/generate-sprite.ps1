Param(
  [Parameter(Mandatory=$true)][string]$Prompt,
  [int]$Width = 64,
  [int]$Height = 64,
  [bool]$Pixel = $true,
  [string]$BgMode = 'transparent',
  [string]$OutDir = 'assets\generated'
)

if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

$apiKey = $env:SPRITECOOK_API_KEY
if (-not $apiKey) { Write-Error "Set SPRITECOOK_API_KEY environment variable."; exit 1 }

$body = @{ jsonrpc = '2.0'; id = 1; method = 'generate_game_art'; params = @{ prompt = $Prompt; width = $Width; height = $Height; variations = 1; pixel = $Pixel; bg_mode = $BgMode } } | ConvertTo-Json -Depth 6

Write-Host "Requesting sprite generation..."
$resp = Invoke-RestMethod -Method Post -Uri 'https://api.spritecook.ai/mcp/' -Headers @{ Authorization = "Bearer $apiKey" } -Body $body -ContentType 'application/json'

$url = $null
if ($resp.result -and $resp.result.assets -and $resp.result.assets.Count -gt 0) { $url = $resp.result.assets[0].pixel_url }

if (-not $url) { Write-Error "No pixel_url found. Response:`n$($resp | ConvertTo-Json -Depth 6)"; exit 1 }

$outfile = Join-Path $OutDir "sprite_$(Get-Date -UFormat %s).png"
Write-Host "Downloading $url -> $outfile"
Invoke-WebRequest -Uri $url -OutFile $outfile
Write-Host "Saved to $outfile"
