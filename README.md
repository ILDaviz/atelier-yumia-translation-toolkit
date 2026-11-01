# Atelier Yumia - Italian Translation Patch

[![Release](https://img.shields.io/github/v/release/ILDaviz/atelier-yumia-translation-toolkit?style=flat-square&label=Latest%20Release)](https://github.com/ILDaviz/atelier-yumia-translation-toolkit/releases)
[![Language](https://img.shields.io/badge/Language-Italian-green?style=flat-square)](#)
[![Platform](https://img.shields.io/badge/Platform-PC%20%2F%20Steam-blue?style=flat-square)](#)

A complete 100% Italian fan-translation patch for **Atelier Yumia: The Alchemist of Memories & the Envisioned Land** on PC (Steam).

---

## 🌟 What is this?

This patch brings a complete Italian localization to the Steam release of *Atelier Yumia*. It replaces the **Español (Spanish)** text slot with natural, high-quality Italian.

### What is translated:
- **100% Story & Dialogue:** All main story events, character side stories, and world quests (`.ebm`).
- **All Interactive Player Choices:** Every dialogue decision and player response prompt (`<SEL_...>`).
- **User Interface & Menus:** Full game UI, settings, status screens, and tutorials (`message.json`).
- **Items & Alchemy:** Complete synthesis recipes, ingredients, material traits, and weapon descriptions.

---

## 📥 Download the Patch

Download the latest pre-compiled, ready-to-use patch from the official GitHub Releases page:

👉 **[Download Latest Release Archive (.zip)](https://github.com/ILDaviz/atelier-yumia-translation-toolkit/releases/latest)**

*(No programming knowledge or Python installation required — simply download and extract the `.zip` archive).*

---

## 🚀 Easy Installation (1-Click)

1. **Download and extract** the latest release `.zip` archive into any folder on your computer.
2. Make sure that **Atelier Yumia is closed**.
3. Double-click on **`Installa_Patch_ITA.bat`**:
   - The installer will automatically locate your Steam library.
   - It creates a safety backup of your original game file (`PACK00.pak.original`).
   - It installs the translated patch.
4. Launch **Atelier Yumia** from Steam.
5. In the game's language settings, select:
   👉 **Text Language: "Español" (Spanish)** *(this slot now contains the full Italian translation)*.

---

## 🔄 How to Uninstall / Restore the Original Game

To remove the translation and revert to the untouched original game:
- Double-click on **`Ripristina_Originale.bat`** in the extracted patch folder.
- Your original vanilla files will be restored immediately.

*(Alternatively, you can verify file integrity via Steam: Right-click *Atelier Yumia* in your Steam Library ➔ **Properties** ➔ **Installed Files** ➔ **Verify integrity of game files**).*

---

## ❓ Frequently Asked Questions (FAQ)

### Why does the patch replace the Spanish ("Español") slot?
Replacing an existing game language slot allows the patch to run natively on the official game executable without requiring third-party DLL injectors, memory hooks, or external mod loaders.

### What happens if Steam updates the game?
Official game updates may overwrite `PACK00.pak`. If this happens, simply re-run `Installa_Patch_ITA.bat` to re-apply the patch.

---

## 🛠️ For Developers & Contributors

Are you interested in how the translation pipeline works, using AI translation models, or contributing to the toolkit?

Please check the **[Developer Guide & Toolkit Documentation (CONTRIBUTING.md)](CONTRIBUTING.md)**.

---

## ⚖️ Disclaimer

- **Fan Translation:** This is a non-commercial, non-profit fan-made translation project created for the Italian gaming community.
- **Copyright:** *Atelier Yumia: The Alchemist of Memories & the Envisioned Land* is a trademark and copyright of **KOEI TECMO GAMES CO., LTD.** and **GUST**.
- **Requirement:** This patch requires a legitimate, legally owned copy of the game on Steam.
