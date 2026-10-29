param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('C2-D01', 'C2-D02', 'C2-D03')]
    [string]$Figure,
    [string]$ThesisRoot = 'C:\Users\zwzhu\Desktop\萝卜论文\markov_drl\大论文',
    [switch]$CheckOnly,
    [switch]$KeepOpen
)

$ErrorActionPreference = 'Stop'
$runtime = Join-Path $env:USERPROFILE '.local\share\editaplot\editaplot-main\runtime'
if ($env:EDITAPLOT_ENGINE_HOME) { $runtime = $env:EDITAPLOT_ENGINE_HOME }
$python = Join-Path $runtime '.editaplot-venv\Scripts\python.exe'
$chapter = Join-Path $ThesisRoot '图表文件夹\01_Origin作图\第2章_原理与建模'
$script = Join-Path $chapter ($Figure.Replace('-', '_') + '.py')
foreach ($required in @($python, $chapter, $script)) {
    if (-not (Test-Path -LiteralPath $required)) { throw "Missing: $required" }
}
$priorUtf8 = $env:PYTHONUTF8
$priorEncoding = $env:PYTHONIOENCODING
try {
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    Push-Location -LiteralPath $chapter
    try {
        if ($CheckOnly) {
            $probe = @'
import ast, json, sys
from pathlib import Path
ast.parse(Path(sys.argv[1]).read_text(encoding="utf-8"))
figure = sys.argv[2]
if figure == "C2-D03":
    from C2_D03 import read_sources, step_nodes, verify_staircase
    panels = read_sources()
    for p in panels:
        for c in p["curves"]:
            verify_staircase(c["xy"], step_nodes(c["xy"], p["xmax"], p["direction"]), p["direction"])
else:
    from C2_load_origin import get_data
    get_data(figure)
print(json.dumps({"figure": figure, "source_and_syntax": "passed", "origin_started": False}))
'@
            & $python -c $probe $script $Figure
        } else {
            $arguments = @($script)
            if ($Figure -ne 'C2-D03') {
                $arguments = @((Join-Path $chapter 'C2_load_origin.py'), '--figure', $Figure)
            }
            if ($KeepOpen) { $arguments += '--keep-open' }
            & $python @arguments 2>&1 | Tee-Object -FilePath ($Figure.Replace('-', '_') + '_run.log') -Append
        }
        if ($LASTEXITCODE -ne 0) { throw "Figure task failed, exit code $LASTEXITCODE" }
    } finally { Pop-Location }
} finally {
    $env:PYTHONUTF8 = $priorUtf8
    $env:PYTHONIOENCODING = $priorEncoding
}
