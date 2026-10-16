# Yumia text tool - extract/apply translatable text from Atelier Yumia A26 EBM + message.json
# Usage:
#   python yumia_text_tool.py check  <master_dir>            -> verify lossless roundtrip on all .ebm
#   python yumia_text_tool.py extract <src_lang> <ref_lang> <master_dir> <out_project.json>
#   python yumia_text_tool.py apply   <target_lang> <master_dir> <project.json> [--dry]
import os, re, sys, struct, json

MAX_STR = 2048

def is_string_candidate(data, off):
    """u32 at off = length of NUL-terminated UTF-8 string? Returns (text, end) or None."""
    if off + 4 > len(data):
        return None
    (v,) = struct.unpack_from("<I", data, off)
    if not (2 <= v <= MAX_STR) or off + 4 + v > len(data):
        return None
    raw = data[off + 4 : off + 4 + v]
    if raw[-1:] != b"\x00" or b"\x00" in raw[:-1]:
        return None
    try:
        txt = raw[:-1].decode("utf-8")
    except UnicodeDecodeError:
        return None
    if not all(c >= " " or c in "\n\r\t" for c in txt):
        return None
    return txt, off + 4 + v

def tokenize(data):
    """Split ebm into tokens: ('raw', bytes) or ('str', text). Preserves byte-perfect alignment."""
    tokens = []
    off = 0
    last_end = 0
    while off < len(data) - 4:
        v = int.from_bytes(data[off : off + 4], "little")
        if 2 <= v <= MAX_STR and off + 4 + v <= len(data):
            raw = data[off + 4 : off + 4 + v]
            if raw[-1:] == b"\x00" and b"\x00" not in raw[:-1]:
                try:
                    txt = raw[:-1].decode("utf-8")
                    if all(c >= " " or c in "\n\r\t" for c in txt):
                        if off > last_end:
                            tokens.append(("raw", data[last_end:off]))
                        tokens.append(("str", txt))
                        off = off + 4 + v
                        last_end = off
                        continue
                except UnicodeDecodeError:
                    pass
        off += 1
    if last_end < len(data):
        tokens.append(("raw", data[last_end:]))
    return tokens

def detokenize(tokens):
    out = bytearray()
    for kind, val in tokens:
        if kind == "raw":
            out += val
        elif kind == "str":
            b = val.encode("utf-8") + b"\x00"
            out += int.to_bytes(len(b), 4, "little") + b
        elif kind == "u32":
            out += struct.pack("<I", val)
    return bytes(out)

IDENT = re.compile(r"^[A-Za-z0-9_\-\.]+$")
def is_translatable(s):
    if IDENT.match(s):          # CHARACTER_YUMIA, STR_0001, numbers
        return False
    if not re.search(r"[A-Za-zÀ-ÿ]", s):
        return False
    return True

def is_ui_translatable(s):
    if not s or not s.strip():
        return False
    if re.match(r"^([0-9\.\,\:\;\/\-\+\%\s]+|%s|\{\d+\}|<[A-Za-z0-9_]+>|<\/[A-Za-z0-9_]+>)*$", s):
        return False
    if not re.search(r"[A-Za-zÀ-ÿ]", s):
        return False
    return True

def words(s):
    return len(re.findall(r"[A-Za-zÀ-ÿ0-9]+", s))

def iter_lang_files(master, lang, ext):
    base = os.path.join(master, lang)
    for root, _, files in os.walk(base):
        for f in files:
            if f.endswith(ext):
                yield os.path.join(root, f)

def load_json(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)

def save_json(path, obj):
    with open(path, "rb") as f:
        has_bom = f.read(3) == b"\xef\xbb\xbf"
    with open(path, "w", encoding="utf-8-sig" if has_bom else "utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)

def cmd_check(master, lang):
    n_ok = n_bad = 0
    tot_words = 0
    for path in iter_lang_files(master, lang, ".ebm"):
        data = open(path, "rb").read()
        try:
            rebuilt = detokenize(tokenize(data))
        except Exception as e:
            print(f"PARSE FAIL {path}: {e}")
            n_bad += 1
            continue
        if rebuilt != data:
            print(f"ROUNDTRIP MISMATCH {path}")
            n_bad += 1
            continue
        n_ok += 1
        tot_words += sum(words(t) for k, t in tokenize(data) if k == "str" and is_translatable(t))
    # UI json
    ui_words = 0
    p = os.path.join(master, lang, "fixed_data", "message", "message.json")
    if os.path.exists(p):
        j = load_json(p)
        for entry in j["message_message"]:
            if is_translatable(entry["MESSAGE"]):
                ui_words += words(entry["MESSAGE"])
    print(f"EBM ok={n_ok} bad={n_bad} | dialog words={tot_words} | UI words={ui_words}")

def cmd_extract(src, ref, master, out):
    project = {"source": src, "reference": ref, "files": {}}
    # dialogs
    ref_map = {}
    for path in iter_lang_files(master, ref, ".ebm"):
        rel = os.path.relpath(path, os.path.join(master, ref)).replace("\\", "/")
        ref_map[rel] = [t for k, t in tokenize(open(path, 'rb').read()) if k == "str"]
    for path in iter_lang_files(master, src, ".ebm"):
        rel = os.path.relpath(path, os.path.join(master, src)).replace("\\", "/")
        toks = tokenize(open(path, "rb").read())
        strs = [t for k, t in toks if k == "str"]
        refs = ref_map.get(rel, [])
        segs = [{"i": i, "src": s, "ref": "", "dst": ""}
                for i, s in enumerate(strs) if is_translatable(s)]
        # alignment: pair translatable strings in order if counts match
        ref_trans = [s for s in refs if is_translatable(s)]
        if len(ref_trans) == len(segs):
            for seg, r in zip(segs, ref_trans):
                seg["ref"] = r
        project["files"][rel] = segs
    # UI
    def load_ui(lang):
        p = os.path.join(master, lang, "fixed_data", "message", "message.json")
        if not os.path.exists(p):
            return {}
        j = load_json(p)
        return {e["NAME_LABEL"]: e["MESSAGE"] for e in j["message_message"]}
    ui_src, ui_ref = load_ui(src), load_ui(ref)
    ui_segs = []
    for label, msg in ui_src.items():
        if is_ui_translatable(msg):
            ui_segs.append({"label": label, "src": msg, "ref": ui_ref.get(label, ""), "dst": ""})
    project["files"]["__ui__/message.json"] = ui_segs
    tot = sum(len(v) for v in project["files"].values())
    with open(out, "w", encoding="utf-8") as f:
        json.dump(project, f, ensure_ascii=False, indent=1)
    print(f"project written: {tot} segments in {len(project['files'])} files")

def strs_sequential_match(refs, strs, i):
    return strs[i]

def cmd_apply(lang, master, project_path, dry=False):
    project = json.load(open(project_path, encoding="utf-8"))
    changed = skipped = 0
    for rel, segs in project["files"].items():
        if not segs:
            continue
        key = "label" if rel == "__ui__/message.json" else "i"
        dst_map = {s[key]: s["dst"] for s in segs if s.get("dst")}
        if rel == "__ui__/message.json":
            p = os.path.join(master, lang, "fixed_data", "message", "message.json")
            j = load_json(p)
            m = dst_map
            for e in j["message_message"]:
                if e["NAME_LABEL"] in m:
                    e["MESSAGE"] = m[e["NAME_LABEL"]]
                    changed += 1
            if not dry:
                save_json(p, j)
            continue
        p = os.path.join(master, lang, rel.replace("/", os.sep))
        data = open(p, "rb").read()
        toks = tokenize(data)
        str_tok_indices = [idx for idx, (k, _) in enumerate(toks) if k == "str"]
        trans_tok_indices = [idx for idx in str_tok_indices if is_translatable(toks[idx][1])]

        used_toks = set()
        for s_idx, s in enumerate(segs):
            dst = s.get("dst")
            if not dst:
                skipped += 1
                continue
            src = s.get("src")
            target = None

            # 1. Exact text match
            for ti in trans_tok_indices:
                if ti not in used_toks and toks[ti][1] == src:
                    target = ti
                    break

            # 2. Sequential fallback if index in bounds
            if target is None:
                if s_idx < len(trans_tok_indices) and trans_tok_indices[s_idx] not in used_toks:
                    target = trans_tok_indices[s_idx]

            if target is not None:
                used_toks.add(target)
                toks[target] = ("str", dst)
                changed += 1
            else:
                skipped += 1

        if not dry:
            open(p, "wb").write(detokenize(toks))
    print(f"{'DRY RUN: ' if dry else ''}applied {changed} segments ({skipped} still untranslated)")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "check":
        # check <master_dir> <lang>
        cmd_check(sys.argv[2], sys.argv[3])
    elif cmd == "extract":
        # extract <src_lang> <ref_lang> <master_dir> <out.json>
        cmd_extract(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif cmd == "apply":
        # apply <lang> <master_dir> <project.json> [--dry]
        cmd_apply(sys.argv[2], sys.argv[3], sys.argv[4], "--dry" in sys.argv)
