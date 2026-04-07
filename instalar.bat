@echo off
setlocal EnableDelayedExpansion
color 0A
title Instalador - Proctoring System v0.3
cls

:: ============================================================================
:: INSTALADOR COMPLETO - PROCTORING SYSTEM v0.3
:: Substitui: instalar.bat + instalar_tudo.bat
:: ============================================================================

echo ========================================
echo   PROCTORING SYSTEM - INSTALADOR
echo   Versao 0.3
echo ========================================
echo.

:: ----------------------------------------------------------------------------
:: PASSO 1: Verificar Python
:: ----------------------------------------------------------------------------
echo [1/8] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] Python nao encontrado!
    echo.
    echo Instale o Python 3.8+ em: https://python.org
    echo MARQUE A OPCAO: "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python detectado: %PYTHON_VERSION%

:: Mostrar caminho do Python
echo [INFO] Caminho:
python -c "import sys; print('        ' + sys.executable)"
echo.

:: ----------------------------------------------------------------------------
:: PASSO 2: Verificar pip
:: ----------------------------------------------------------------------------
echo [2/8] Verificando pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] pip nao encontrado!
    echo.
    echo Execute: python -m ensurepip --upgrade
    echo.
    pause
    exit /b 1
)
echo [OK] pip detectado
echo.

:: ----------------------------------------------------------------------------
:: PASSO 3: Atualizar pip
:: ----------------------------------------------------------------------------
echo [3/8] Atualizando pip...
python -m pip install --upgrade pip --quiet 2>nul
if errorlevel 1 (
    echo [ALERTA] Nao foi possivel atualizar o pip
) else (
    echo [OK] pip atualizado
)
echo.

:: ----------------------------------------------------------------------------
:: PASSO 4: Remover bibliotecas problemáticas
:: ----------------------------------------------------------------------------
echo [4/8] Removendo bibliotecas problemáticas...
echo       (Pillow, pyautogui, pyscreeze)
echo.

pip uninstall pillow -y >nul 2>&1
pip uninstall pillow -y >nul 2>&1
pip uninstall pyautogui -y >nul 2>&1
pip uninstall pyscreeze -y >nul 2>&1

echo [OK] Bibliotecas antigas removidas
echo.

:: ----------------------------------------------------------------------------
:: PASSO 5: Instalar novas dependências
:: ----------------------------------------------------------------------------
echo [5/8] Instalando dependencias...
echo       Aguarde, isso pode levar alguns minutos...
echo.

echo       Instalando: mss (captura de tela leve)...
python -m pip install mss --quiet 2>nul
if errorlevel 1 (
    echo [ERRO] Falha ao instalar mss!
    goto :install_error
)

echo       Instalando: pyzipper, pycryptodomex (segurança)...
python -m pip install pyzipper pycryptodomex --quiet 2>nul
if errorlevel 1 (
    echo [ERRO] Falha ao instalar pyzipper!
    goto :install_error
)

echo       Instalando: pynput, pyperclip, psutil, pygetwindow...
python -m pip install pynput pyperclip psutil pygetwindow requests python-dateutil --quiet 2>nul
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias!
    goto :install_error
)

echo [OK] Todas as bibliotecas instaladas
echo.

:: ----------------------------------------------------------------------------
:: PASSO 6: Criar estrutura de pastas
:: ----------------------------------------------------------------------------
echo [6/8] Criando estrutura de pastas...

if not exist "core" mkdir core
if not exist "sensors" mkdir sensors
if not exist "indicators" mkdir indicators
if not exist "config" mkdir config
if not exist "logs" mkdir logs
if not exist "screenshots" mkdir screenshots
if not exist "secure_logs" mkdir secure_logs
if not exist "utils" mkdir utils
if not exist "keys" mkdir keys

echo [OK] Pastas criadas
echo.

:: ----------------------------------------------------------------------------
:: PASSO 7: Criar arquivos __init__.py
:: ----------------------------------------------------------------------------
echo [7/8] Criando arquivos __init__.py...

if not exist "core\__init__.py" echo # Pacote: core > core\__init__.py
if not exist "sensors\__init__.py" echo # Pacote: sensors > sensors\__init__.py
if not exist "indicators\__init__.py" echo # Pacote: indicators > indicators\__init__.py
if not exist "config\__init__.py" echo # Pacote: config > config\__init__.py
if not exist "utils\__init__.py" echo # Pacote: utils > utils\__init__.py

echo [OK] Arquivos __init__.py criados
echo.

:: ----------------------------------------------------------------------------
:: PASSO 8: Criar arquivo de configuração
:: ----------------------------------------------------------------------------
echo [8/8] Configurando sistema...

if not exist "config\security_config.json" (
    echo {
    echo   "admin_password": "MudeEstaSenha123!",
    echo   "zip_encryption": "AES256",
    echo   "auto_send_to_server": false,
    echo   "server_url": "https://api.faculdade.edu.br/proctoring",
    echo   "retention_days": 180
    echo } > config\security_config.json
    echo [OK] config/security_config.json criado
    echo [ALERTA] MUDE A SENHA antes de usar em producao!
) else (
    echo [OK] config/security_config.json ja existe
)
echo.

:: ----------------------------------------------------------------------------
:: VERIFICAÇÃO FINAL
:: ----------------------------------------------------------------------------
echo ========================================
echo   VERIFICANDO INSTALACAO
echo ========================================
echo.

set VERIFICACAO_OK=1

python -c "import mss" 2>nul
if errorlevel 1 (
    echo [ERRO] mss nao instalado
    set VERIFICACAO_OK=0
) else (
    echo [OK] mss
)

python -c "import pyzipper" 2>nul
if errorlevel 1 (
    echo [ERRO] pyzipper nao instalado
    set VERIFICACAO_OK=0
) else (
    echo [OK] pyzipper
)

python -c "import pynput" 2>nul
if errorlevel 1 (
    echo [ERRO] pynput nao instalado
    set VERIFICACAO_OK=0
) else (
    echo [OK] pynput
)

python -c "import pyperclip" 2>nul
if errorlevel 1 (
    echo [ERRO] pyperclip nao instalado
    set VERIFICACAO_OK=0
) else (
    echo [OK] pyperclip
)

python -c "import psutil" 2>nul
if errorlevel 1 (
    echo [ERRO] psutil nao instalado
    set VERIFICACAO_OK=0
) else (
    echo [OK] psutil
)

python -c "import pygetwindow" 2>nul
if errorlevel 1 (
    echo [ERRO] pygetwindow nao instalado
    set VERIFICACAO_OK=0
) else (
    echo [OK] pygetwindow
)

echo.

:: ----------------------------------------------------------------------------
:: CONCLUSÃO
:: ----------------------------------------------------------------------------
if "%VERIFICACAO_OK%"=="1" (
    echo ========================================
    echo   INSTALACAO CONCLUIDA COM SUCESSO!
    echo ========================================
    echo.
    echo Proximos passos:
    echo   1. EDITE config/security_config.json
    echo      e MUDE a senha do administrador!
    echo.
    echo   2. Execute: python test_geral.py
    echo      (para verificar tudo)
    echo.
    echo   3. Execute: python main.py
    echo      (para iniciar o sistema)
    echo.
    echo Documentacao:
    echo   - Leia o README.md
    echo   - Consulte LICENCA.md
    echo.
) else (
    echo ========================================
    echo   INSTALACAO COMPLETA COM AVISOS
    echo ========================================
    echo.
    echo Algumas bibliotecas podem nao estar
    echo instaladas corretamente.
    echo.
    echo Tente:
    echo   1. Executar como Administrador
    echo   2. Usar: pip install --user -r requirements.txt
    echo.
)

echo ========================================
echo.
pause
exit /b 0

:: ----------------------------------------------------------------------------
:: TRATAMENTO DE ERROS
:: ----------------------------------------------------------------------------
:install_error
echo.
echo ========================================
echo   ERRO NA INSTALACAO
echo ========================================
echo.
echo Possiveis solucoes:
echo   1. Execute como Administrador
echo   2. Verifique sua conexao com a internet
echo   3. Use: pip install --user [nome_pacote]
echo.
echo Para ajuda, execute:
echo   python verificar.py
echo.
pause
exit /b 1