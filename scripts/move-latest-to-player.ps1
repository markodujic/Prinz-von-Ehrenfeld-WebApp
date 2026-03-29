Param()

$srcDir = "assets\generated"
$dstDir = "assets\sprites"
If (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Path $dstDir | Out-Null }

$files = Get-ChildItem -Path $srcDir -Filter 'sprite_*.png' | Sort-Object LastWriteTime -Descending
if ($files.Count -eq 0) {
  Write-Error "No generated sprite found in $srcDir"
  exit 1
}

$latest = $files[0].FullName
$dst = Join-Path $dstDir 'Player.png'
Write-Host "Copying $latest -> $dst"
Copy-Item -Path $latest -Destination $dst -Force
Write-Host "Done."
