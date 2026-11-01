# Developer Guide & Translation Toolkit Documentation

This document describes the technical architecture, development workflows, and tools behind the **Atelier Yumia Translation Toolkit**.

---

## 🏗️ Architecture Overview

Atelier Yumia (Gust / Koei Tecmo) stores localized game text across two primary formats inside the main archive `Data/PACK00.pak`:
1. **Dialogue & Event Scripts (`.ebm`):** Binary bytecode files containing dialogue lines, character names, and player interactive branching choices (`<SEL_...><CR>`).
2. **System & UI Messages (`fixed_data/message/message.json`):** JSON dictionary containing UI menus, tutorial texts, item names, descriptions, and synthesis traits.

The toolkit provides an end-to-end Python pipeline to unpack, extract, normalize, translate (manually or via AI), and repack these files cleanly.

```
       PACK00.pak (Vanilla)
               │
               ▼  [gust_pak.exe]
         pak_work/master/
               │
               ├── spa/eventmessagedata/*.ebm
               └── spa/fixed_data/message/message.json
                       │
       project_yumia_es_en.json (29,007 segments)
               │
               ▼  [yumia_text_tool.py & apply_choices.py]
         pak_work/master/ (Patched)
               │
               ▼  [gust_pak.exe PACK00.json]
       PACK00.pak (Patched Italian Release)
```

---

## 📋 Prerequisites & Environment Setup

### 1. Requirements
- Python 3.10 or higher
- Legitimate PC Steam installation of *Atelier Yumia*
- Optional: OpenAI API Key (or local Ollama instance) for running AI translation tasks

### 2. Configuration (`.env`)
Copy `.env.example` to `.env` in the project root:
```ini
# OpenAI / ChatGPT API Key (Optional, for running AI translation)
OPENAI_API_KEY=sk-proj-...

# Optional Configurations:
OPENAI_MODEL=gpt-6-luna
OPENAI_BASE_URL=https://api.openai.com/v1
```
*(The `.env` file is protected by `.gitignore` and will never be tracked by Git).*

### 3. Game Directory Configuration (`config.json`)
The toolkit automatically detects your Steam game directory on startup and saves it to `config.json`. You can also configure it manually:
```json
{
  "game_dir": "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Atelier Yumia"
}
```

---

## 🗂️ Project Structure

| File / Folder | Role |
| :--- | :--- |
| **`run_toolkit.bat`** | Windows 1-click launcher for the interactive CLI menu. |
| **`project_yumia_es_en.json`** | Master translation dataset containing all 29,007 translatable game segments. |
| **`glossary.json`** | Terminology consistency dictionary for characters, locations, and alchemy terms. |
| **`src/yumia_cli.py`** | Interactive console wizard with options for installing, translating, extracting, and packaging. |
| **`src/update_patch.py`** | Automated pipeline: extracts vanilla PAK, normalizes fonts, injects Italian text and choices, and repacks. |
| **`src/package_release.py`** | Automated release builder: compresses the release folder into `.zip` and prints GitHub release notes. |
| **`src/yumia_text_tool.py`** | Core binary parser: extracts/injects strings into `.ebm` and `message.json`. |
| **`src/apply_choices.py`** | Specialized injector for player interactive choices (`<SEL_...><CR>`). |
| **`src/yumia_translate.py`** | Concurrent multi-threaded AI translation runner (OpenAI / Ollama / DeepSeek). |
| **`src/fix_accents.py`** | Normalizes accented characters (`è` ➔ `e'`) for Gust bitmap font compatibility. |
| **`src/game_config.py`** | Steam directory auto-detection and environment loader. |
| **`gust_tools/`** | Bundled native binaries for Gust archive extraction and repacking (`gust_pak.exe`, etc.). |

---

## 🛠️ Development Workflows

### 1. Interactive CLI (`run_toolkit.bat`)
To launch the full interactive suite:
```bash
python src/yumia_cli.py
```
Menu options:
- **`[1] Install / Update translation in game`**: Runs the complete update pipeline and installs to Steam.
- **`[2] AI Translation`**: Configure and run parallel translation passes.
- **`[3] Create downloadable ZIP release package`**: Packages a distribution-ready `.zip` archive.
- **`[4] Extract raw texts from game`**: Extracts game assets to a fresh `project.json`.
- **`[5] Change / Set game folder path`**: Change the target Steam game directory.

---

### 2. Updating / Recompiling the Patch
To re-extract, inject translations, and repack `PACK00.pak`:
```bash
python src/update_patch.py
```
This script will:
1. Detect or verify the game directory and back up the vanilla `PACK00.pak` as `PACK00.pak.original`.
2. Extract the vanilla package into `pak_work/`.
3. Normalize character encodings with `fix_accents.py`.
4. Inject dialogues and UI messages with `yumia_text_tool.py apply`.
5. Inject all 128 player choices across 59 `.ebm` files with `apply_choices.py`.
6. Repack `PACK00.pak` using `gust_pak.exe` and deploy it to the game directory.

---

### 3. Building a Downloadable Release Package
To create a clean distribution archive:
```bash
python src/package_release.py
```
This script:
1. Bundles `PACK00.pak`, `Installa_Patch_ITA.bat`, `Ripristina_Originale.bat`, and `ISTRUZIONI.txt`.
2. Compresses the package into `Atelier_Yumia_v1.0.7_ITA.zip` (~71 MB).
3. Computes the SHA-256 integrity hash.
4. Copies the archive directly to your Desktop.
5. Prints the ready-to-paste GitHub Release title, tag, and markdown description.

---

### 4. Running AI Translations (`yumia_translate.py`)
To translate new or modified segments using OpenAI or compatible APIs:
```bash
python src/yumia_translate.py project_yumia_es_en.json \
    --endpoint https://api.openai.com/v1 \
    --model gpt-6-luna \
    --workers 15 \
    --glossary glossary.json
```
For local execution via Ollama:
```bash
python src/yumia_translate.py project_yumia_es_en.json \
    --endpoint http://localhost:11434/v1 \
    --model qwen2.5:7b-instruct \
    --workers 6 \
    --glossary glossary.json
```

---

## 📐 Translation & Font Guidelines

1. **Tag Preservation:**
   - Always preserve tags such as `<SEL_...><CR>`, `<CLEG>...</CLNR>`, and placeholders like `%s`, `{0}`, and `\n`.
   - Never remove or translate player choice tags (e.g. `<SEL_CM01_010_1_A><CR>`).

2. **Font Compatibility (Accents):**
   - The game's engine uses a bitmap font that lacks glyphs for accented vowels (`è`, `à`, `ù`, `ì`, `ò`).
   - Use apostrophes instead (`e'`, `a'`, `u'`, `i'`, `o'`). Run `src/fix_accents.py` to normalize automatically.

3. **Dual-Reference Context:**
   - Translations use Spanish as the source slot (`src`) and English as a reference (`ref`) to ensure accurate terminology and tone.
