Param()

$manifest = 'docs\sprite-manifest.json'
if (-not (Test-Path $manifest)) { Write-Error "Manifest not found: $manifest"; exit 1 }

Write-Host "Starting batch generation from $manifest"
$json = Get-Content $manifest -Raw | ConvertFrom-Json
$count = 0
foreach ($item in $json) {
  $id = $item.id
  $prompt = $item.prompt
  $width = $item.width
  $height = $item.height
  $pixel = $item.pixel
  $bg_mode = $item.bg_mode

  Write-Host "Generating [$id] ($width x $height)"
  .\scripts\generate-sprite.ps1 -Prompt $prompt -Width $width -Height $height -Pixel $pixel -BgMode $bg_mode

  $files = Get-ChildItem -Path assets\generated -Filter 'sprite_*.png' | Sort-Object LastWriteTime -Descending
  if ($files.Count -eq 0) { Write-Error "No generated file found for $id"; exit 2 }
  $latest = $files[0].FullName
  $dest = Join-Path 'assets\generated' "$($id).png"
  Move-Item -Path $latest -Destination $dest -Force
  Write-Host "Saved to $dest"
  $count++
}

Write-Host "Batch generation finished. Generated $count assets."
