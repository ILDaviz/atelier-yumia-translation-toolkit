# yumia_translate.py - concurrent AI translation for the Yumia project file
# Works with any OpenAI-compatible endpoint (Ollama, OpenAI, Gemini via proxy, LM Studio...)
#
# Usage:
#   python yumia_translate.py project.json --endpoint http://localhost:11434/v1 --model qwen2.5:7b-instruct \
#       [--api-key KEY] [--workers 8] [--batch-chars 3000] [--glossary glossary.json] [--max-passes 5]
#
# Resumable: re-run the same command to fill only missing translations.
import json, os, re, sys, time, random, argparse, threading, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

LOCK = threading.Lock()
STATS = {"done": 0, "failed": 0}
ABORT = False

class FatalError(Exception):
    pass

def chat(endpoint, api_key, model, system, user, timeout=180):
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
    }
    if not any(k in model.lower() for k in ["luna", "o1", "o3", "o4", "gpt-5", "gpt-6"]):
        payload["temperature"] = 0.3
    req = urllib.request.Request(
        endpoint.rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key or 'none'}"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))["choices"][0]["message"]["content"]

def build_system(glossary):
    g = ""
    if glossary:
        g = "\nGlossary (use EXACTLY these Italian terms):\n" + "\n".join(
            f"- {k} => {v}" for k, v in glossary.items())
    return (
        "You are a professional video game localizer translating Spanish to Italian "
        "for the JRPG 'Atelier Yumia'. Translate each numbered Spanish line into natural, "
        "correct Italian suitable for a fantasy alchemy adventure.\n"
        "Rules:\n"
        "- NEVER merge, split, reorder or skip lines. Output exactly one line per input ID.\n"
        "- CRITICAL - preserve ALL angle-bracket tags and placeholders EXACTLY as in the source: "
        "highlight tags like <CLEG>...</CLNR>, key-binding placeholders like "
        "<KEY_ASSIGN_FIELD_SET_UP_GUN>, and any %s, {0}, \\n, [ff0000] style codes. "
        "Keep each tag in the same position relative to the words it wraps "
        "(<CLEG>kit de reparación<CLNR> => <CLEG>kit di riparazione<CLNR>). "
        "Never translate, rename, add or drop a tag.\n"
        "- If the source contains line breaks, output the translation on a single line.\n"
        "- Keep character/speaker names consistent. Keep register friendly and adventurous.\n"
        "- Keep line lengths similar to the source when possible (UI constraints).\n"
        "- Output format: 'ID<TAB>translation' - nothing else, no explanations.\n" + g)

TAG = re.compile(r"<[A-Za-z0-9_]+>")

def tags_ok(src, dst):
    """Translation is accepted only if it preserves every tag, in the same count."""
    s = sorted(TAG.findall(src))
    d = sorted(TAG.findall(dst))
    return s == d

def translate_batch(cfg, system, segs):
    """segs: list of dicts with id/src/ref. Returns (dict id->translation, last_error)."""
    lines = []
    for s in segs:
        if s.get("ref"):
            lines.append(f"{s['id']}\t[EN ref: {s['ref']}]\nES: {s['src']}")
        else:
            lines.append(f"{s['id']}\t{s['src']}")
    user = "\n".join(lines)
    out = {}
    last_err = ""
    for attempt in range(8):
        if ABORT:
            break
        try:
            text = chat(cfg.endpoint, cfg.api_key, cfg.model, system, user)
            for ln in text.splitlines():
                if "\t" not in ln:
                    continue
                tid, _, val = ln.partition("\t")
                tid = tid.strip()
                val = " ".join(val.split())          # collapse any embedded newlines
                if tid in {s["id"] for s in segs} and val.strip():
                    src_of = next((s["src"] for s in segs if s["id"] == tid), "")
                    if tags_ok(src_of, val):          # reject lost/duplicated tags
                        out[tid] = val.strip()
            if len(out) >= len(segs):          # complete
                return out, ""
            last_err = f"incomplete {len(out)}/{len(segs)}"   # tag-rejects or format misses
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode(errors="replace")[:200]
            except Exception:
                body = ""
            last_err = f"HTTP {e.code} {body}"
            if "1113" in body.lower() or "insufficient" in body.lower():
                raise FatalError(last_err)            # out of quota: stop everything
            if e.code == 429 or "rate" in body.lower():
                time.sleep(min(8 * (attempt + 1), 60) + random.uniform(0, 3))
                continue
        except Exception as e:
            last_err = f"{type(e).__name__}: {str(e)[:120]}"
        time.sleep(min(2 ** attempt * 2, 30) + random.uniform(0, 2))
    return out, last_err

def do_batch(cfg, system, segs, project, ppath):
    global STATS, ABORT
    if ABORT:
        return
    try:
        res, err = translate_batch(cfg, system, segs)
    except FatalError as e:
        with LOCK:
            ABORT = True
            STATS["failed"] += sum(1 for s in segs if not s.get("dst"))
            print(f"*** ABORT: quota esaurita o blocco account: {e}", flush=True)
        return
    with LOCK:
        for s in segs:
            if s["id"] in res:
                s["dst"] = res[s["id"]]
                STATS["done"] += 1
            else:
                STATS["failed"] += 1
        # periodic save (resume support)
        with open(ppath, "w", encoding="utf-8") as f:
            json.dump(project, f, ensure_ascii=False)
        total = STATS["done"] + STATS["failed"]
        msg = f"[{total}] +{len(res)}/{len(segs)}  (tot ok={STATS['done']}, miss={STATS['failed']})"
        if len(res) < len(segs):
            msg += f"  ERR: {err[:150]}"
        print(msg, flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--endpoint", required=True, help="OpenAI-compatible base URL (e.g. http://localhost:11434/v1)")
    ap.add_argument("--model", required=True)
    ap.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY", ""))
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--batch-chars", type=int, default=3000)
    ap.add_argument("--glossary", default="")
    ap.add_argument("--max-passes", type=int, default=5, help="retry passes for missed lines")
    cfg = ap.parse_args()

    project = json.load(open(cfg.project, encoding="utf-8"))
    glossary = json.load(open(cfg.glossary, encoding="utf-8")) if cfg.glossary else None
    system = build_system(glossary)

    # 1) collect ALL untranslated segments across files (global pool, better thread utilization)
    segs_by_id = {}
    for fname, segs in project["files"].items():
        for s in segs:
            if s.get("dst"):
                continue
            sid = f"{fname}::{s.get('i', s.get('label'))}"
            s["id"] = sid
            segs_by_id[sid] = s
    todo = list(segs_by_id.values())
    print(f"segments to translate: {len(todo)}")
    if not todo:
        return

    # 2) batch by character budget, keeping same-file segments together
    batches, cur, size = [], [], 0
    for s in todo:
        ln = len(s["src"]) + len(s.get("ref", "")) + 20
        if cur and size + ln > cfg.batch_chars:
            batches.append(cur); cur, size = [], 0
        cur.append(s); size += ln
    if cur:
        batches.append(cur)
    print(f"{len(batches)} batches, {cfg.workers} workers")

    t0 = time.time()
    for p in range(cfg.max_passes):
        remaining = [b for b in batches if any(not s.get("dst") for s in b)]
        if not remaining:
            break
        if p:
            print(f"pass {p+1}: retrying {len(remaining)} incomplete batches")
        with ThreadPoolExecutor(max_workers=cfg.workers) as ex:
            futs = [ex.submit(do_batch, cfg, system, b, project, cfg.project) for b in remaining]
            for f in as_completed(futs):
                f.result()
        if ABORT:
            print("arresto: quota/blocco rilevato, progetto salvato (riavviabile)")
            break
    with open(cfg.project, "w", encoding="utf-8") as f:
        json.dump(project, f, ensure_ascii=False, indent=1)
    dt = time.time() - t0
    print(f"DONE in {dt/60:.1f} min - ok={STATS['done']} missing={STATS['failed']}")
    print("re-run the same command to fill any missed lines")

if __name__ == "__main__":
    main()
