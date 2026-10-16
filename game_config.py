# game_config.py - Helper for detecting, validating, and saving game paths
import os, sys, json, winreg

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

DEFAULT_CANDIDATE_PATHS = [
    r"C:\Program Files (x86)\Steam\steamapps\common\Atelier Yumia",
    r"C:\Program Files\Steam\steamapps\common\Atelier Yumia",
    r"D:\SteamLibrary\steamapps\common\Atelier Yumia",
    r"E:\SteamLibrary\steamapps\common\Atelier Yumia",
    r"F:\SteamLibrary\steamapps\common\Atelier Yumia",
    r"G:\SteamLibrary\steamapps\common\Atelier Yumia",
    r"D:\Steam\steamapps\common\Atelier Yumia",
    r"E:\Steam\steamapps\common\Atelier Yumia",
    r"F:\Steam\steamapps\common\Atelier Yumia",
]

def is_valid_game_dir(path):
    if not path or not os.path.isdir(path):
        return False
    pak_file = os.path.join(path, "Data", "PACK00.pak")
    orig_file = os.path.join(path, "Data", "PACK00.pak.original")
    return os.path.isfile(pak_file) or os.path.isfile(orig_file)

def get_steam_path_from_registry():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
        winreg.CloseKey(key)
        if steam_path and os.path.isdir(steam_path):
            return steam_path
    except Exception:
        pass
    return None

def detect_game_dir():
    # 1. Check Steam Registry location
    steam_path = get_steam_path_from_registry()
    if steam_path:
        candidate = os.path.join(steam_path, "steamapps", "common", "Atelier Yumia")
        if is_valid_game_dir(candidate):
            return candidate

    # 2. Check Candidate standard paths
    for p in DEFAULT_CANDIDATE_PATHS:
        if is_valid_game_dir(p):
            return p

    return None

def load_saved_game_dir():
    if os.path.isfile(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                path = data.get("game_dir", "").strip()
                if is_valid_game_dir(path):
                    return path
        except Exception:
            pass
    return None

def save_game_dir(path):
    path = os.path.abspath(path.strip('\"\' '))
    data = {}
    if os.path.isfile(CONFIG_FILE):
        try:
            data = json.load(open(CONFIG_FILE, "r", encoding="utf-8"))
        except Exception:
            data = {}
    data["game_dir"] = path
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path

def get_or_prompt_game_dir(interactive=True):
    # 1. Saved in config.json
    saved = load_saved_game_dir()
    if saved:
        return saved

    # 2. Auto-detect
    detected = detect_game_dir()
    if detected:
        save_game_dir(detected)
        return detected

    if not interactive:
        return None

    # 3. Prompt user
    print("\nCould not automatically locate 'Atelier Yumia' installation.")
    while True:
        p = input("Please enter the full path to your Atelier Yumia folder: ").strip('\"\' ')
        if not p:
            return None
        if is_valid_game_dir(p):
            save_game_dir(p)
            print(f"Path saved: {p}")
            return p
        print("Invalid directory! Make sure the folder contains 'Data/PACK00.pak'. Try again.")
