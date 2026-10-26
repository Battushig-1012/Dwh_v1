# Apply DWH SQL init scripts to a local PostgreSQL instance.
# Usage: .\scripts\init_db.ps1 -Connection "postgresql://dwh_admin:pass@localhost:5432/bbsb_dwh"

param(
    [Parameter(Mandatory = $true)]
    [string]$Connection
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$files = Get-ChildItem "$root\dwh\init\*.sql" | Sort-Object Name

foreach ($f in $files) {
    Write-Host "Applying $($f.Name) ..."
    & psql $Connection -f $f.FullName
    if ($LASTEXITCODE -ne 0) { throw "Failed on $($f.Name)" }
}

Write-Host "DWH schemas ready."
