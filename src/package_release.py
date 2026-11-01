# package_release.py - Automated release packager for Atelier Yumia Italian Translation
import os, sys, shutil, zipfile, hashlib
import game_config

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
VERSION = "v1.0.7"
RELEASE_DIR = os.path.join(PROJECT_ROOT, "release", f"Atelier_Yumia_{VERSION}_ITA")
OUTPUT_ZIP = os.path.join(PROJECT_ROOT, "release", f"Atelier_Yumia_{VERSION}_ITA.zip")
DESKTOP_DIR = os.path.join(os.path.expanduser("~"), "Desktop")

REQUIRED_FILES = [
    "PACK00.pak",
    "Installa_Patch_ITA.bat",
    "Ripristina_Originale.bat",
    "ISTRUZIONI.txt",
]

def calculate_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest().upper()

def build_markdown_notes(zip_filename, zip_size_mb, zip_sha, version=VERSION):
    return f"""# Atelier Yumia: The Alchemist of Memories - Italian Translation Patch ({version})

Complete fan translation patch in Italian for the PC / Steam release of **Atelier Yumia: The Alchemist of Memories & the Envisioned Land**.

Translates 100% of game texts: main story, side quests, player interactive choices, user interface (UI), menus, tutorials, alchemy synthesis, and item descriptions.

---

## 📥 Installation Guide

1. **Download and extract** the archive **`{zip_filename}`** into a folder of your choice.
2. Ensure that **Atelier Yumia is closed**.
3. Double-click on **`Installa_Patch_ITA.bat`**:
   - The script will automatically locate your Steam game folder.
   - It will create a safety backup of your original vanilla file (`PACK00.pak.original`).
   - It will install the translated patch file.
4. Launch **Atelier Yumia** on Steam.
5. In game settings, set the text language to:
   👉 **"Español" (Spanish)** *(this is the slot replaced with the full Italian translation)*.

---

## 🔄 Restoring Original Game (Uninstall)

If you ever want to revert to the untouched original vanilla game:
- Double-click **`Ripristina_Originale.bat`** in the extracted folder.
- It will immediately restore the clean backup file created during installation.

*(Alternatively, verify file integrity via Steam: Right-click game -> Properties -> Installed Files -> Verify integrity of game files).*

---

## 🛡️ File Integrity Check (Checksum)
- **File:** `{zip_filename}`
- **Size:** `{zip_size_mb:.2f} MB`
- **SHA-256:** `{zip_sha}`

---
*Non-commercial fan translation created for the Atelier community.*
"""

def build_release_zip(copy_to_desktop=True):
    print("=" * 70)
    print(" ATELIER YUMIA - RELEASE PACKAGE BUILDER")
    print("=" * 70)

    os.makedirs(RELEASE_DIR, exist_ok=True)
    desktop_folder = os.path.join(DESKTOP_DIR, f"Atelier_Yumia_{VERSION}_ITA")

    # Recover missing files if available from desktop release folder
    for f in REQUIRED_FILES:
        target = os.path.join(RELEASE_DIR, f)
        if not os.path.isfile(target) and os.path.isdir(desktop_folder):
            src_f = os.path.join(desktop_folder, f)
            if os.path.isfile(src_f):
                shutil.copy2(src_f, target)

    pak_path = os.path.join(RELEASE_DIR, "PACK00.pak")

    # If PACK00.pak is missing, attempt auto-recovery from game or pak_work
    if not os.path.isfile(pak_path):
        print("[!] PACK00.pak missing in release directory. Attempting recovery...")
        candidates = [
            os.path.join(PROJECT_ROOT, "pak_work", "PACK00.pak"),
            os.path.join(DESKTOP_DIR, f"Atelier_Yumia_{VERSION}_ITA", "PACK00.pak"),
        ]
        game_dir = game_config.load_saved_game_dir() or game_config.detect_game_dir()
        if game_dir:
            candidates.append(os.path.join(game_dir, "Data", "PACK00.pak"))

        found = False
        for c in candidates:
            if c and os.path.isfile(c) and os.path.getsize(c) > 100 * 1024 * 1024:
                print(f"    Found candidate: {c}")
                shutil.copy2(c, pak_path)
                found = True
                break

        if not found:
            print("ERROR: PACK00.pak could not be located. Compile the patch first!")
            return None

    # Check all required files
    missing = [f for f in REQUIRED_FILES if not os.path.isfile(os.path.join(RELEASE_DIR, f))]
    if missing:
        print(f"ERROR: Missing required files: {missing}")
        return None

    print(f"\n[1/3] Packaging files from:\n      {RELEASE_DIR}")
    for f in REQUIRED_FILES:
        sz_mb = os.path.getsize(os.path.join(RELEASE_DIR, f)) / (1024 * 1024)
        print(f"      - {f:<26} ({sz_mb:6.2f} MB)")

    print(f"\n[2/3] Compressing into ZIP archive:\n      {OUTPUT_ZIP}")
    with zipfile.ZipFile(OUTPUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for fname in REQUIRED_FILES:
            full_path = os.path.join(RELEASE_DIR, fname)
            zf.write(full_path, arcname=fname)

    zip_size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    zip_sha = calculate_sha256(OUTPUT_ZIP)
    zip_basename = os.path.basename(OUTPUT_ZIP)
    print(f"      Archive created successfully! Size: {zip_size_mb:.2f} MB")
    print(f"      SHA-256: {zip_sha}")

    # Copy zip to Desktop
    desktop_zip = os.path.join(DESKTOP_DIR, zip_basename)
    if copy_to_desktop and os.path.isdir(DESKTOP_DIR):
        print(f"\n[3/3] Copying package to Desktop:\n      {desktop_zip}")
        shutil.copy2(OUTPUT_ZIP, desktop_zip)

    # Print GitHub release guide and notes (in console only, no extra .md file saved)
    notes_content = build_markdown_notes(zip_basename, zip_size_mb, zip_sha, VERSION)
    print("\n" + "=" * 70)
    print(" GITHUB RELEASE PUBLISHING GUIDE")
    print("=" * 70)
    print(" 1. Open the GitHub new release page:")
    print("    https://github.com/ILDaviz/atelier-yumia-translation-toolkit/releases/new")
    print()
    print(f" 2. Tag version:   {VERSION}")
    print(f" 3. Release title: Atelier Yumia - Italian Translation Patch ({VERSION})")
    print()
    print(" 4. Attach binary file (Attach binaries by dropping them here):")
    print(f"    -> Drag and drop: {desktop_zip}")
    print()
    print(" 5. Release description (Markdown) - copy and paste into GitHub:")
    print("-" * 70)
    print(notes_content.strip())
    print("-" * 70)
    print(" 6. Click 'Publish release'! The patch is now public.")
    print("=" * 70 + "\n")

    return OUTPUT_ZIP

def main():
    build_release_zip(copy_to_desktop=True)

if __name__ == "__main__":
    main()
