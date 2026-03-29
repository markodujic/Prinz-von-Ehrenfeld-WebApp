Param(
  [Parameter(Mandatory=$false)][string]$Prompt = "16-bit SNES style side view character: young male in a hoodie and cap",
  [int]$Width = 64,
  [int]$Height = 64
)

Write-Host "Checking credits..."
.\scripts\check-credits.ps1
$last = $LASTEXITCODE
if ($last -eq 0) {
  Write-Host "Credits ok — generating sprite..."
  .\scripts\generate-sprite.ps1 -Prompt $Prompt -Width $Width -Height $Height
  exit 0
} elseif ($last -eq 3) {
  Write-Error "No credits available. Aborting."
  exit 3
} else {
  Write-Error "Error checking credits (exit $last)."
  exit $last
}
