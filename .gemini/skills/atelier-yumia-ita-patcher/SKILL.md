---
name: atelier-yumia-ita-patcher
description: Install, update, verify, or restore the 100% Italian translation patch for Atelier Yumia (Steam/PC). Use whenever the user asks to install the Italian translation, fix untranslated texts, restore the original game, or re-apply the patch after a Steam game update.
---

# Atelier Yumia - Italian Translation Patcher Skill

This skill guides the agent in installing, maintaining, and updating the complete Italian fan-translation patch for **Atelier Yumia: The Alchemist of Memories & the Envisioned Land** on Steam (PC).

The patch translates 100% of the game texts:
- Story and side dialogues (`.ebm`)
- All player interactive choice options (`<SEL_...><CR>`)
- User Interface, menus, tutorials, item names, and descriptions (`fixed_data/message/message.json`)

It replaces the **Español (Spanish)** text slot with Italian.

---

## 1. Locating the Game Installation

Check the following common Steam library locations:
1. `C:\Program Files (x86)\Steam\steamapps\common\Atelier Yumia`
2. `D:\SteamLibrary\steamapps\common\Atelier Yumia`
3. `E:\SteamLibrary\steamapps\common\Atelier Yumia`
4. Or parse Steam's `libraryfolders.vdf` in `C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf`.

The target directory must contain `Data\PACK00.pak`.

---

## 2. Quick Installation (Using Pre-compiled PAK)

When the user asks to install or re-apply the patch:

1. **Locate the pre-compiled Italian `PACK00.pak`**:
   - Repository: `release/Atelier_Yumia_v1.0.7_ITA/PACK00.pak` or `pak_work/PACK00.pak`.
   - Desktop release folder: `C:\Users\David\Desktop\Atelier_Yumia_v1.0.7_ITA\PACK00.pak`.

2. **Create backup of original game files**:
   - If `<GameDir>\Data\PACK00.pak.original` does NOT exist:
     ```powershell
     Copy-Item "<GameDir>\Data\PACK00.pak" "<GameDir>\Data\PACK00.pak.original"
     ```

3. **Install the translated PAK**:
   ```powershell
   Copy-Item "<SourcePath>\PACK00.pak" "<GameDir>\Data\PACK00.pak" -Force
   ```

4. **Verify & Inform User**:
   - Confirm file size matches the translated PAK (~208 MB).
   - Instruct the user to launch the game and select **Español** in the game text language settings.

---

## 3. Handling Steam Game Updates (Re-building from Source)

If Steam updates the game and overwrites `PACK00.pak`:

1. Open the translation toolkit repository (or WSL path):
   ```bash
   cd /home/david/src/tries/2026-10-16-atelier-yumia-translation-toolkit
   ```
2. Run the auto-updater:
   ```bash
   python3 src/update_patch.py
   ```
   *(Or on Windows: run `run_toolkit.bat` and select option `1`)*

3. This script will:
   - Extract the new game files using `gust_pak.exe`.
   - Run `fix_accents.py` to ensure font compatibility.
   - Inject the complete Italian translation dataset (`project_yumia_es_en.json`).
   - Run `apply_choices.py` to ensure all player choice prompts are translated.
   - Recompile `PACK00.pak` and automatically deploy it to the game directory.

---

## 4. Restoring the Original Game (Vanilla)

If the user wants to revert to the untouched original:
```powershell
if (Test-Path "<GameDir>\Data\PACK00.pak.original") {
    Copy-Item "<GameDir>\Data\PACK00.pak.original" "<GameDir>\Data\PACK00.pak" -Force
}
```
Or advise the user to use Steam: **Properties -> Installed Files -> Verify integrity of game files**.
