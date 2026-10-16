# update_patch.py - Automatic translation updater after Steam game patches
import os, sys, shutil, subprocess, json

DEFAULT_GAME_PATHS = [
    r"C:\Program Files (x86)\Steam\steamapps\common\Atelier Yumia",
    r"D:\SteamLibrary\steamapps\common\Atelier Yumia",
    r"E:\SteamLibrary\steamapps\common\Atelier Yumia",
    r"F:\SteamLibrary\steamapps\common\Atelier Yumia",
    r"D:\Steam\steamapps\common\Atelier Yumia",
    r"E:\Steam\steamapps\common\Atelier Yumia",
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAK_WORK_DIR = os.path.join(BASE_DIR, "pak_work")
GUST_PAK_EXE = os.path.join(BASE_DIR, "gust_tools", "gust_pak.exe")
PROJECT_JSON = os.path.join(BASE_DIR, "project_yumia_es_en.json")
TEXT_TOOL_PY = os.path.join(BASE_DIR, "yumia_text_tool.py")
FIX_ACCENTS_PY = os.path.join(BASE_DIR, "fix_accents.py")

def find_game_dir(custom_path=None):
    if custom_path and os.path.isdir(custom_path):
        return custom_path
    for p in DEFAULT_GAME_PATHS:
        if os.path.isdir(p) and os.path.isfile(os.path.join(p, "Data", "PACK00.pak")):
            return p
    return None

def run_cmd(cmd, cwd=None):
    print(f">> Executing: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if res.returncode != 0:
        print(f"ERROR [code {res.returncode}]:\n{res.stderr}\n{res.stdout}")
        sys.exit(1)
    return res.stdout

def main():
    print("=" * 66)
    print(" ATELIER YUMIA - ITALIAN TRANSLATION AUTO-UPDATER")
    print("=" * 66)

    # 1. Locate game directory
    custom_dir = sys.argv[1] if len(sys.argv) > 1 else None
    game_dir = find_game_dir(custom_dir)
    if not game_dir:
        print("\nAtelier Yumia game folder not found in default paths.")
        game_dir = input("Enter your game installation folder path: ").strip('\"\' ')
        if not (os.path.isdir(game_dir) and os.path.isfile(os.path.join(game_dir, "Data", "PACK00.pak"))):
            print("Invalid directory or PACK00.pak missing!")
            sys.exit(1)

    print(f"\n[1/5] Game directory detected:\n      {game_dir}")
    data_dir = os.path.join(game_dir, "Data")
    game_pak = os.path.join(data_dir, "PACK00.pak")
    game_pak_orig = os.path.join(data_dir, "PACK00.pak.original")

    # Safety backup if not present
    if not os.path.isfile(game_pak_orig):
        print("      Creating safety backup (PACK00.pak.original)...")
        shutil.copy2(game_pak, game_pak_orig)

    # 2. Extract PACK00.pak
    print("\n[2/5] Extracting current PACK00.pak...")
    os.makedirs(PAK_WORK_DIR, exist_ok=True)
    pak_work_pak = os.path.join(PAK_WORK_DIR, "PACK00.pak")
    shutil.copy2(game_pak, pak_work_pak)
    
    run_cmd([GUST_PAK_EXE, "PACK00.pak"], cwd=PAK_WORK_DIR)
    print("      Extraction completed successfully.")

    # 3. Font character normalization
    print("\n[3/5] Checking and normalizing font character formats...")
    run_cmd([sys.executable, FIX_ACCENTS_PY, PROJECT_JSON], cwd=BASE_DIR)

    # 4. Inject Italian translation
    print("\n[4/5] Injecting Italian translation into Spanish slot...")
    master_dir = os.path.join(PAK_WORK_DIR, "master")
    run_cmd([sys.executable, TEXT_TOOL_PY, "apply", "spa", master_dir, PROJECT_JSON], cwd=BASE_DIR)

    # 5. Repack and install into game
    print("\n[5/5] Repacking PACK00.pak and installing into game...")
    run_cmd([GUST_PAK_EXE, "PACK00.json"], cwd=PAK_WORK_DIR)

    new_pak = os.path.join(PAK_WORK_DIR, "PACK00.pak")
    if not os.path.isfile(new_pak):
        print("ERROR: Repacking failed, PACK00.pak not found!")
        sys.exit(1)

    shutil.copy2(new_pak, game_pak)

    print("\n" + "=" * 66)
    print(" UPDATE COMPLETED SUCCESSFULLY! ")
    print(" Italian translation has been applied to your game.")
    print(" In game settings, select language 'Español' to play in Italian.")
    print("=" * 66 + "\n")

if __name__ == "__main__":
    main()
