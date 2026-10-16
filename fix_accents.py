import json, os, sys

project_path = sys.argv[1] if len(sys.argv) > 1 else "project_yumia_es_en.json"

replacements = {
    'à': 'á',
    'è': 'é',
    'ì': 'í',
    'ò': 'ó',
    'ù': 'ú',
    'À': 'Á',
    'È': 'É',
    'Ì': 'Í',
    'Ò': 'Ó',
    'Ù': 'Ú',
    '’': "'",
    '‘': "'",
    '`': "'",
    '“': '"',
    '”': '"',
    '«': '"',
    '»': '"',
    '…': '...',
    '–': '-',
    '—': '-',
    '→': '->',
    '°': ' deg',
}

def main():
    print("Caricamento del progetto...")
    with open(project_path, "r", encoding="utf-8") as f:
        p = json.load(f)

    changed_segments = 0
    total_replacements = {k: 0 for k in replacements}

    for fname, segs in p["files"].items():
        for s in segs:
            dst = s.get("dst")
            if not dst:
                continue
            new_dst = dst
            for orig, repl in replacements.items():
                if orig in new_dst:
                    count = new_dst.count(orig)
                    total_replacements[orig] += count
                    new_dst = new_dst.replace(orig, repl)
            if new_dst != dst:
                s["dst"] = new_dst
                changed_segments += 1

    print(f"Modificati {changed_segments} segmenti.")
    with open(project_path, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=1)
    print("Progetto salvato con successo!")

if __name__ == "__main__":
    main()
