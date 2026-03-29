Param()

$apiKey = $env:SPRITECOOK_API_KEY
if (-not $apiKey) { Write-Error "Set SPRITECOOK_API_KEY environment variable."; exit 2 }

$body = @{ jsonrpc = '2.0'; id = 1; method = 'get_credit_balance'; params = @{} } | ConvertTo-Json -Depth 6
try {
  $resp = Invoke-RestMethod -Method Post -Uri 'https://api.spritecook.ai/mcp/' -Headers @{ Authorization = "Bearer $apiKey" } -Body $body -ContentType 'application/json'
} catch {
  Write-Error "Request failed: $_"
  exit 2
}

$credits = $null
if ($resp.result -and $resp.result.credits) { $credits = $resp.result.credits }
if (-not $credits) {
  # try to find nested
  function Find-Key($obj,$key) {
    if ($null -eq $obj) { return $null }
    if ($obj -is [System.Collections.IDictionary]) {
      if ($obj.Contains($key)) { return $obj[$key] }
      foreach ($k in $obj.Keys) { $r = Find-Key $obj[$k] $key; if ($r) { return $r } }
    } elseif ($obj -is [System.Collections.IEnumerable]) {
      foreach ($e in $obj) { $r = Find-Key $e $key; if ($r) { return $r } }
    }
    return $null
  }
  $credits = Find-Key $resp 'credits'
}

Write-Host "credits: $credits"
if ($credits -and ($credits -as [int]) -gt 0) { exit 0 } else { exit 3 }
