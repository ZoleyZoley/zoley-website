import re, os, json

SRC = "/Users/ryan/Library/CloudStorage/OneDrive-Personal/VS Code/Zoley/Website Code/main pages"
OUT = "/Users/ryan/Library/CloudStorage/OneDrive-Personal/VS Code/Zoley/Website Code/sections.v2"

# ---------- monolithic pages: (file, wrapper_id, div_open, style_open, style_close, div_close, folder, [slugs]) ----------
MONO = [
 ("zoley-homepage.v2.html","zly-hy",23,24,286,650,"homepage",
  ["hero","capabilities","approach","who-we-are","resources","featured","testimonials","final-cta"]),
 ("zoley-ai-page.v2.html","zly-ai-page",16,17,167,422,"ai",
  ["hero","adoption-gap","what-we-do","current-state","advise-against","how-we-do-it","case-study","final-cta"]),
 ("zoley-automation-page.v2.html","zly-auto-page",15,16,163,408,"automation",
  ["hero","cost-of-manual-work","what-we-automate","current-state","where-to-start","how-we-do-it","case-study","final-cta"]),
 ("zoley-digital-advertising-page.v2.html","zly-ads-page",17,18,173,427,"advertising",
  ["hero","cost-of-guessing","what-we-do","current-state","advise-against","how-we-do-it","tracking-metrics","case-study","final-cta"]),
 ("zoley-strategic-consulting-page.v2.html","zly-consulting-page",15,16,161,383,"consulting",
  ["hero","cost-of-guessing","what-we-do","current-state","what-you-receive","how-we-do-it","case-study","final-cta"]),
 ("zoley-web-design-page.v2.html","zly-web-page",17,18,174,440,"web-design",
  ["hero","cost-of-slow-site","what-we-do","current-state","signs","how-we-do-it","what-we-measure","case-study","final-cta"]),
]

# new id stem per folder
STEM = {"homepage":"zly-hy","ai":"zly-ai","automation":"zly-auto","advertising":"zly-ads",
        "consulting":"zly-consulting","web-design":"zly-web"}

DEF_RE = re.compile(r'<(linearGradient|radialGradient|filter|clipPath|mask|pattern|symbol)\b[^>]*\sid="([^"]+)"[^>]*?(?:/>|>.*?</\1>)', re.S)

def collect_defs(text):
    return {m.group(2): m.group(0) for m in DEF_RE.finditer(text)}

manifest = {}

for fname, wid, dopen, sopen, sclose, dclose, folder, slugs in MONO:
    lines = open(os.path.join(SRC, fname)).read().split("\n")
    css  = "\n".join(lines[sopen:sclose-1])          # between <style> and </style>
    body = lines[sclose:dclose-1]                     # between </style> and </div>
    page_defs = collect_defs("\n".join(lines))

    starts = [i for i,l in enumerate(body) if re.match(r'\s*<!--\s*\d+\.', l)]
    assert len(starts)==len(slugs), f"{fname}: {len(starts)} sections vs {len(slugs)} slugs"

    stem = STEM[folder]
    os.makedirs(os.path.join(OUT, folder), exist_ok=True)
    entries=[]

    for j, s in enumerate(starts):
        e = starts[j+1] if j+1 < len(starts) else len(body)
        seg = body[s:e]
        title = re.sub(r'^\s*<!--\s*|\s*-->\s*$','', seg[0]).strip()
        slug  = slugs[j]
        nid   = f"{stem}-{slug}"

        markup = "\n".join(seg[1:]).rstrip()          # drop the "<!-- N. X -->" marker line
        scss   = css.replace(f"#{wid}", f"#{nid}")
        markup = markup.replace(f"#{wid}", f"#{nid}") # selectors inside inline JS/markup

        # --- repair SVG defs referenced but not defined in this fragment ---
        have = set(collect_defs(markup))
        need = set(re.findall(r'url\(#([^)\'"]+)\)', markup))   # direct SVG references
        # plus: gradients reached via a CSS rule whose class this section actually uses
        used_classes = set(re.findall(r'class="([^"]*)"', markup))
        used_classes = {c for grp in used_classes for c in grp.split()}
        for rule in re.findall(r'([^{}]+)\{([^{}]*)\}', scss):
            sel, decl = rule
            refs = re.findall(r'url\(#([^)\'"]+)\)', decl)
            if not refs: continue
            sel_classes = set(re.findall(r'\.([A-Za-z0-9_-]+)', sel))
            if sel_classes & used_classes:
                need.update(refs)
        missing = [d for d in sorted(need - have) if d in page_defs]
        defs_block = ""
        if missing:
            inner = "\n      ".join(page_defs[d] for d in missing)
            defs_block = (
        '\n  <!-- Gradient definitions this section needs. They live in the hero SVG on the\n'
        '       full page; this hidden SVG makes the section stand alone. Do not delete. -->\n'
        '  <svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">\n'
        f'    <defs>\n      {inner}\n    </defs>\n  </svg>\n')

        out = (f"<!--\nZOLEY — {folder.upper()} — {title}\nSource: main pages/{fname}\n"
               f"Scoped under #{nid}. Self-contained: drop into a Squarespace Code Block.\n-->\n\n"
               f'<div id="{nid}">\n  <style>\n{scss}\n  </style>\n{defs_block}\n{markup}\n</div>\n')

        path = os.path.join(OUT, folder, f"{j+1:02d}-{slug}.html")
        open(path,"w").write(out)
        entries.append({"file":f"{j+1:02d}-{slug}.html","id":nid,"title":title,
                        "key":f"{folder}/{slug}","defs_injected":missing})
    manifest[folder]={"source":fname,"sections":entries}

print(json.dumps({k:[s['key'] for s in v['sections']] for k,v in manifest.items()}, indent=1))
json.dump(manifest, open("/private/tmp/claude-501/-Users-ryan-Library-CloudStorage-OneDrive-Personal-VS-Code-Zoley/2b6b716a-4f7a-4957-b675-165e0bbd6f20/scratchpad/mono.json","w"), indent=1)
