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
    print("\n--- INSTALL / UPDATE TRANSLATION IN GAME ---")
    print("Applying the pre-translated Italian dataset (29,007 segments)...\n")
    subprocess.run([sys.executable, UPDATE_PATCH_PY], cwd=BASE_DIR)

def option_ai_translation():
    print("\n--- INTERACTIVE AI TRANSLATION SETUP ---")
    
    # 1. Provider Selection
    print("\nSelect your LLM Provider:")
    print("  [1] OpenAI (Cloud - GPT-6 Luna, GPT-5, GPT-4o-mini)")
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
    model = ask_choice("Model name", default_model)

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
    res = subprocess.run(cmd, cwd=BASE_DIR)
    if res.returncode != 0:
        print("\nError occurred during translation.")
        return

    # Accent normalization
    print("\n>> Normalizing font characters (fix_accents.py)...")
    subprocess.run([sys.executable, FIX_ACCENTS_PY, project_file], cwd=BASE_DIR)

    # Prompt to apply into game
    apply_now = ask_choice("\nApply translated texts into the game now? (y/n)", "y").lower()
    if apply_now in ("y", "yes"):
        subprocess.run([sys.executable, UPDATE_PATCH_PY], cwd=BASE_DIR)

def option_extract_game():
    print("\n--- EXTRACT RAW GAME TEXTS ---")
    if not os.path.isdir(PAK_WORK_DIR):
        print(f"Directory '{PAK_WORK_DIR}' not found. Please run option [1] first to extract PACK00.pak.")
        return
    master_dir = os.path.join(PAK_WORK_DIR, "master")
    out_file = ask_choice("Output filename for new project", "project_yumia_es_en.json")
    print(f"\n>> Extracting text from {master_dir}...")
    cmd = [sys.executable, TEXT_TOOL_PY, "extract", "spa", "eng", master_dir, out_file]
    subprocess.run(cmd, cwd=BASE_DIR)
    print("\nExtraction finished successfully!")

def main():
    while True:
        clear_screen()
        print_header()
        print("\nWhat would you like to do?\n")
        print("  [1] Install / Update translation in game (Fast, ~15s, ready-to-play)")
        print("  [2] AI Translation (Configure provider, API key, model & workers)")
        print("  [3] Extract raw texts from game (Create a fresh project.json)")
        print("  [4] Exit")
        print()
        
        choice = ask_choice("Select an option number", "1")
        if choice == "1":
            option_install_ready()
            input("\nPress ENTER to continue...")
        elif choice == "2":
            option_ai_translation()
            input("\nPress ENTER to continue...")
        elif choice == "3":
            option_extract_game()
            input("\nPress ENTER to continue...")
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice!")
            input("\nPress ENTER to try again...")

if __name__ == "__main__":
    main()
