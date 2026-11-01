@echo off
setlocal enabledelayedexpansion
title Atelier Yumia - Installatore Traduzione Italiana (v1.0.7)
chcp 65001 >nul
cls

echo ==================================================================
echo   ATELIER YUMIA: THE ALCHEMIST OF MEMORIES - PATCH ITALIANA
echo   Versione Gioco: v1.0.7  ^|  Lingua: Italiano (Slot Spagnolo)
echo ==================================================================
echo.

if not exist "%~dp0PACK00.pak" (
    echo [ERRORE] File 'PACK00.pak' non trovato nella cartella corrente!
    echo Assicurati di aver estratto tutti i file dello zip insieme.
    echo.
    pause
    exit /b 1
)

set "GAME_DIR="

:: 1. Controllo percorsi comuni Steam
if exist "C:\Program Files (x86)\Steam\steamapps\common\Atelier Yumia\Data\PACK00.pak" (
    set "GAME_DIR=C:\Program Files (x86)\Steam\steamapps\common\Atelier Yumia"
) else if exist "D:\SteamLibrary\steamapps\common\Atelier Yumia\Data\PACK00.pak" (
    set "GAME_DIR=D:\SteamLibrary\steamapps\common\Atelier Yumia"
) else if exist "E:\SteamLibrary\steamapps\common\Atelier Yumia\Data\PACK00.pak" (
    set "GAME_DIR=E:\SteamLibrary\steamapps\common\Atelier Yumia"
) else if exist "F:\SteamLibrary\steamapps\common\Atelier Yumia\Data\PACK00.pak" (
    set "GAME_DIR=F:\SteamLibrary\steamapps\common\Atelier Yumia"
) else if exist "G:\SteamLibrary\steamapps\common\Atelier Yumia\Data\PACK00.pak" (
    set "GAME_DIR=G:\SteamLibrary\steamapps\common\Atelier Yumia"
)

:: 2. Se non trovato, chiedi all'utente
if "%GAME_DIR%"=="" (
    echo [!] Cartella di Atelier Yumia non rilevata automaticamente.
    echo Trascina qui la cartella principale del gioco o incolla il percorso
    echo (es. C:\Program Files (x86)\Steam\steamapps\common\Atelier Yumia)
    echo.
    set /p "INPUT_DIR=Percorso cartella gioco: "
    set "INPUT_DIR=!INPUT_DIR:"=!"
    if exist "!INPUT_DIR!\Data\PACK00.pak" (
        set "GAME_DIR=!INPUT_DIR!"
    ) else (
        echo.
        echo [ERRORE] Il percorso specificato non contiene la cartella 'Data\PACK00.pak'!
        echo.
        pause
        exit /b 1
    )
)

echo [*] Cartella di gioco rilevata:
echo     "%GAME_DIR%"
echo.

set "DATA_DIR=%GAME_DIR%\Data"
set "ORIG_PAK=%DATA_DIR%\PACK00.pak.original"
set "DEST_PAK=%DATA_DIR%\PACK00.pak"

:: 3. Backup originale
if not exist "%ORIG_PAK%" (
    echo [*] Creazione copia di backup del file originale in corso...
    echo     PACK00.pak -^> PACK00.pak.original
    copy /y "%DEST_PAK%" "%ORIG_PAK%" >nul
    if errorlevel 1 (
        echo [ERRORE] Impossibile creare il backup. Verifica i permessi della cartella.
        pause
        exit /b 1
    )
    echo     [OK] Backup completato!
) else (
    echo [*] Backup originale gia' presente (PACK00.pak.original).
)

:: 4. Copia del file tradotto
echo [*] Installazione della traduzione italiana in corso...
copy /y "%~dp0PACK00.pak" "%DEST_PAK%" >nul
if errorlevel 1 (
    echo.
    echo [ERRORE] Impossibile copiare il file tradotto.
    echo Assicurati che il gioco sia chiuso prima di installare!
    echo.
    pause
    exit /b 1
)

echo.
echo ==================================================================
echo   INSTALLAZIONE COMPLETATA CON SUCCESSO!
echo ==================================================================
echo.
echo   COME ATTIVARE L'ITALIANO:
echo   1. Avvia Atelier Yumia su Steam.
echo   2. Nelle impostazioni del gioco, seleziona la lingua del testo:
echo      -^> "Español" (Spagnolo)
echo.
echo   Tutti i testi (storia, menu, tutorial, dialoghi e scelte)
echo   appariranno ora interamente in ITALIANO!
echo ==================================================================
echo.
pause
