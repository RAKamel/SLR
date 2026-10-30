param([string]$Root, [int]$Par = 6)
$dirs = Get-ChildItem $Root -Directory | Where-Object { -not ((Test-Path (Join-Path $_.FullName 'last.txt')) -and (Select-String -Path (Join-Path $_.FullName 'last.txt') -Pattern 'END_CSV' -Quiet)) }
$jobs = @()
foreach ($d in $dirs) {
  while (($jobs | Where-Object State -eq 'Running').Count -ge $Par) { Start-Sleep -Seconds 5 }
  $jobs += Start-Job -ArgumentList $d.FullName -ScriptBlock { param($p) Set-Location $p; $b = Get-Content (Join-Path $p 'brief.txt') -Raw -Encoding utf8; agy -p $b --mode plan *> (Join-Path $p 'last.txt') }
}
$jobs | Wait-Job | Out-Null
"done: " + ((Get-ChildItem $Root -Directory | Where-Object { (Test-Path (Join-Path $_.FullName 'last.txt')) -and (Select-String -Path (Join-Path $_.FullName 'last.txt') -Pattern 'END_CSV' -Quiet) }).Count) + " of " + (Get-ChildItem $Root -Directory).Count
