import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yumia_text_tool import tokenize, detokenize, is_translatable
from translate_choices_data import CHOICE_TRANSLATIONS

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_JSON = os.path.join(REPO_DIR, "project_yumia_es_en.json")
MASTER_DIR = os.path.join(REPO_DIR, "pak_work", "master")
SPA_DIR = os.path.join(MASTER_DIR, "spa")

def main():
    print(f"Applying choices to {PROJECT_JSON} and EBM files in {SPA_DIR}...")
    
    # 1. Update project_yumia_es_en.json
    with open(PROJECT_JSON, "r", encoding="utf-8") as f:
        project = json.load(f)

    json_updated_count = 0
    json_added_count = 0

    for rel, choices in CHOICE_TRANSLATIONS.items():
        if rel not in project["files"]:
            project["files"][rel] = []
        segs = project["files"][rel]

        for spa, eng, ita in choices:
            # Check if segment already exists in segs (by src or <SEL_ tag)
            tag = spa.split("<CR>")[0] if "<CR>" in spa else spa
            found = False
            for s in segs:
                if tag in s.get("src", "") or tag in s.get("dst", ""):
                    s["src"] = spa
                    s["ref"] = eng
                    s["dst"] = ita
                    json_updated_count += 1
                    found = True
                    break
            if not found:
                # Add new segment
                new_idx = len(segs)
                segs.append({
                    "i": new_idx,
                    "src": spa,
                    "ref": eng,
                    "dst": ita
                })
                json_added_count += 1

    with open(PROJECT_JSON, "w", encoding="utf-8") as f:
        json.dump(project, f, ensure_ascii=False, indent=1)

    print(f"JSON updated: {json_updated_count} existing updated, {json_added_count} new added.")

    # 2. Directly update .ebm files in pak_work/master/spa
    ebm_updated_count = 0
    ebm_files_count = 0

    for rel, choices in CHOICE_TRANSLATIONS.items():
        ebm_path = os.path.join(SPA_DIR, rel.replace("/", os.sep))
        if not os.path.exists(ebm_path):
            print(f"WARNING: File not found {ebm_path}")
            continue

        data = open(ebm_path, "rb").read()
        toks = tokenize(data)
        
        file_changed = False
        for spa, eng, ita in choices:
            tag = spa.split("<CR>")[0] if "<CR>" in spa else spa
            for idx, (k, t) in enumerate(toks):
                if k == "str" and tag in t:
                    if t != ita:
                        toks[idx] = ("str", ita)
                        ebm_updated_count += 1
                        file_changed = True
                    break

        if file_changed:
            open(ebm_path, "wb").write(detokenize(toks))
            ebm_files_count += 1

    print(f"EBM files updated: {ebm_updated_count} choice strings replaced across {ebm_files_count} files.")

if __name__ == "__main__":
    main()
