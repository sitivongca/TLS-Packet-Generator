# config.ps1
# Script will modify Activate.ps1, openssl.cnf, and /configdata.pm

Write-Host ""
Write-Host "SSLv3 Enabler Install for OpenSSL" -ForegroundColor Green
Write-Host "---------------------------------" -ForegroundColor Yellow
Write-Host ""

$parentDir = [System.IO.Path]::GetFullPath("$PSScriptRoot\..\")

try {
    # Path to openssl config to enable SSLv3
    $opensslPath = "$parentDir.venv\openssl\openssl.cnf"
    # Path to openssl source folder to compile for SSLv3
    $configDataPath = Get-ChildItem -Path "$parentDir.venv\" -Directory | Where-Object { $_.Name -like "openssl-*" } | Select-Object -First 1
    $configPath = Join-Path "$parentDir.venv\" $configDataPath
    $configPath += "/configdata.pm"
    # Path venv activate script for paths
    $activatePath = Join-Path $parentDir ".venv\Scripts\Activate.ps1" 

    Write-Host "Paths found:"
    Write-Host "$($opensslPath)`n$($configPath)`n$($activatePath)"

    # Use VS build tools for make
    Write-Host "Configuring OpenSSL.." -ForegroundColor Green
    & "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat x86_amd64"
    perl Configure VC-WIN64A --prefix="$parentDir/.venv/opensll" --openssldir="$parentDir/.venv/opensll" enable-ssl3 enable-ssl3-method
    nmake
    nmake install

    # Remove SSL removers
    Write-Host "Removing no-ssl3 options from configdata.pm..." -ForegroundColor Green
    $openConfig = Get-Content $configPath
    $openConfig = $openConfig -replace 'no-ssl3-method', ''
    $openConfig = $openConfig -replace 'no-ssl3', ''
    Set-Content $configPath $openConfig

    # Edit cnf file
    $content = Get-Content $opensslPath

    if($content.IndexOf({$_ -match "openssl_conf = default_conf"}) -eq $true){
        Write-Host("Configs already set up.")
        exit 1
    }

    $index= $content.IndexOf({$_ -match "openssl_init"})
    $config = "openssl_conf = default_conf"

    if($index -ne $null){
        # Append 1 line after init
        $content = $content[0..$index] + $config + $content[($index + 1)..$content.Length]
        Set-Content -Path $opensslPath -Value $content
    } else {
        Add-Content -Path $opensslPath -Value @('openssl_conf = default_conf')
    }

    Add-Content -Path $opensslPath -Value @(       
        '[ default_conf ]'
        'ssl_conf = ssl_sect'
        '[ssl_sect]'
        'system_default = system_default_sect'
        '[system_default_sect]'
        'MinProtocol = SSLv3'
        'CipherString = DEFAULT:@SECLEVEL=0'
    )

    # Edit Activate.ps1
    $content = Get-Content $activatePath
    $index= $content.IndexOf({$_ -match "# SIG # Begin signature block"})
    $config = @"
    # Add Environment Paths

    # Rust
    `$Env:PATH=`"$HOME\.cargo\bin;$Env:PATH`"

    `$parentDir = [System.IO.Path]::GetFullPath(`"$PSScriptRoot\..\..`\")

    # OpenSSL paths
    `$Env:OPENSSL_DIR = `"$parentDir\.venv\openssl`"
    `$Env:OPENSSL_CONF = `"$parentDir\.venv\openssl\openssl.cnf`"
    `$Env:SSL_CERT_DIR = `"$parentDir\.venv\openssl\lib`"
    `$Env:PATH = `"$parentDir\.venv\openssl\bin;$Env:PATH`"
    `$Env:INCLUDE = `"$parentDir\.venv\openssl\include;$Env:INCLUDE`"
    `$Env:LIB = `"$parentDir\.venv\openssl\lib;$Env:LIB`"

    # Set MSVC and Windows SDK paths
    `$Env:INCLUDE = `"C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\ucrt;$Env:INCLUDE`"
    `$Env:LIB = `"C:\Program Files (x86)\Windows Kits\10\Lib\10.0.22621.0\ucrt\x64;$Env:LIB`"
    `$Env:INCLUDE = `"C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\um;$Env:INCLUDE`"
    `$Env:LIB = `"C:\Program Files (x86)\Windows Kits\10\Lib\10.0.22621.0\um\x64;$Env:LIB`"
    `$Env:INCLUDE = `"D:\Other\Visual studio\VC\Tools\MSVC\14.43.34808\include;$Env:INCLUDE`"
    `$Env:LIB = `"D:\Other\Visual studio\VC\Tools\MSVC\14.43.34808\lib;$Env:LIB`"
"@    

    if($index -ne $null){
        # Append 1 line before # SIG
        $content = $content[0..$index-1] + $config + $content[($index + 1)..$content.Length]
        Set-Content -Path $activatePath -Value $content
    }
    else{
        Write-Host "Index was null. Exiting program." -ForegroundColor Red
        exit(1)
    }

    Write-Host "OpenSSL configured successfully, please continue compiling the other dependencies." -ForegroundColor Green

} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit(1)
}

Write-Host ""
Write-Host "Press Enter key to continue." -ForegroundColor Cyan
Read-Host
exit 0