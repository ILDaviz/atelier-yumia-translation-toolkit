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
2. Double-click **`aggiorna_traduzione.bat`** (or run `python update_patch.py` in terminal).
3. Launch the game and set the text language to **Español** in the settings.

*That's it! All dialogues, menus, tutorials, items, and UI are now in Italian.*

---

## Game Updates / Steam Patches

If an official game update or Steam patch resets your language:
- Simply double-click **`aggiorna_traduzione.bat`** again.
- It will automatically re-extract, inject the translations, and update your game in ~15 seconds.

---

## Files Overview

| File | Description |
| :--- | :--- |
| **`project_yumia_es_en.json`** | Full dataset with all 29,007 translated segments. |
| **`aggiorna_traduzione.bat`** | Interactive CLI launcher for Windows (1-click menu). |
| **`yumia_cli.py`** | Interactive CLI wizard (installer, AI configurator, extractor). |
| **`update_patch.py`** | Automated installation & packaging script. |
| **`yumia_text_tool.py`** | A26 EBM and UI `message.json` extractor/injector. |
| **`yumia_translate.py`** | Multi-threaded AI translation tool (OpenAI / Ollama). |
| **`fix_accents.py`** | Font-safe character normalizer. |
| **`gust_tools/`** | Official Gust PAK unpacker and repacker binaries. |

---

## Manual Installation (Alternative)

If you prefer running commands manually:
```bash
# 1. Unpack PACK00.pak
cd pak_work && ..\gust_tools\gust_pak.exe "<GamePath>\Data\PACK00.pak" && cd ..

# 2. Inject Italian translation
python yumia_text_tool.py apply spa pak_work\master project_yumia_es_en.json

# 3. Repack and copy
cd pak_work && ..\gust_tools\gust_pak.exe PACK00.json && cd ..
copy /y pak_work\PACK00.pak "<GamePath>\Data\PACK00.pak"
```

---

## Disclaimer

Non-commercial fan translation project. *Atelier Yumia* is a trademark and copyright of **KOEI TECMO GAMES CO., LTD.** / **GUST**.
