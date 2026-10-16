# yumia_cli.py - Interactive CLI tool for Atelier Yumia Italian Translation
import os, sys, subprocess, shutil, json
import game_config

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
PROJECT_JSON = os.path.join(PROJECT_ROOT, "project_yumia_es_en.json")
GLOSSARY_JSON = os.path.join(PROJECT_ROOT, "glossary.json")
UPDATE_PATCH_PY = os.path.join(SRC_DIR, "update_patch.py")
TRANSLATE_PY = os.path.join(SRC_DIR, "yumia_translate.py")
FIX_ACCENTS_PY = os.path.join(SRC_DIR, "fix_accents.py")
TEXT_TOOL_PY = os.path.join(SRC_DIR, "yumia_text_tool.py")
PAK_WORK_DIR = os.path.join(PROJECT_ROOT, "pak_work")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_header(game_dir):
    print("=" * 66)
    print("        ATELIER YUMIA - ITALIAN TRANSLATION TOOLKIT (CLI)")
    print("=" * 66)
    if game_dir:
        print(f"  Game Folder: {game_dir}")
    else:
        print("  Game Folder: [Not configured - will auto-detect]")
    print("-" * 66)

def ask_choice(prompt, default="1"):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def option_install_ready(game_dir):
    print("\n--- INSTALL / UPDATE TRANSLATION IN GAME ---")
    if not game_dir:
        game_dir = game_config.get_or_prompt_game_dir(interactive=True)
        if not game_dir:
            print("Cannot proceed without a valid game installation directory.")
            return

    print("Applying the pre-translated Italian dataset (29,007 segments)...\n")
    subprocess.run([sys.executable, UPDATE_PATCH_PY, game_dir], cwd=PROJECT_ROOT)

def option_ai_translation(game_dir):
    print("\n--- INTERACTIVE AI TRANSLATION SETUP ---")
    
    # 1. Provider Selection
    print("\nSelect your LLM Provider:")
    print("  [1] OpenAI (Cloud - GPT-6 Luna [Recommended], GPT-5, GPT-4o-mini)")
    print("  [2] Ollama (Local - Qwen 2.5, Llama 3, Mistral)")
    print("  [3] Custom / OpenAI-compatible endpoint (DeepSeek, Groq, LM Studio)")
    p_choice = ask_choice("Provider choice", "1")

    endpoint = "https://api.openai.com/v1"
    default_model = "gpt-6-luna"
    default_workers = "15"

    if p_choice == "2":
        endpoint = ask_choice("Ollama endpoint", "http://localhost:11434/v1")
        default_model = "qwen2.5:7b-instruct"
        default_workers = "6"
        api_key = "ollama"
    elif p_choice == "3":
        endpoint = ask_choice("Base URL endpoint", "https://api.deepseek.com/v1")
        default_model = "deepseek-chat"
        default_workers = "10"
        api_key = ask_choice("API Key")
    else:
        # OpenAI
        endpoint = "https://api.openai.com/v1"
        env_key = os.environ.get("OPENAI_API_KEY", "")
        key_prompt = "Enter your OpenAI API Key (sk-...)"
        if env_key:
            key_prompt += f" [leave blank to use system env: {env_key[:7]}...]"
            api_key = input(f"{key_prompt}: ").strip()
            if not api_key:
                api_key = env_key
        else:
            api_key = input(f"{key_prompt}: ").strip()

    # 2. Model
    model = ask_choice("Model name (Recommended: gpt-6-luna)", default_model)

    # 3. Parallel Workers
    workers = ask_choice("Number of concurrent requests (workers)", default_workers)

    # 4. Project File
    project_file = ask_choice("Target project JSON file", PROJECT_JSON)

    print("\n" + "-" * 66)
    print("CONFIGURATION SUMMARY:")
    print(f"  Endpoint:  {endpoint}")
    print(f"  Model:     {model}")
    print(f"  Workers:   {workers}")
    print(f"  Project:   {project_file}")
    print(f"  Glossary:  {GLOSSARY_JSON}")
    print("-" * 66)

    confirm = ask_choice("Start translation now? (y/n)", "y").lower()
    if confirm not in ("y", "yes"):
        print("Operation cancelled.")
        return

    # Run translation
    print("\n>> Launching yumia_translate.py...")
    cmd = [
        sys.executable, TRANSLATE_PY, project_file,
        "--endpoint", endpoint,
        "--model", model,
        "--api-key", api_key,
        "--workers", str(workers),
        "--glossary", GLOSSARY_JSON
    ]
    res = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if res.returncode != 0:
        print("\nError occurred during translation.")
        return

    # Accent normalization
    print("\n>> Normalizing font characters (fix_accents.py)...")
    subprocess.run([sys.executable, FIX_ACCENTS_PY, project_file], cwd=PROJECT_ROOT)

    # Prompt to apply into game
    apply_now = ask_choice("\nApply translated texts into the game now? (y/n)", "y").lower()
    if apply_now in ("y", "yes"):
        option_install_ready(game_dir)

def option_extract_game():
    print("\n--- EXTRACT RAW GAME TEXTS ---")
    if not os.path.isdir(PAK_WORK_DIR):
        print(f"Directory '{PAK_WORK_DIR}' not found. Please run option [1] first to extract PACK00.pak.")
        return
    master_dir = os.path.join(PAK_WORK_DIR, "master")
    out_file = ask_choice("Output filename for new project", "project_yumia_es_en.json")
    print(f"\n>> Extracting text from {master_dir}...")
    cmd = [sys.executable, TEXT_TOOL_PY, "extract", "spa", "eng", master_dir, out_file]
    subprocess.run(cmd, cwd=PROJECT_ROOT)
    print("\nExtraction finished successfully!")

def option_configure_game_dir(current_dir):
    print("\n--- CONFIGURE GAME INSTALLATION DIRECTORY ---")
    if current_dir:
        print(f"Current saved path:\n  {current_dir}\n")
    else:
        print("No game directory currently saved.\n")

    new_dir = input("Enter new Atelier Yumia folder path (or press Enter to cancel): ").strip('\"\' ')
    if not new_dir:
        return current_dir

    if game_config.is_valid_game_dir(new_dir):
        saved = game_config.save_game_dir(new_dir)
        print(f"\n[OK] Game path successfully updated:\n     {saved}")
        return saved
    else:
        print("\n[ERROR] Invalid path! The folder must contain 'Data/PACK00.pak'. Path not saved.")
        return current_dir

def main():
    # Load or auto-detect game directory on startup
    game_dir = game_config.load_saved_game_dir()
    if not game_dir:
        game_dir = game_config.detect_game_dir()
        if game_dir:
            game_config.save_game_dir(game_dir)

    while True:
        clear_screen()
        print_header(game_dir)
        print("\nWhat would you like to do?\n")
        print("  [1] Install / Update translation in game (Fast, ~15s, ready-to-play)")
        print("  [2] AI Translation (Configure provider, API key, model & workers)")
        print("  [3] Extract raw texts from game (Create a fresh project.json)")
        print("  [4] Change / Set game folder path")
        print("  [5] Exit")
        print()
        
        choice = ask_choice("Select an option number", "1")
        if choice == "1":
            option_install_ready(game_dir)
            input("\nPress ENTER to continue...")
        elif choice == "2":
            option_ai_translation(game_dir)
            input("\nPress ENTER to continue...")
        elif choice == "3":
            option_extract_game()
            input("\nPress ENTER to continue...")
        elif choice == "4":
            game_dir = option_configure_game_dir(game_dir)
            input("\nPress ENTER to continue...")
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice!")
            input("\nPress ENTER to try again...")

if __name__ == "__main__":
    main()
