# Copy the generated PRISMA figure into paper\figures\ and zip paper\ as paper_overleaf.zip (main.tex at the zip root).
# Run from anywhere:  .\scripts\make_overleaf_zip.ps1
$ErrorActionPreference = 'Stop'
$root  = Split-Path -Parent $PSScriptRoot
$paper = Join-Path $root 'paper'
$fig   = Join-Path $root 'figures\prisma_flow.tex'
$zip   = Join-Path $root 'paper_overleaf.zip'

if (-not (Test-Path -LiteralPath $fig)) { throw "Missing $fig - run: python scripts\prisma.py" }
New-Item -ItemType Directory -Force (Join-Path $paper 'figures') | Out-Null
Copy-Item -LiteralPath $fig -Destination (Join-Path $paper 'figures\prisma_flow.tex') -Force

Add-Type -AssemblyName System.IO.Compression.FileSystem
if (Test-Path -LiteralPath $zip) { Remove-Item -LiteralPath $zip -Force }
[System.IO.Compression.ZipFile]::CreateFromDirectory($paper, $zip)   # entries use '/' separators, as Overleaf needs
$entries = [System.IO.Compression.ZipFile]::OpenRead($zip)
try { $entries.Entries.FullName } finally { $entries.Dispose() }
Write-Output "written: $zip"
