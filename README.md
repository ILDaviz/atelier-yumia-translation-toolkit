# Atelier Yumia: Italian Translation Toolkit (ES/EN → IT)

Complete fan-translation toolchain and localization dataset for **Atelier Yumia: The Alchemist of Memories & the Envisioned Land** (A26 / Gust engine).

---

## Highlights

- **Dual-Language Pipeline (ES + EN → IT):** Translates primarily from Spanish for natural Romance-language syntax, syllable timing, and lip-sync cadence, while simultaneously cross-referencing English to eliminate false friends and ambiguities.
- **100% Text Coverage:** Covers all **29,007 segments** (~106,000 dialogue words + ~185,000 UI, menu, synthesis, item, and tutorial words).
- **Font-Safe Accent Normalization:** Built-in normalization (`fix_accents.py`) converts accented vowels to ASCII letters with apostrophes (`e'`, `piu'`, `pero'`), completely eliminating missing glyphs / square boxes on game font atlases.
- **Concurrent AI Translation:** Multi-threaded translator (`yumia_translate.py`) supporting any OpenAI-compatible endpoint (OpenAI GPT-4o / GPT-5 / Luna models, Ollama, LM Studio, etc.) with automatic resume and tag-preservation verification.

---

## Repository Structure

```text
├── project_yumia_es_en.json   # Complete translated project (all 29,007 segments in Italian)
├── yumia_text_tool.py          # Extractor/injector for A26 EBM dialogues and message.json UI
├── yumia_translate.py          # Multi-threaded AI translation runner (OpenAI / Ollama)
├── fix_accents.py              # Font-compatibility normalizer for accents and typographic symbols
├── build_glossary_draft.py     # Term frequency & proper-noun extraction tool
├── glossary.json               # Curated term/character name glossary
├── gust_tools/                 # Gust binary utilities (gust_pak, gust_ebm, etc.)
└── README.md                   # Documentation (English)
```

---

## Fast Track: Installing the Translation

If you just want to play the game in Italian using the included pre-translated project:

### 1. Requirements
- Python 3.10+
- The game installed via Steam (`Atelier Yumia`)

### 2. Extract `PACK00.pak`
Locate `PACK00.pak` inside your game directory:  
`<SteamLibrary>\steamapps\common\Atelier Yumia\Data\PACK00.pak`

Create a folder named `pak_work`, copy `PACK00.pak` there, and extract it:
```bash
mkdir pak_work
copy "<GamePath>\Data\PACK00.pak" pak_work\
cd pak_work
..\gust_tools\gust_pak.exe PACK00.pak
cd ..
```

### 3. Apply the Italian Translation
Apply the Italian text to the Spanish slot:
```bash
python yumia_text_tool.py apply spa pak_work\master project_yumia_es_en.json
```

### 4. Rebuild `PACK00.pak`
```bash
cd pak_work
..\gust_tools\gust_pak.exe PACK00.json
cd ..
```

### 5. Install to the Game
1. Make a backup of the original `PACK00.pak` in your game's `Data\` folder (e.g., rename to `PACK00.pak.original`).
2. Copy `pak_work\PACK00.pak` to `<GamePath>\Data\PACK00.pak`.
3. Launch the game and set the language in settings to **Español**. All text, menus, dialogues, and system notices will be in **Italian**!

---

## Full Pipeline: Translating From Scratch

If a game update is released or you want to translate into another language:

### 1. Extract Project from Game Assets
```bash
python yumia_text_tool.py extract spa eng pak_work\master project.json
```

### 2. Generate Glossary
```bash
python build_glossary_draft.py project.json glossary_draft.md
```
Edit or create `glossary.json` with your custom terminology:
```json
{
  "alquimia": "alchimia",
  "maná": "mana"
}
```

### 3. Run Concurrent Translation
```bash
# Using OpenAI API:
python yumia_translate.py project.json \
  --endpoint https://api.openai.com/v1 \
  --model gpt-6-luna \
  --api-key YOUR_API_KEY \
  --workers 15 \
  --glossary glossary.json

# Using local Ollama:
python yumia_translate.py project.json \
  --endpoint http://localhost:11434/v1 \
  --model qwen2.5:7b-instruct \
  --workers 8 \
  --glossary glossary.json
```
*Note: The script is fully resumable; re-running it will only translate remaining/failed segments.*

### 4. Font Compatibility Pass
```bash
python fix_accents.py project.json
```
Normalizes unmapped grave accents and directional quotes to font-safe glyphs.

### 5. Apply and Pack
Follow the steps in [Fast Track](#fast-track-installing-the-translation) to inject and repack.

---

## Technical Notes

### Why Spanish as Source?
JRPG English localizations frequently compress dialogue lengths and lose honorific/grammatical register (e.g. *you* collapses *tu/Lei/Voi*, loss of gendered adjectives). Translating from Spanish preserves grammatical gender, subjunctive moods, and sentence duration that matches Japanese voice-acting timing much more closely.

### Font Handling
Gust engine bitmap fonts use texture atlases containing only characters used by specific languages. `fix_accents.py` automatically converts accented vowels to ASCII letters followed by apostrophes (`e'`, `a'`, `i'`, `o'`, `u'`) and curved quotes (`’`, `“`, `”`) to standard ASCII, guaranteeing 100% font compatibility and zero missing character boxes ("tofu").

---

## Disclaimer

This is a non-commercial, fan-made translation project created for accessibility and preservation purposes.  
*Atelier Yumia: The Alchemist of Memories & the Envisioned Land* and all related assets are trademarks and copyright of **KOEI TECMO GAMES CO., LTD.** / **GUST**.
