# Build a starter glossary draft from the project file: frequent terms + proper nouns
import json, os, re, collections, sys
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)

PROJECT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PROJECT_ROOT, "project_yumia_es_en.json")
OUT_MD = sys.argv[2] if len(sys.argv) > 2 else os.path.join(PROJECT_ROOT, "glossary_draft.md")

proj = json.load(open(PROJECT, encoding="utf-8"))

STOP = set("""de la el los las del al un una unos unas y o en con por para que se su sus lo le les
es son esta este estos estas eso esa ese mi tu su nuestro vuestro yo tu el ella nosotros vosotros
no ni si ya muy mas más pero como cuando donde donde cual cuales quien qué que ha han he has have
the of and to in is it for on with as at by from or an be was were are you your this that these
those not all can will would could should there their his her its our they them we he she i
sí no gracias hola adiós bien mal muy pero porque pues entonces ahora después antes también
también sólo solo aún aun algo alguien algo nada nadie cada otro otra otros otras mismo misma
one two three es está está era fue será son estás estén""".split())

words = collections.Counter()
bigrams = collections.Counter()   # capitalized multi-word names e.g. "Ryza中西"
examples = {}

def feed(src, ref):
    # single words from ES
    for w in re.findall(r"[A-Za-zÀ-ÿ]{4,}", src):
        wl = w.lower()
        if wl in STOP:
            continue
        words[wl] += 1
        if wl not in examples:
            examples[wl] = (src[:90], ref[:90] if ref else "")
    # proper-noun bigrams (both words capitalized) from ES or EN
    text = src + " || " + ref
    for m in re.finditer(r"\b([A-ZÀ-Þ][a-zà-ÿ]{2,})\s+([A-ZÀ-Þ][a-zà-ÿ]{2,})\b", text):
        side = m.group(0)
        bigrams[side] += 1

for fname, segs in proj["files"].items():
    for s in segs:
        feed(s.get("src", ""), s.get("ref", ""))

# filter names that are just normal words (appear lowercase too)
def is_name(bg):
    a, b = bg.split(" ", 1)
    return not (a.lower() in words and b.lower() in words and words[a.lower()] > 2 and words[b.lower()] > 2)

top_words = [(w, c) for w, c in words.most_common(400) if c >= 8][:150]
top_names = [(n, c) for n, c in bigrams.most_common(120) if c >= 3 and is_name(n)][:50]

with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("# Glossario di bozza - da completare (formato glossary.json: {\"termine\": \"traduzione\"})\n\n")
    f.write("## Nomi propri (personaggi/luoghi) - più critici da fissare\n\n")
    f.write("| Termine (ES/EN) | Freq | Italiano proposto |\n|---|---|---|\n")
    for n, c in top_names:
        f.write(f"| {n} | {c} | |\n")
    f.write("\n## Termini ricorrenti (verbi/nomi comuni utili per coerenza)\n\n")
    f.write("| Termine | Freq | Esempio |\n|---|---|---|\n")
    for w, c in top_words[:80]:
        ex, exref = examples[w]
        f.write(f"| {w} | {c} | {ex} |\n")

print(f"names: {len(top_names)}, words: {len(top_words)} -> {OUT_MD}")
print("\nTop 25 nomi propri:")
for n, c in top_names[:25]:
    print(f"  {c:4d}  {n}")
print("\nTop 20 termini ricorrenti:")
for w, c in top_words[:20]:
    print(f"  {c:5d}  {w}")
