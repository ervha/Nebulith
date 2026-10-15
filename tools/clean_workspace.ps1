param([switch]$Apply)
$ErrorActionPreference = 'Stop'
$taskRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$report = Join-Path $taskRoot 'audit/maintenance/2026-10-15-cleanup.json'
if ($Apply -and (Test-Path -LiteralPath $report)) { throw 'Cleanup report exists; use a new dated run' }
$protected = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
Get-ChildItem -LiteralPath (Join-Path $taskRoot 'audit') -Recurse -File -Filter '*.json' | ForEach-Object {
    $data = Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json
    foreach ($property in @('artifact_sha256', 'manifest')) {
        if ($data.$property) {
            $data.$property.PSObject.Properties.Name | ForEach-Object {
                [void]$protected.Add([System.IO.Path]::GetFullPath((Join-Path $taskRoot $_)))
            }
        }
    }
}
$obsolete = @('build_master_lexicon_grand_1000.py','build_master_lexicon_v15.py','build_master_lexicon_v20.py',
 'build_master_lexicon_v21.py','generate_grand_milestone_1000.py','generate_v20_candidates.py','generate_v21_candidates.py',
 'check_levenshtein_660.py','generate_dashboard_v20.py','update_font_glyphs.py','update_all_remaining_glyphs.py',
 'update_num_specimen.py','create_specimen.py','map_reorganization.py','reclassify_lexicon.py','reorganize_and_expand.py')
$candidates = @($obsolete | ForEach-Object { Join-Path $taskRoot ('tools/' + $_) })
$candidates += Join-Path $taskRoot 'docs/dashboard_v20.html'
Get-ChildItem -LiteralPath (Join-Path $taskRoot 'audit/comparisons') -Directory | Where-Object {
    $_.Name -match '-draft$' -or $_.Name -eq 'glyph-v2.3-wide'
} | ForEach-Object { $candidates += $_.FullName }
$candidates += Join-Path $taskRoot 'audit/runs/2026-10-15-glyphs-v2.4/discarded-cross-script-draft'
Get-ChildItem -LiteralPath (Join-Path $taskRoot 'audit/runs') -Directory | Where-Object {
    $_.Name -match '^2026-10-15-\d{6}-[a-f0-9]{8}$' -and -not (Test-Path -LiteralPath (Join-Path $_.FullName 'seal.json'))
} | ForEach-Object { $candidates += $_.FullName }
foreach ($directory in @('tools','tests')) {
    Get-ChildItem -LiteralPath (Join-Path $taskRoot $directory) -Directory -Recurse -Filter '__pycache__' | ForEach-Object { $candidates += $_.FullName }
}
$records = @()
foreach ($candidate in $candidates) {
    if (-not (Test-Path -LiteralPath $candidate)) { continue }
    $resolved = (Resolve-Path -LiteralPath $candidate).Path
    if (-not $resolved.StartsWith($taskRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) { throw "Outside workspace: $resolved" }
    $item = Get-Item -LiteralPath $resolved
    if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) { throw "Refusing link: $resolved" }
    $files = if ($item.PSIsContainer) { @(Get-ChildItem -LiteralPath $resolved -Recurse -File) } else { @($item) }
    $blocked = @($files | Where-Object { $protected.Contains($_.FullName) })
    if ($blocked.Count) { Write-Output "Keep protected: $resolved"; continue }
    foreach ($file in $files) {
        $records += [pscustomobject]@{ path = [System.IO.Path]::GetRelativePath($taskRoot,$file.FullName).Replace('\','/'); bytes=$file.Length; sha256=(Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLower(); reason='obsolete generator, discarded draft, unsealed test run, or regenerable cache' }
    }
    if ($Apply) { Remove-Item -LiteralPath $resolved -Recurse -Force }
}
if ($Apply) {
    New-Item -ItemType Directory -Path (Split-Path $report) -Force | Out-Null
    @{files=$records;deletedFiles=$records.Count;deletedBytes=($records | Measure-Object bytes -Sum).Sum;preserved='Sealed artifact paths and audited input paths are protected.'} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $report -Encoding utf8
}
Write-Output "Files selected: $($records.Count); apply=$Apply"
