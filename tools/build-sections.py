#!/usr/bin/env python3
"""
Regenerate sections.v2/ from the full-page builds in "main pages"/*.v2.html.

Run it after editing any .v2.html page:

    python3 tools/build-sections.py

It overwrites sections.v2/ completely, so treat "main pages" as the source of
truth and never hand-edit a file under sections.v2/ that you want to keep.
(If you'd rather edit sections directly, just stop running this script — the
section files are plain HTML and stand on their own.)

Boundaries are parsed, not hardcoded, so the pages can grow or shrink freely.
"""
import re, os, json, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC  = os.path.join(REPO, "main pages")
OUT  = os.path.join(REPO, "sections.v2")

# page file -> (folder, new-id stem, [slug per section, in page order])
# Slugs name the files and the data-zoley-section keys, so changing one is a
# content change in Squarespace too. Order must match the page.
PAGES = {
 "zoley-homepage.v2.html": ("homepage", "zly-hy",
   ["hero","capabilities","approach","who-we-are","resources","featured","testimonials","final-cta"]),
 "zoley-ai-page.v2.html": ("ai", "zly-ai",
   ["hero","adoption-gap","what-we-do","current-state","advise-against","how-we-do-it","case-study","final-cta"]),
 "zoley-automation-page.v2.html": ("automation", "zly-auto",
   ["hero","cost-of-manual-work","what-we-automate","current-state","where-to-start","how-we-do-it","case-study","final-cta"]),
 "zoley-digital-advertising-page.v2.html": ("advertising", "zly-ads",
   ["hero","cost-of-guessing","what-we-do","current-state","advise-against","how-we-do-it","tracking-metrics","case-study","final-cta"]),
 "zoley-strategic-consulting-page.v2.html": ("consulting", "zly-consulting",
   ["hero","cost-of-guessing","what-we-do","current-state","what-you-receive","how-we-do-it","case-study","final-cta"]),
 "zoley-web-design-page.v2.html": ("web-design", "zly-web",
   ["hero","cost-of-slow-site","what-we-do","current-state","signs","how-we-do-it","what-we-measure","case-study","final-cta"]),
 # These pages already ship one <div> per section; slugs rename the files only.
 "zoley-about.v2.html": ("about", None, ["hero","story","how-we-work","principles","final-cta"]),
 "zoley-pricing.v2.html": ("pricing", None, ["hero","what-shapes-a-quote","two-paths"]),
 "zoley-quickstart.v2.html": ("quickstart", None, ["hero","form","next-steps"]),
 "zoley-build.v2.html": ("build", None, ["hero","lead-magnet","services","validation","final-cta"]),
 "zoley-case-studies.v2.html": ("case-studies", None, ["hero","how-we-measure","grid","final-cta"]),
}

PAGE_URLS = {"homepage":"/","ai":"/ai","automation":"/automation","advertising":"/digital-advertising",
 "consulting":"/strategic-consulting","web-design":"/web-design","about":"/about","pricing":"/pricing",
 "quickstart":"/find-your-next-best-business-move","build":"/build","case-studies":"/case-studies"}

ORDER = ["homepage","ai","automation","advertising","consulting","web-design",
         "about","pricing","quickstart","build","case-studies"]

DEF_RE = re.compile(
    r'<(linearGradient|radialGradient|filter|clipPath|mask|pattern|symbol)\b[^>]*\sid="([^"]+)"[^>]*?(?:/>|>.*?</\1>)', re.S)

# Runs the body immediately if the document already finished loading, which is
# what happens when the loader injects a section after DOMContentLoaded.
GUARD = ('(function(run){ if (document.readyState !== "loading") { run(); }\n'
         '  else { document.addEventListener("DOMContentLoaded", run); } })(() => {')
DCL = 'document.addEventListener("DOMContentLoaded", () => {'


def collect_defs(text):
    return {m.group(2): m.group(0) for m in DEF_RE.finditer(text)}


def needed_defs(markup, css, page_defs):
    """Gradient ids this fragment uses but does not define."""
    have = set(collect_defs(markup))
    need = set(re.findall(r'url\(#([^)\'"]+)\)', markup))
    used = {c for grp in re.findall(r'class="([^"]*)"', markup) for c in grp.split()}
    for sel, decl in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        refs = re.findall(r'url\(#([^)\'"]+)\)', decl)
        if refs and set(re.findall(r'\.([A-Za-z0-9_-]+)', sel)) & used:
            need.update(refs)
    return [d for d in sorted(need - have) if d in page_defs]


def defs_block(missing, page_defs):
    if not missing:
        return ""
    inner = "\n      ".join(page_defs[d] for d in missing)
    return ('\n  <!-- Gradient definitions this section needs. On the full page they live in\n'
            '       the hero SVG; this hidden copy lets the section stand alone. Keep it. -->\n'
            '  <svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">\n'
            f'    <defs>\n      {inner}\n    </defs>\n  </svg>\n')


def tokenize(css):
    """Split CSS into (kind, selector, body, raw). Handles one level of nesting."""
    toks, i, n, buf = [], 0, len(css), ""
    while i < n:
        if css[i] == '@' and css[i:].lstrip('@').startswith('import'):
            # Find the ';' that ends the at-rule - not one inside url(...) or a
            # quoted string. Google Fonts URLs contain ';' between weights, and
            # cutting there leaves an unterminated string that kills the sheet.
            j, depth, quote = i, 0, None
            while j < n:
                ch = css[j]
                if quote:
                    if ch == quote and css[j-1] != '\\': quote = None
                elif ch in '"\'': quote = ch
                elif ch == '(': depth += 1
                elif ch == ')': depth -= 1
                elif ch == ';' and depth == 0: break
                j += 1
            toks.append(('import', None, None, css[i:j+1])); i = j + 1; buf = ""; continue
        if css[i] == '{':
            sel, depth, j = buf.strip(), 1, i+1
            while depth:
                if css[j] == '{': depth += 1
                elif css[j] == '}': depth -= 1
                j += 1
            toks.append(('at' if sel.startswith('@') else 'rule', sel, css[i+1:j-1], sel + " " + css[i:j]))
            i = j; buf = ""; continue
        buf += css[i]; i += 1
    return toks


def css_for(css, sid):
    """Rules belonging to #sid, keeping @media wrappers and any @keyframes they use."""
    toks = tokenize(css)
    out = []
    kf = {s.split()[1].strip(): r for k, s, b, r in toks if k == 'at' and s.startswith('@keyframes')}
    for k, sel, body, raw in toks:
        if k == 'rule' and f"#{sid}" in sel:
            out.append(raw)
        elif k == 'at' and sel.startswith('@media'):
            inner = [r for kk, ss, bb, r in tokenize(body) if kk == 'rule' and f"#{sid}" in ss]
            if inner:
                out.append(sel + " {\n  " + "\n  ".join(inner) + "\n}")
    joined = "\n".join(out)
    imports = [t[3] for t in toks if t[0] == 'import']
    used_kf = [r for name, r in kf.items() if re.search(r'\b' + re.escape(name) + r'\b', joined)]
    return imports + used_kf + out


def header(folder, title, source, sid):
    return (f"<!--\nZOLEY - {folder} - {title}\nGenerated from main pages/{source} by tools/build-sections.py\n"
            f"Scoped under #{sid}. Self-contained: paste into a Squarespace Code Block as-is.\n-->\n\n")


def pretty(slug):
    t = slug.replace('-', ' ').title()
    t = re.sub(r"'([A-Z])", lambda m: "'" + m.group(1).lower(), t)
    return t.replace("Cta", "CTA").replace("Ai ", "AI ")


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    manifest = {}

    for fname, (folder, stem, slugs) in PAGES.items():
        path = os.path.join(SRC, fname)
        text = open(path).read()
        lines = text.split("\n")
        page_defs = collect_defs(text)
        os.makedirs(os.path.join(OUT, folder), exist_ok=True)
        entries = []

        top_divs = [i for i, l in enumerate(lines) if re.match(r'<div id="[^"]+">\s*$', l)]

        if stem:  # ---- one wrapper div, numbered section comments inside ----
            assert len(top_divs) == 1, f"{fname}: expected 1 wrapper div, found {len(top_divs)}"
            dopen = top_divs[0]
            wid = re.match(r'<div id="([^"]+)">', lines[dopen]).group(1)
            dclose = next(i for i in range(len(lines)-1, dopen, -1) if lines[i].rstrip() == "</div>")
            sopen  = next(i for i in range(dopen, dclose) if lines[i].strip() == "<style>")
            sclose = next(i for i in range(sopen, dclose) if lines[i].strip() == "</style>")
            css  = "\n".join(lines[sopen+1:sclose])
            body = lines[sclose+1:dclose]

            starts = [i for i, l in enumerate(body) if re.match(r'\s*<!--\s*\d+\.', l)]
            assert len(starts) == len(slugs), \
                f"{fname}: page has {len(starts)} sections but {len(slugs)} slugs are configured"

            for j, s in enumerate(starts):
                e = starts[j+1] if j+1 < len(starts) else len(body)
                sid = f"{stem}-{slugs[j]}"
                markup = "\n".join(body[s+1:e]).rstrip().replace(f"#{wid}", f"#{sid}")
                scss   = css.replace(f"#{wid}", f"#{sid}")
                miss   = needed_defs(markup, scss, page_defs)
                out = (header(folder, pretty(slugs[j]), fname, sid) +
                       f'<div id="{sid}">\n  <style>\n{scss}\n  </style>\n'
                       f'{defs_block(miss, page_defs)}\n{markup}\n</div>\n')
                fn = f"{j+1:02d}-{slugs[j]}.html"
                open(os.path.join(OUT, folder, fn), "w").write(out)
                entries.append({"file": fn, "id": sid, "title": pretty(slugs[j]),
                                "key": f"{folder}/{fn[:-5]}", "defs_injected": miss})
        else:     # ---- already one div per section ----
            assert len(top_divs) == len(slugs), \
                f"{fname}: page has {len(top_divs)} divs but {len(slugs)} slugs are configured"
            sopen  = next(i for i, l in enumerate(lines) if l.strip() == "<style>")
            sclose = next(i for i in range(sopen, len(lines)) if lines[i].strip() == "</style>")
            css = "\n".join(lines[sopen+1:sclose])

            for j, dopen in enumerate(top_divs):
                sid = re.match(r'<div id="([^"]+)">', lines[dopen]).group(1)
                dclose = next(i for i in range(dopen+1, len(lines)) if lines[i].rstrip() == "</div>")
                markup = "\n".join(lines[dopen+1:dclose]).rstrip()
                rules = css_for(css, sid)
                assert len(rules) > 1, f"{fname}: no CSS found for #{sid}"
                block = "\n".join("    " + l if l.strip() else l
                                  for r in rules for l in r.split("\n"))
                out = (header(folder, pretty(slugs[j]), fname, sid) +
                       f'<div id="{sid}">\n  <style>\n{block}\n  </style>\n\n{markup}\n</div>\n')
                fn = f"{j+1:02d}-{slugs[j]}.html"
                open(os.path.join(OUT, folder, fn), "w").write(out)
                entries.append({"file": fn, "id": sid, "title": pretty(slugs[j]),
                                "key": f"{folder}/{fn[:-5]}", "defs_injected": []})

        manifest[folder] = {"source": fname, "sections": entries}

    attach_page_scripts(manifest)
    write_readme(manifest)
    json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=2)
    total = sum(len(v["sections"]) for v in manifest.values())
    print(f"built {total} sections across {len(manifest)} pages -> sections.v2/")
    return manifest


def attach_page_scripts(manifest):
    """The homepage keeps its JS in one block below the markup. Split it so each
    behaviour travels with the section that owns it."""
    src = open(os.path.join(SRC, "zoley-homepage.v2.html")).read()
    blocks = re.findall(r'^document\.addEventListener\("DOMContentLoaded".*?^\}\);', src, re.S | re.M)
    assert len(blocks) == 2, f"homepage: expected 2 DOMContentLoaded blocks, found {len(blocks)}"
    targets = [("02-capabilities.html", "zly-hy-capabilities"),
               ("07-testimonials.html", "zly-hy-testimonials")]
    for (fn, sid), js in zip(targets, blocks):
        assert js.startswith(DCL)
        js = (GUARD + js[len(DCL):]).replace("#zly-hy ", f"#{sid} ")
        p = os.path.join(OUT, "homepage", fn)
        s = open(p).read().rstrip()
        assert s.endswith("</div>")
        indented = "\n".join("  " + l if l.strip() else l for l in js.split("\n"))
        open(p, "w").write(s[:-len("</div>")].rstrip() +
                           f"\n\n  <script>\n{indented}\n  </script>\n</div>\n")


def write_readme(manifest):
    o = ["# Zoley website - v2 sections\n",
         "Generated by `tools/build-sections.py` from the `.v2.html` files in `main pages/`.",
         "Every section is **self-contained**: it carries its own scoped CSS and renders on its own.\n",
         "## Squarespace wiring\n",
         "**Once**, in Settings -> Advanced -> Code Injection -> **Header**:\n",
         '```html\n<script src="https://cdn.jsdelivr.net/gh/ZoleyZoley/zoley-website@v1.0.1/dist/zoley-loader.js"></script>\n```\n',
         "Then give each page one Code Block per section, each holding a single line (listed below).",
         "Paste those once; you never touch them again.\n",
         "**To ship a change:** edit the section -> `git push` -> `git tag v1.0.2 && git push --tags` ->",
         "change `@v1.0.1` to `@v1.0.2` in the header snippet. That number is the only thing you edit in Squarespace.\n",
         "> Pinned tags, not `@main`: jsDelivr caches a branch for 12h at the edge and **7 days in a browser",
         "> that already loaded it**. Exact tags are immutable and go live immediately.\n", "---\n"]
    for folder in ORDER:
        v = manifest[folder]
        o.append(f"## {folder} -> `{PAGE_URLS[folder]}`\n")
        o.append(f"Source: `main pages/{v['source']}` - {len(v['sections'])} sections\n")
        o.append("| # | Section | File | Wrapper id |")
        o.append("|---|---|---|---|")
        for i, s in enumerate(v["sections"], 1):
            o.append(f"| {i} | {s['title']} | `{folder}/{s['file']}` | `#{s['id']}` |")
        o.append("\n```html")
        o += [f'<div data-zoley-section="{s["key"]}"></div>' for s in v["sections"]]
        o.append("```\n")
    open(os.path.join(OUT, "README.md"), "w").write("\n".join(o))


if __name__ == "__main__":
    build()
