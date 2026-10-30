param([string]$Root, [int]$Par = 7)
$dirs = Get-ChildItem $Root -Directory | Where-Object { -not (Test-Path (Join-Path $_.FullName 'last.txt')) -or (Get-Item (Join-Path $_.FullName 'last.txt')).Length -lt 200 }
$jobs = @()
foreach ($d in $dirs) {
  while (($jobs | Where-Object State -eq 'Running').Count -ge $Par) { Start-Sleep -Seconds 5 }
  $jobs += Start-Job -ArgumentList $d.FullName -ScriptBlock { param($p) Set-Location $p; Get-Content (Join-Path $p 'brief.txt') -Raw -Encoding utf8 | codex exec --skip-git-repo-check -s read-only -o (Join-Path $p 'last.txt') *> (Join-Path $p 'run.log') }
}
$jobs | Wait-Job | Out-Null
"done: " + ((Get-ChildItem $Root -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'last.txt') }).Count) + " of " + (Get-ChildItem $Root -Directory).Count
