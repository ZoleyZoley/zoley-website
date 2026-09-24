import re, os, json
SRC="/Users/ryan/Library/CloudStorage/OneDrive-Personal/VS Code/Zoley/Website Code/main pages"
OUT="/Users/ryan/Library/CloudStorage/OneDrive-Personal/VS Code/Zoley/Website Code/sections.v2"

# file, style_open, style_close, folder, [(div_id, slug)]
PRE=[
 ("zoley-about.v2.html",14,108,"about",
  [("zly-about-hero","hero"),("zly-about-story","story"),("zly-about-how","how-we-work"),
   ("zly-about-values","principles"),("zly-about-cta","final-cta")]),
 ("zoley-build.v2.html",13,157,"build",
  [("zly-build-hero","hero"),("zly-build-magnet","lead-magnet"),("zly-build-services","services"),
   ("zly-build-validate","validation"),("zly-build-cta","final-cta")]),
 ("zoley-case-studies.v2.html",13,86,"case-studies",
  [("zly-cs-hero","hero"),("zly-cs-measure","how-we-measure"),("zly-cs-grid","grid"),("zly-cs-cta","final-cta")]),
 ("zoley-pricing.v2.html",13,94,"pricing",
  [("zly-price-hero","hero"),("zly-price-shape","what-shapes-a-quote"),("zly-price-paths","two-paths")]),
 ("zoley-quickstart.v2.html",15,93,"quickstart",
  [("zly-quickstart-hero","hero"),("zly-quickstart-form","form"),("zly-quickstart-next","next-steps")]),
]

def tokenize(css):
    """Split top-level CSS into (kind, selector, body, raw) tokens."""
    toks=[]; i=0; n=len(css); buf=""
    while i<n:
        c=css[i]
        if c=='@' and css[i:].lstrip('@').startswith('import'):
            j=css.index(';',i); toks.append(('import',None,None,css[i:j+1])); i=j+1; buf=""; continue
        if c=='{':
            sel=buf.strip(); depth=1; j=i+1
            while depth>0:
                if css[j]=='{': depth+=1
                elif css[j]=='}': depth-=1
                j+=1
            raw=css[i:j]           # includes braces
            body=css[i+1:j-1]
            kind='at' if sel.startswith('@') else 'rule'
            toks.append((kind,sel,body,sel+" "+raw)); i=j; buf=""; continue
        buf+=c; i+=1
    return toks

def css_for(css, sid):
    """Return the CSS that belongs to #sid, preserving @media wrappers and needed @keyframes."""
    out=[]; toks=tokenize(css)
    imports=[t[3] for t in toks if t[0]=='import']
    kf={}
    for k,sel,body,raw in toks:
        if k=='at' and sel.startswith('@keyframes'):
            kf[sel.split()[1].strip()]=raw
    for k,sel,body,raw in toks:
        if k=='rule':
            if f"#{sid}" in sel: out.append(raw)
        elif k=='at' and sel.startswith('@media'):
            inner=[r for kk,ss,bb,r in tokenize(body) if kk=='rule' and f"#{sid}" in ss]
            if inner:
                out.append(sel+" {\n  "+"\n  ".join(inner)+"\n}")
    joined="\n".join(out)
    used=[raw for name,raw in kf.items() if re.search(r'\b'+re.escape(name)+r'\b', joined)]
    return imports+used+out

manifest={}
for fname,so,sc,folder,divs in PRE:
    lines=open(os.path.join(SRC,fname)).read().split("\n")
    css="\n".join(lines[so:sc-1])
    text="\n".join(lines)
    os.makedirs(os.path.join(OUT,folder),exist_ok=True)
    entries=[]
    for j,(sid,slug) in enumerate(divs):
        m=re.search(r'^<div id="'+re.escape(sid)+r'">\n(.*?)\n^</div>', text, re.S|re.M)
        assert m, f"{fname}: div {sid} not found"
        markup=m.group(1).rstrip()
        rules=css_for(css,sid)
        assert len(rules)>1, f"{fname}/{sid}: no CSS found"
        body="\n".join("    "+l if l.strip() else l for r in rules for l in r.split("\n"))
        out=(f"<!--\nZOLEY — {folder.upper()} — {slug.replace('-',' ').title()}\n"
             f"Source: main pages/{fname}\nScoped under #{sid}. Self-contained: drop into a Squarespace Code Block.\n-->\n\n"
             f'<div id="{sid}">\n  <style>\n{body}\n  </style>\n\n{markup}\n</div>\n')
        path=os.path.join(OUT,folder,f"{j+1:02d}-{slug}.html")
        open(path,"w").write(out)
        entries.append({"file":f"{j+1:02d}-{slug}.html","id":sid,"key":f"{folder}/{slug}",
                        "title":slug.replace('-',' ').title()})
    manifest[folder]={"source":fname,"sections":entries}
print(json.dumps({k:[s['key'] for s in v['sections']] for k,v in manifest.items()},indent=1))
json.dump(manifest,open("/private/tmp/claude-501/-Users-ryan-Library-CloudStorage-OneDrive-Personal-VS-Code-Zoley/2b6b716a-4f7a-4957-b675-165e0bbd6f20/scratchpad/pre.json","w"),indent=1)
