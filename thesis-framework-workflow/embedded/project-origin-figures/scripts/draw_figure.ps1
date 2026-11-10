param(
    [Parameter(Mandatory = $true)][string]$Python,
    [Parameter(Mandatory = $true)][string]$Script,
    [string[]]$ScriptArguments = @(),
    [switch]$CheckOnly
)
$ErrorActionPreference = 'Stop'
$resolvedScript = (Resolve-Path -LiteralPath $Script).Path
$resolvedPython = (Resolve-Path -LiteralPath $Python).Path
Push-Location -LiteralPath (Split-Path -Parent $resolvedScript)
try {
    if ($CheckOnly) {
        & $resolvedPython -B -X utf8 -c 'import ast,sys; from pathlib import Path; ast.parse(Path(sys.argv[1]).read_text(encoding="utf-8-sig")); print("Syntax checked; Origin not started")' $resolvedScript
    } else {
        & $resolvedPython -B -X utf8 $resolvedScript @ScriptArguments
    }
    if ($LASTEXITCODE -ne 0) { throw 'Figure script did not complete successfully' }
} finally {
    Pop-Location
}
