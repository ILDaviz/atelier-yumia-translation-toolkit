# Atelier Yumia: Italian Translation

Complete 100% Italian fan translation for **Atelier Yumia: The Alchemist of Memories & the Envisioned Land** (Steam / PC).

Replaces the **Spanish** language slot with clean, natural Italian.

---

## Quick Install (1-Click)

### Requirements
- Python 3.10+
- Game installed on Steam

### Installation
1. Clone or download this repository.
2. Double-click **`run_toolkit.bat`** and choose **`[1]`** to install the ready translation.
3. Launch the game and set the text language to **Español** in the settings.

*That's it! All dialogues, menus, tutorials, items, and UI are now in Italian.*

---

## Toolkit Menu Options (`run_toolkit.bat`)

Running `run_toolkit.bat` (or `python src/yumia_cli.py`) opens an interactive menu:

- **`[1] Install / Update translation in game`**: Automatically injects all 29,007 Italian translations into the game (~15 seconds, ready-to-play).
- **`[2] AI Translation`**: Interactive wizard to run or customize translations with AI. *(Recommended model: **`gpt-6-luna`** via OpenAI — exceptionally fast, high accuracy, and costs under $0.50 for the entire game).*
- **`[3] Extract raw texts from game`**: Extracts dialogues and UI text directly from game files into a new project JSON (useful when new DLCs or major game updates arrive).
- **`[4] Change / Set game folder path`**: Displays the currently detected Steam folder and lets you set a custom path if needed.

---

## Game Updates / Steam Patches

If an official game update or Steam patch resets your language:
- Simply run **`run_toolkit.bat`** and choose **`[1]`** again (or run `python src/update_patch.py`).
- It will automatically re-extract, inject the translations, and update your game in ~15 seconds.

---

## Files Overview

| File / Folder | Description |
| :--- | :--- |
| **`project_yumia_es_en.json`** | Full dataset with all 29,007 translated segments. |
| **`run_toolkit.bat`** | Interactive CLI launcher for Windows (1-click menu). |
| **`src/yumia_cli.py`** | Interactive CLI wizard (installer, AI configurator, extractor). |
| **`src/update_patch.py`** | Automated installation & packaging script. |
| **`src/yumia_text_tool.py`** | A26 EBM and UI `message.json` extractor/injector. |
| **`src/yumia_translate.py`** | Multi-threaded AI translation tool (OpenAI / Ollama). |
| **`src/fix_accents.py`** | Font-safe character normalizer. |
| **`gust_tools/`** | Official Gust PAK unpacker and repacker binaries. |

---

## Manual Installation (Alternative)

If you prefer running commands manually:
```bash
# 1. Unpack PACK00.pak
cd pak_work && ..\gust_tools\gust_pak.exe "<GamePath>\Data\PACK00.pak" && cd ..

# 2. Inject Italian translation
python src/yumia_text_tool.py apply spa pak_work\master project_yumia_es_en.json

# 3. Repack and copy
cd pak_work && ..\gust_tools\gust_pak.exe PACK00.json && cd ..
copy /y pak_work\PACK00.pak "<GamePath>\Data\PACK00.pak"
```

---

## Disclaimer

Non-commercial fan translation project. *Atelier Yumia* is a trademark and copyright of **KOEI TECMO GAMES CO., LTD.** / **GUST**.
