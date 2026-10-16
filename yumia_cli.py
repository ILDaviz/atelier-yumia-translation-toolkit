# yumia_cli.py - Interactive CLI tool for Atelier Yumia Italian Translation
import os, sys, subprocess, shutil, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_JSON = os.path.join(BASE_DIR, "project_yumia_es_en.json")
GLOSSARY_JSON = os.path.join(BASE_DIR, "glossary.json")
UPDATE_PATCH_PY = os.path.join(BASE_DIR, "update_patch.py")
TRANSLATE_PY = os.path.join(BASE_DIR, "yumia_translate.py")
FIX_ACCENTS_PY = os.path.join(BASE_DIR, "fix_accents.py")
TEXT_TOOL_PY = os.path.join(BASE_DIR, "yumia_text_tool.py")
PAK_WORK_DIR = os.path.join(BASE_DIR, "pak_work")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_header():
    print("=" * 66)
    print("        ATELIER YUMIA - ITALIAN TRANSLATION TOOLKIT (CLI)")
    print("=" * 66)

def ask_choice(prompt, default="1"):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def option_install_ready():
    print("\n--- INSTALLAZIONE / AGGIORNAMENTO RAPIDO NEL GIOCO ---")
    print("Applico il pacchetto di traduzione italiana gia' pronto (29.007 segmenti)...\n")
    subprocess.run([sys.executable, UPDATE_PATCH_PY], cwd=BASE_DIR)

def option_ai_translation():
    print("\n--- CONFIGURAZIONE TRADUZIONE IA INTERATTIVA ---")
    
    # 1. Scelta Provider
    print("\nSeleziona il provider:")
    print("  [1] OpenAI (Cloud - GPT-6 Luna, GPT-5, GPT-4o-mini)")
    print("  [2] Ollama (Locale - Qwen 2.5, Llama 3, Mistral)")
    print("  [3] Custom / Altro endpoint compatibile OpenAI (DeepSeek, Groq, LM Studio)")
    p_choice = ask_choice("Scelta provider", "1")

    endpoint = "https://api.openai.com/v1"
    default_model = "gpt-6-luna"
    default_workers = "15"

    if p_choice == "2":
        endpoint = ask_choice("Endpoint Ollama", "http://localhost:11434/v1")
        default_model = "qwen2.5:7b-instruct"
        default_workers = "6"
        api_key = "ollama"
    elif p_choice == "3":
        endpoint = ask_choice("Endpoint base URL", "https://api.deepseek.com/v1")
        default_model = "deepseek-chat"
        default_workers = "10"
        api_key = ask_choice("API Key")
    else:
        # OpenAI
        endpoint = "https://api.openai.com/v1"
        env_key = os.environ.get("OPENAI_API_KEY", "")
        key_prompt = "Inserisci la tua OpenAI API Key (sk-...)"
        if env_key:
            key_prompt += f" [lascia vuoto per usare quella di sistema: {env_key[:7]}...]"
            api_key = input(f"{key_prompt}: ").strip()
            if not api_key:
                api_key = env_key
        else:
            api_key = input(f"{key_prompt}: ").strip()

    # 2. Modello
    model = ask_choice("Nome del modello", default_model)

    # 3. Numero Worker Paralleli
    workers = ask_choice("Numero di richieste in parallelo (workers)", default_workers)

    # 4. File di progetto
    project_file = ask_choice("File di progetto da tradurre", PROJECT_JSON)

    print("\n" + "-" * 66)
    print("RIEPILOGO CONFIGURAZIONE:")
    print(f"  Provider Endpoint: {endpoint}")
    print(f"  Modello:           {model}")
    print(f"  Worker:            {workers}")
    print(f"  Progetto:          {project_file}")
    print(f"  Glossario:         {GLOSSARY_JSON}")
    print("-" * 66)

    confirm = ask_choice("Avviare la traduzione adesso? (s/n)", "s").lower()
    if confirm not in ("s", "si", "y", "yes"):
        print("Operazione annullata.")
        return

    # Esecuzione traduzione
    print("\n>> Avvio di yumia_translate.py...")
    cmd = [
        sys.executable, TRANSLATE_PY, project_file,
        "--endpoint", endpoint,
        "--model", model,
        "--api-key", api_key,
        "--workers", str(workers),
        "--glossary", GLOSSARY_JSON
    ]
    res = subprocess.run(cmd, cwd=BASE_DIR)
    if res.returncode != 0:
        print("\nErrore durante la traduzione.")
        return

    # Normalizzazione accenti
    print("\n>> Normalizzazione automatica caratteri (fix_accents.py)...")
    subprocess.run([sys.executable, FIX_ACCENTS_PY, project_file], cwd=BASE_DIR)

    # Chiedi se applicare subito al gioco
    apply_now = ask_choice("\nVuoi applicare subito la traduzione al gioco? (s/n)", "s").lower()
    if apply_now in ("s", "si", "y", "yes"):
        subprocess.run([sys.executable, UPDATE_PATCH_PY], cwd=BASE_DIR)

def option_extract_game():
    print("\n--- ESTRAZIONE TESTI DAI FILE DI GIOCO ---")
    if not os.path.isdir(PAK_WORK_DIR):
        print(f"Cartella {PAK_WORK_DIR} non trovata. Esegui prima l'opzione [1] per estrarre PACK00.pak.")
        return
    master_dir = os.path.join(PAK_WORK_DIR, "master")
    out_file = ask_choice("Nome file di output per il nuovo progetto", "project_yumia_es_en.json")
    print(f"\n>> Estrazione in corso da {master_dir}...")
    cmd = [sys.executable, TEXT_TOOL_PY, "extract", "spa", "eng", master_dir, out_file]
    subprocess.run(cmd, cwd=BASE_DIR)
    print("\nEstrazione completata con successo!")

def main():
    while True:
        clear_screen()
        print_header()
        print("\nCosa desideri fare?\n")
        print("  [1] Installa / Aggiorna traduzione nel gioco (Veloce, 15 sec, gia' pronta)")
        print("  [2] Traduzione IA (configura provider, chiave, modello e worker)")
        print("  [3] Estrai testi grezzi dal gioco (crea nuovo project.json)")
        print("  [4] Esci")
        print()
        
        choice = ask_choice("Digita il numero dell'opzione", "1")
        if choice == "1":
            option_install_ready()
            input("\nPremi INVIO per continuare...")
        elif choice == "2":
            option_ai_translation()
            input("\nPremi INVIO per continuare...")
        elif choice == "3":
            option_extract_game()
            input("\nPremi INVIO per continuare...")
        elif choice == "4":
            print("\nArrivederci!")
            break
        else:
            print("Scelta non valida!")
            input("\nPremi INVIO per riprovare...")

if __name__ == "__main__":
    main()
