@echo off
setlocal enabledelayedexpansion
title Atelier Yumia - Ripristino Lingua Originale
chcp 65001 >nul
cls

echo ==================================================================
echo   ATELIER YUMIA - RIPRISTINO FILE ORIGINALE
echo ==================================================================
echo.

set "GAME_DIR="

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

if "%GAME_DIR%"=="" (
    echo Trascina qui la cartella di Atelier Yumia:
    set /p "INPUT_DIR=Percorso: "
    set "INPUT_DIR=!INPUT_DIR:"=!"
    set "GAME_DIR=!INPUT_DIR!"
)

set "ORIG_PAK=%GAME_DIR%\Data\PACK00.pak.original"
set "DEST_PAK=%GAME_DIR%\Data\PACK00.pak"

if not exist "%ORIG_PAK%" (
    echo [ERRORE] Nessun backup trovato in:
    echo "%ORIG_PAK%"
    echo.
    echo Per ripristinare il gioco originale, puoi usare la funzione di Steam:
    echo Tasto destro sul gioco -^> Proprieta' -^> File installati -^> Verifica integrita' dei file di gioco.
    echo.
    pause
    exit /b 1
)

echo [*] Ripristino del file originale in corso...
copy /y "%ORIG_PAK%" "%DEST_PAK%" >nul
if errorlevel 1 (
    echo [ERRORE] Impossibile ripristinare il file. Chiudi il gioco prima di procedere.
    pause
    exit /b 1
)

echo.
echo [OK] File originale ripristinato con successo!
echo.
pause
