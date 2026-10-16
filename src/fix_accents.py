import json, os, sys

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
DEFAULT_PROJECT = os.path.join(PROJECT_ROOT, "project_yumia_es_en.json")
project_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROJECT
if not os.path.isabs(project_path) and not os.path.exists(project_path):
    candidate = os.path.join(PROJECT_ROOT, project_path)
    if os.path.exists(candidate):
        project_path = candidate

replacements = {
    'à': "a'",
    'á': "a'",
    'è': "e'",
    'é': "e'",
    'ì': "i'",
    'í': "i'",
    'ò': "o'",
    'ó': "o'",
    'ù': "u'",
    'ú': "u'",
    'À': "A'",
    'Á': "A'",
    'È': "E'",
    'É': "E'",
    'Ì': "I'",
    'Í': "I'",
    'Ò': "O'",
    'Ó': "O'",
    'Ù': "U'",
    'Ú': "U'",
    '’': "'",
    '‘': "'",
    '`': "'",
    '“': '"',
    '”': '"',
    '«': '"',
    '»': '"',
    '…': '...',
    '–': '-',
    '—': '-'
}

def main():
    print(f"Caricamento {project_path}...")
    with open(project_path, "r", encoding="utf-8") as f:
        p = json.load(f)

    changed = 0
    total_replaces = 0

    for fname, segs in p["files"].items():
        for s in segs:
            dst = s.get("dst")
            if not dst:
                continue
            new_dst = dst
            for k, v in replacements.items():
                if k in new_dst:
                    count = new_dst.count(k)
                    total_replaces += count
                    new_dst = new_dst.replace(k, v)
            if new_dst != dst:
                s["dst"] = new_dst
                changed += 1

    print(f"Modificati {changed} segmenti (totale sostituzioni: {total_replaces}).")
    with open(project_path, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=1)
    print("Salvataggio completato!")

if __name__ == "__main__":
    main()
