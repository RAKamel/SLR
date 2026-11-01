# Build the final Moodle submission bundle from verified project artifacts.
# The stale Word workbook and superseded PDF are intentionally excluded.
# Run from anywhere:  .\scripts\make_moodle_bundle.ps1
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$bundle = Join-Path $root 'SLR_Moodle_Submission_Ramy_Kamel.zip'
$stage = Join-Path $env:TEMP ('slr-moodle-bundle-' + [guid]::NewGuid().ToString('N'))

$items = @(
    @{ Source = 'SLR_Submission_Ramy_Kamel_FINAL.pdf'; Destination = 'final/SLR_Submission_Ramy_Kamel_FINAL.pdf' },
    @{ Source = 'paper_overleaf.zip'; Destination = 'source/paper_overleaf.zip' },
    @{ Source = 'data/extraction/extraction.xlsx'; Destination = 'data/extraction.xlsx' },
    @{ Source = 'data/prisma_counts.json'; Destination = 'prisma/prisma_counts.json' },
    @{ Source = 'data/screening/protocol_criteria.md'; Destination = 'prisma/protocol_criteria.md' },
    @{ Source = 'paper/figures/prisma_flow.tex'; Destination = 'prisma/prisma_flow.tex' },
    @{ Source = 'paper/sections/appendix-prisma-checklist.tex'; Destination = 'prisma/appendix-prisma-checklist.tex' },
    @{ Source = 'paper/sections/ai-use-statement.tex'; Destination = 'disclosure/ai-use-statement.tex' },
    @{ Source = 'paper/refs.bib'; Destination = 'bibliography/refs.bib' },
    @{ Source = 'paper/included_studies.bib'; Destination = 'bibliography/included_studies.bib' },
    @{ Source = 'paper/background_refs.bib'; Destination = 'bibliography/background_refs.bib' },
    @{ Source = 'paper/selected_refs.bib'; Destination = 'bibliography/selected_refs.bib' }
)

New-Item -ItemType Directory -Path $stage | Out-Null
try {
    $manifest = @(
        'DAI701 SLR Moodle submission bundle',
        'Generated: 2026-11-01',
        '',
        'Upload the final PDF as the primary manuscript. The remaining files support reproducibility.',
        'The stale 61-study Word workbook and the superseded pre-caption PDF are intentionally excluded.',
        '',
        'SHA-256 manifest:'
    )

    foreach ($item in $items) {
        $source = Join-Path $root $item.Source
        if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
            throw "Missing required submission artifact: $source"
        }

        $destination = Join-Path $stage ($item.Destination -replace '/', [IO.Path]::DirectorySeparatorChar)
        $destinationDirectory = Split-Path -Parent $destination
        New-Item -ItemType Directory -Path $destinationDirectory -Force | Out-Null
        Copy-Item -LiteralPath $source -Destination $destination -Force
        $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $source).Hash
        $manifest += "$hash  $($item.Destination)"
    }

    $manifestPath = Join-Path $stage 'MANIFEST.txt'
    $manifest | Set-Content -LiteralPath $manifestPath -Encoding utf8

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    if (Test-Path -LiteralPath $bundle) {
        Remove-Item -LiteralPath $bundle -Force
    }
    [System.IO.Compression.ZipFile]::CreateFromDirectory($stage, $bundle)

    $archive = [System.IO.Compression.ZipFile]::OpenRead($bundle)
    try {
        if ($archive.Entries.Count -ne 13) {
            throw "Expected 13 bundle entries; found $($archive.Entries.Count)"
        }
        $archive.Entries.FullName
    }
    finally {
        $archive.Dispose()
    }

    Write-Output "written: $bundle"
    Write-Output "SHA256: $((Get-FileHash -Algorithm SHA256 -LiteralPath $bundle).Hash)"
}
finally {
    $resolvedStage = [IO.Path]::GetFullPath($stage)
    $resolvedTemp = [IO.Path]::GetFullPath($env:TEMP)
    if ($resolvedStage.StartsWith($resolvedTemp, [StringComparison]::OrdinalIgnoreCase) -and
        (Split-Path -Leaf $resolvedStage).StartsWith('slr-moodle-bundle-', [StringComparison]::OrdinalIgnoreCase)) {
        Remove-Item -LiteralPath $resolvedStage -Recurse -Force -ErrorAction SilentlyContinue
    }
}
