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
    print(f">> Esecuzione: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if res.returncode != 0:
        print(f"ERRORE [code {res.returncode}]:\n{res.stderr}\n{res.stdout}")
        sys.exit(1)
    return res.stdout

def main():
    print("=" * 65)
    print(" ATELIER YUMIA - AGGIORNATORE AUTOMATICO TRADUZIONE ITALIANA")
    print("=" * 65)

    # 1. Trova la cartella del gioco
    custom_dir = sys.argv[1] if len(sys.argv) > 1 else None
    game_dir = find_game_dir(custom_dir)
    if not game_dir:
        print("\nCartella di Atelier Yumia non trovata nei percorsi standard.")
        game_dir = input("Inserisci il percorso della cartella del gioco: ").strip('\"\' ')
        if not (os.path.isdir(game_dir) and os.path.isfile(os.path.join(game_dir, "Data", "PACK00.pak"))):
            print("Cartella non valida o PACK00.pak mancante!")
            sys.exit(1)

    print(f"\n[1/5] Cartella gioco rilevata:\n      {game_dir}")
    data_dir = os.path.join(game_dir, "Data")
    game_pak = os.path.join(data_dir, "PACK00.pak")
    game_pak_orig = os.path.join(data_dir, "PACK00.pak.original")

    # Backup di sicurezza se non esiste
    if not os.path.isfile(game_pak_orig):
        print("      Creazione backup di sicurezza (PACK00.pak.original)...")
        shutil.copy2(game_pak, game_pak_orig)

    # 2. Estrazione PACK00.pak
    print("\n[2/5] Estrazione del file PACK00.pak attuale...")
    os.makedirs(PAK_WORK_DIR, exist_ok=True)
    pak_work_pak = os.path.join(PAK_WORK_DIR, "PACK00.pak")
    shutil.copy2(game_pak, pak_work_pak)
    
    run_cmd([GUST_PAK_EXE, "PACK00.pak"], cwd=PAK_WORK_DIR)
    print("      Estrazione completata con successo.")

    # 3. Normalizzazione preventiva caratteri
    print("\n[3/5] Controllo e normalizzazione formato caratteri...")
    run_cmd([sys.executable, FIX_ACCENTS_PY, PROJECT_JSON], cwd=BASE_DIR)

    # 4. Iniezione testi italiani
    print("\n[4/5] Applicazione traduzione italiana allo slot Spagnolo...")
    master_dir = os.path.join(PAK_WORK_DIR, "master")
    run_cmd([sys.executable, TEXT_TOOL_PY, "apply", "spa", master_dir, PROJECT_JSON], cwd=BASE_DIR)

    # 5. Ricompilazione e copia nel gioco
    print("\n[5/5] Ricompilazione pacchetto PACK00.pak e installazione...")
    run_cmd([GUST_PAK_EXE, "PACK00.json"], cwd=PAK_WORK_DIR)

    new_pak = os.path.join(PAK_WORK_DIR, "PACK00.pak")
    if not os.path.isfile(new_pak):
        print("ERRORE: Ricompilazione fallita, PACK00.pak non generato!")
        sys.exit(1)

    shutil.copy2(new_pak, game_pak)

    print("\n" + "=" * 65)
    print(" AGGIORNAMENTO COMPLETATO CON SUCCESSO! ")
    print(" I testi italiani sono stati riapplicati al gioco aggiornato.")
    print(" Nel gioco seleziona la lingua SPAGNOLO per giocare in italiano.")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
