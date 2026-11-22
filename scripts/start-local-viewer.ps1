[CmdletBinding()]
param([string]$DataRoot = 'D:\PACS-HIS\local')
$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$localRoot = [IO.Path]::GetFullPath($DataRoot)
if ($localRoot.StartsWith($repoRoot, [StringComparison]::OrdinalIgnoreCase) -or $localRoot.StartsWith('\\')) {
    throw 'Use um disco local fora do repositorio para os exames e segredos.'
}
if ($localRoot -eq [IO.Path]::GetPathRoot($localRoot)) { throw 'Use uma subpasta exclusiva, nunca a raiz do disco.' }
$marker = Join-Path $localRoot '.pacs-his-local'
if ((Test-Path -LiteralPath $localRoot) -and !(Test-Path -LiteralPath $marker)) {
    if (@(Get-ChildItem -LiteralPath $localRoot -Force).Count -gt 0) {
        throw 'Pasta ja possui outros arquivos. Escolha uma pasta exclusiva vazia.'
    }
}
New-Item -ItemType Directory -Path $localRoot -Force | Out-Null
if (!(Test-Path -LiteralPath $marker)) {
    $sid = [Security.Principal.WindowsIdentity]::GetCurrent().User.Value
    & icacls $localRoot /inheritance:r /grant:r "*${sid}:(OI)(CI)F" '*S-1-5-18:(OI)(CI)F' | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel restringir a pasta local.' }
    [IO.File]::WriteAllText($marker, 'pacs-his-local-v1')
}
if ([IO.File]::ReadAllText($marker) -ne 'pacs-his-local-v1') { throw 'Marcador local desconhecido.' }
foreach ($folder in @('archive', 'secrets')) {
    New-Item -ItemType Directory -Path (Join-Path $localRoot $folder) -Force | Out-Null
}
$hostIdFile = Join-Path $localRoot 'hostid'
if (!(Test-Path -LiteralPath $hostIdFile)) {
    [IO.File]::WriteAllText($hostIdFile, ([guid]::NewGuid().ToString('N').Substring(0, 8) + "`n"))
}
$secretFile = Join-Path $localRoot 'secrets\orthanc-users.json'
if (!(Test-Path -LiteralPath $secretFile)) {
    $bytes = New-Object byte[] 24
    $rng = [Security.Cryptography.RandomNumberGenerator]::Create()
    try { $rng.GetBytes($bytes) } finally { $rng.Dispose() }
    $password = ([BitConverter]::ToString($bytes)).Replace('-', '').ToLowerInvariant()
    $users = @{RegisteredUsers = @{local = $password}} | ConvertTo-Json -Depth 3
    [IO.File]::WriteAllText($secretFile, $users, (New-Object Text.UTF8Encoding($false)))
}
$credential = Get-Content -Raw -LiteralPath $secretFile | ConvertFrom-Json
if (!$credential.RegisteredUsers.local) { throw 'Credencial local invalida; arquivo preservado.' }
$accessFile = Join-Path $localRoot 'ACESSO-LOCAL.txt'
$accessText = "Importacao: http://127.0.0.1:8042/`r`nVisualizador: http://127.0.0.1:8042/ohif/`r`nUsuario: local`r`nSenha: $($credential.RegisteredUsers.local)`r`nUso local. Nao publicar este arquivo."
[IO.File]::WriteAllText($accessFile, $accessText, (New-Object Text.UTF8Encoding($false)))
$env:PACS_LOCAL_ROOT = $localRoot.Replace('\', '/')
$compose = Join-Path $repoRoot 'infra\local\compose.yaml'
& docker info --format '{{.ServerVersion}}' 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Inicie o Docker Desktop e execute novamente.' }
& docker compose -f $compose config --quiet
if ($LASTEXITCODE -ne 0) { throw 'Configuracao de containers invalida.' }
& docker compose -f $compose up -d --wait --wait-timeout 120
if ($LASTEXITCODE -ne 0) { throw 'Servico ainda nao ficou saudavel. Confira o container pacs-his-local.' }
Write-Output 'Importacao: http://127.0.0.1:8042/'
Write-Output 'Visualizador: http://127.0.0.1:8042/ohif/'
Write-Output "Credenciais locais: $accessFile"
