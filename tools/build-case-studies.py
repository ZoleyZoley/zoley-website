#!/usr/bin/env python3
"""
Render the case study pages from tools/case_study_content.py.

    python3 tools/build-case-studies.py && python3 tools/build-sections.py

Writes one "main pages/zoley-case-study-<key>.v2.html" per case study (each is a
single self-contained section: title, snapshot, story, CTA, newsletter), and
refreshes the cards on "main pages/zoley-case-studies.v2.html" between the
CASE STUDY CARDS START/END markers. build-sections.py then publishes each page
as sections.v2/cs-<key>/01-page.html.

The generated pages are overwritten on every run: edit the content file or the
template below, never the generated .v2.html files.
"""
import os, re, sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC = os.path.join(REPO, "main pages")
sys.path.insert(0, HERE)
from case_study_content import CASE_STUDIES, INDEX_URL  # noqa: E402

QUICKSTART = "https://www.zoley.io/find-your-next-best-business-move"
CALENDLY = "https://calendly.com/zoley/zoley-discovery-call"
NEWSLETTER_ENDPOINT = "https://script.google.com/macros/s/AKfycbxMauQxJhF3SWBEQsbL3HZCYoUTGGx3eYjJZnJz3lN82IAzELAXmortCYFprQLaCu95Vg/exec"

DISCLAIMER = ("This case study reflects a real project with real results. As a standard practice, "
              "we do not name clients in public case studies without their permission. "
              "The details here are accurate to the work performed.")


def e(s):
    return escape(s, quote=False)


def page_file(cs):
    return f"zoley-case-study-{cs['key']}.v2.html"


# ---------------------------------------------------------------- illustration
def value_lines(lines, x, fill):
    longest = max(len(l) for l in lines)
    fs = 42 if longest <= 5 else 36 if longest <= 6 else min(26, int(150 / (0.5 * longest)))
    lh = fs * 1.08
    y0 = 108 - (len(lines) - 1) * lh / 2 + fs * 0.34
    return "\n".join(
        f'<text x="{x}" y="{y0 + i * lh:.0f}" font-family="Newsreader, Georgia, serif" font-size="{fs}" '
        f'font-weight="600" fill="{fill}" text-anchor="middle">{e(l)}</text>'
        for i, l in enumerate(lines))


def illustration(cs):
    il, gid = cs["illustration"], f"{cs['sid']}-grad"
    label = f"Illustration: {il['metric'].lower()}, before {' '.join(il['before'])}, after {' '.join(il['after'])}"
    return f'''<svg viewBox="0 0 420 300" fill="none" role="img" aria-label="{escape(label)}">
          <defs>
            <linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#14457a"/><stop offset="1" stop-color="#6c5ce7"/></linearGradient>
          </defs>
          <text x="210" y="26" font-family="DM Sans, sans-serif" font-size="12" font-weight="700" fill="#1b2430" letter-spacing="1.2" text-anchor="middle">{e(il['metric'])}</text>
          <g transform="rotate(-3 114 140)">
            <rect x="34" y="66" width="160" height="150" rx="8" fill="#fff9ef" stroke="#1b2430" stroke-width="2.5"/>
            <text x="114" y="100" font-family="Caveat, cursive" font-size="22" font-weight="700" fill="#5c6b76" text-anchor="middle">before</text>
            <g transform="translate(0 38)">
            {value_lines(il['before'], 114, '#5c6b76')}
            </g>
          </g>
          <g transform="rotate(3 306 140)">
            <rect x="226" y="66" width="160" height="150" rx="8" fill="#fff9ef" stroke="#1b2430" stroke-width="2.5"/>
            <text x="306" y="100" font-family="Caveat, cursive" font-size="22" font-weight="700" fill="#6c5ce7" text-anchor="middle">after</text>
            <g transform="translate(0 38)">
            {value_lines(il['after'], 306, '#14457a')}
            </g>
            <circle cx="372" cy="204" r="14" fill="#7a8b69" stroke="#1b2430" stroke-width="2"/>
            <path d="M365.5 204 l4.5 4.5 l8 -9" stroke="#fff9ef" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          </g>
          <path d="M116 64 C 160 34, 262 32, 304 62" stroke="url(#{gid})" stroke-width="2.2" stroke-dasharray="6 6" fill="none" opacity="0.85"/>
          <path d="M291 57 L305 64 L300 50" stroke="#6c5ce7" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="116" cy="66" r="7" fill="#14457a" stroke="#1b2430" stroke-width="1.5"/>
          <circle cx="304" cy="64" r="7" fill="#6c5ce7" stroke="#1b2430" stroke-width="1.5"/>
          <text x="210" y="266" font-family="Caveat, cursive" font-size="22" font-weight="700" fill="#1b2430" text-anchor="middle" transform="rotate(-1.5 210 266)">{e(il['note'])}</text>
        </svg>'''


# ---------------------------------------------------------------- story blocks
def block(kind, data, ind="        "):
    if kind == "p":
        return f"{ind}<p>{e(data)}</p>"
    if kind == "ul":
        items = "\n".join(f"{ind}  <li>{e(i)}</li>" for i in data)
        return f'{ind}<ul class="ticks">\n{items}\n{ind}</ul>'
    if kind == "points":
        out = [f'{ind}<ol class="points">']
        for n, (t, txt) in enumerate(data, 1):
            out.append(f'{ind}  <li><span class="pt-n">{n}</span><div><h3>{e(t)}</h3><p>{e(txt)}</p></div></li>')
        out.append(f"{ind}</ol>")
        return "\n".join(out)
    if kind == "parts":
        out = [f'{ind}<div class="parts">']
        for p in data:
            out.append(f'{ind}  <div class="part">')
            out.append(f'{ind}    <span class="part-label">{e(p["label"])}</span>')
            out.append(f'{ind}    <h3>{e(p["title"])}</h3>')
            if p.get("intro"):
                out.append(f'{ind}    <p>{e(p["intro"])}</p>')
            if p.get("list_title"):
                out.append(f'{ind}    <p class="list-title">{e(p["list_title"])}</p>')
            out.append(f'{ind}    <ul class="ticks">')
            out += [f'{ind}      <li>{e(i)}</li>' for i in p["items"]]
            out.append(f'{ind}    </ul>')
            if p.get("outro"):
                out.append(f'{ind}    <p class="part-outro">{e(p["outro"])}</p>')
            out.append(f'{ind}  </div>')
        out.append(f"{ind}</div>")
        return "\n".join(out)
    if kind == "results":
        out = [f'{ind}<div class="results">']
        for group, rows in data:
            out.append(f'{ind}  <div class="r-group">')
            out.append(f'{ind}    <h3>{e(group)}</h3>')
            out.append(f'{ind}    <ul>')
            for val, label, note in rows:
                n = f'<span class="r-note">{e(note)}</span>' if note else ""
                out.append(f'{ind}      <li><span class="r-val">{e(val)}</span><span class="r-label">{e(label)}</span>{n}</li>')
            out.append(f'{ind}    </ul>')
            out.append(f'{ind}  </div>')
        out.append(f"{ind}</div>")
        return "\n".join(out)
    if kind == "diff":
        out = [f'{ind}<div class="diff">']
        for lead, txt in data:
            out.append(f'{ind}  <div class="diff-item"><h3>{e(lead)}</h3><p>{e(txt)}</p></div>')
        out.append(f"{ind}</div>")
        return "\n".join(out)
    raise ValueError(kind)


def story(cs):
    out = []
    for heading, blocks in cs["story"]:
        out.append('      <section class="chapter">')
        out.append(f'        <h2>{e(heading)}</h2>')
        out += [block(k, d) for k, d in blocks]
        out.append('      </section>')
    return "\n".join(out)


# ---------------------------------------------------------------- snapshot
def snapshot(cs):
    s = cs["snapshot"]
    num = f'\n          <p class="snap-impact-number">{e(s["impact_number"])}</p>' if s["impact_number"] else ""
    stats = ""
    if s["stats"]:
        items = "\n".join(f'          <li><span class="snap-stat-num">{e(n)}</span><span class="snap-stat-label">{e(l)}</span></li>'
                          for n, l in s["stats"])
        stats = f'\n      <ul class="snap-stats" aria-label="Key results">\n{items}\n      </ul>'
    return f'''  <section class="snap-wrap" aria-label="Case study at a glance">
    <div class="snap">
      <div class="snap-glow snap-glow-a" aria-hidden="true"></div>
      <div class="snap-glow snap-glow-b" aria-hidden="true"></div>
      <div class="snap-inner">
        <div>
          <span class="snap-tag">at a glance</span>
          <dl>
            <dt>Client</dt>
            <dd class="snap-strong">{e(s['client'])}</dd>
            <dt>Industry</dt>
            <dd>{e(s['industry'])}</dd>
            <dt>What we did</dt>
            <dd>{e(cs['category'])}</dd>
            <dt>Problem</dt>
            <dd>{e(s['problem'])}</dd>
            <dt>Solution</dt>
            <dd>{e(s['solution'])}</dd>
          </dl>
        </div>
        <div class="snap-impact">
          <p class="snap-impact-label">The impact</p>{num}
          <p class="snap-impact-text">{e(s['impact_text'])}</p>
        </div>
      </div>{stats}
    </div>
  </section>'''


# ---------------------------------------------------------------- CSS
CSS = r'''
  @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,600;1,6..72,500&family=DM+Sans:wght@400;500;700&family=Caveat:wght@600;700&display=swap');

  #W {
    --paper: #faf3e7; --paper-2: #f6e4b8; --card: #fff9ef; --ink: #1b2430; --ink-soft: #5c6b76;
    --marigold: #e3a72e; --barn: #14457a; --sage: #7a8b69; --violet: #6c5ce7; --blue: #4ea1ff;
    --border: rgba(27,36,48,0.14);
    font-family: 'DM Sans', -apple-system, sans-serif; background: var(--paper); color: var(--ink);
  }
  #W * { box-sizing: border-box; margin: 0; padding: 0; }
  #W h1, #W h2, #W h3 { font-family: 'Newsreader', Georgia, serif; font-weight: 600; line-height: 1.15; letter-spacing: -0.01em; color: var(--ink); }
  #W p { color: var(--ink-soft); line-height: 1.7; }
  #W a { color: inherit; }

  /* ---------- TITLE ---------- */
  #W .hero { padding: 88px 24px 48px; max-width: 1160px; margin: 0 auto; display: grid; grid-template-columns: 1.05fr 0.95fr; column-gap: 56px; align-items: start; }
  #W .hero-head { grid-column: 1; grid-row: 1; }
  #W .hero-copy { grid-column: 1; grid-row: 2; }
  #W .board { grid-column: 2; grid-row: 2; background: var(--paper-2); border: 1px solid var(--border); border-radius: 14px; padding: 20px; }
  #W .board svg { width: 100%; height: auto; display: block; }
  #W .back { display: inline-flex; align-items: center; min-height: 44px; font-size: 14px; font-weight: 700; text-decoration: none; color: var(--ink-soft); }
  #W .back:hover { color: var(--barn); }
  #W .tag { display: block; width: max-content; max-width: 100%; font-family: 'Caveat', cursive; font-size: 22px; font-weight: 700; color: var(--barn); transform: rotate(-2deg); margin: 4px 0 8px; padding: 0 4px; }
  #W .hero h1 { font-size: clamp(32px, 4vw, 50px); line-height: 1.1; }
  #W .hero .dek { font-size: 18px; margin-top: 20px; max-width: 540px; }

  /* ---------- SNAPSHOT (dark band) ---------- */
  #W .snap-wrap { max-width: 1160px; margin: 0 auto; padding: 0 24px 72px; }
  #W .snap { --snap-text: #fff9ef; --snap-soft: #d4dbe0; --snap-label: #9fb3c8; --snap-line: rgba(250,243,231,0.14);
    position: relative; overflow: hidden; background: var(--ink); color: var(--snap-text); border-radius: 16px; }
  #W .snap-glow { position: absolute; border-radius: 50%; pointer-events: none; }
  #W .snap-glow-a { top: -120px; left: -80px; width: 360px; height: 360px; background: radial-gradient(circle, rgba(108,92,231,0.28), transparent 65%); }
  #W .snap-glow-b { bottom: -140px; right: -60px; width: 380px; height: 380px; background: radial-gradient(circle, rgba(78,161,255,0.2), transparent 65%); }
  #W .snap-inner { position: relative; display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: 36px; padding: 36px 40px; }
  #W .snap-tag { display: block; font-family: 'Caveat', cursive; font-size: 24px; font-weight: 700; line-height: 1; color: var(--marigold); margin: 0 0 6px; }
  #W .snap dl { display: grid; grid-template-columns: 120px minmax(0, 1fr); column-gap: 18px; }
  #W .snap dt { padding: 13px 0; border-bottom: 1px solid var(--snap-line); font-size: 11.5px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--snap-label); }
  #W .snap dd { padding: 11px 0; border-bottom: 1px solid var(--snap-line); font-size: 15px; line-height: 1.55; color: var(--snap-soft); }
  #W .snap dt:last-of-type, #W .snap dd:last-of-type { border-bottom: 0; }
  #W .snap dd.snap-strong { font-size: 15.5px; font-weight: 700; color: var(--snap-text); }
  #W .snap-impact { display: flex; flex-direction: column; justify-content: center; gap: 10px; background: rgba(250,243,231,0.06); border: 1px solid rgba(250,243,231,0.16); border-radius: 12px; padding: 26px 24px; }
  #W .snap-impact-label { font-size: 11.5px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--marigold); }
  #W .snap-impact-number { font-family: 'Newsreader', Georgia, serif; font-size: 44px; font-weight: 600; line-height: 1.05; color: var(--snap-text); }
  #W .snap-impact-text { font-size: 15px; line-height: 1.6; color: var(--snap-soft); }
  #W .snap-stats { position: relative; list-style: none; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); border-top: 1px solid var(--snap-line); }
  #W .snap-stats li { padding: 22px 24px 26px; border-right: 1px solid var(--snap-line); }
  #W .snap-stats li:first-child { padding-left: 40px; }
  #W .snap-stats li:last-child { border-right: 0; padding-right: 40px; }
  #W .snap-stat-num { display: block; font-family: 'Newsreader', Georgia, serif; font-size: 30px; font-weight: 600; line-height: 1.1; color: var(--snap-text); margin-bottom: 6px; }
  #W .snap-stat-label { display: block; font-size: 13.5px; line-height: 1.45; color: var(--snap-soft); }

  /* ---------- STORY ---------- */
  #W .story { max-width: 760px; margin: 0 auto; padding: 0 24px 40px; }
  #W .chapter { padding: 0 0 56px; }
  #W .chapter h2 { font-size: clamp(26px, 3vw, 34px); margin-bottom: 18px; }
  #W .chapter h2::before { content: ''; display: block; width: 36px; height: 3px; border-radius: 2px; background: linear-gradient(90deg, var(--barn), var(--violet)); margin-bottom: 14px; }
  #W .chapter > p { font-size: 17px; margin-bottom: 16px; }
  #W .chapter > p:last-child { margin-bottom: 0; }
  #W .chapter > * + .parts, #W .chapter > * + .points, #W .chapter > * + .results, #W .chapter > * + .diff { margin-top: 24px; }
  #W .parts + p, #W .points + p, #W .diff + p, #W .ticks + p { margin-top: 24px; }
  #W .ticks { list-style: none; margin: 4px 0 16px; }
  #W .ticks li { position: relative; padding-left: 30px; margin-bottom: 10px; font-size: 16px; line-height: 1.6; color: var(--ink); }
  #W .ticks li::before { content: ''; position: absolute; left: 2px; top: 6px; width: 16px; height: 16px; border-radius: 50%; background: var(--sage) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4.5 8.2l2.3 2.3 4.7-5' stroke='%23fff9ef' stroke-width='2' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / 16px no-repeat; }
  #W .points { list-style: none; display: grid; gap: 16px; }
  #W .points li { display: grid; grid-template-columns: 44px minmax(0, 1fr); gap: 14px; background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 24px 24px 24px 20px; }
  #W .pt-n { font-family: 'Caveat', cursive; font-size: 34px; font-weight: 700; line-height: 1; color: var(--violet); text-align: center; }
  #W .points h3 { font-size: 19px; margin-bottom: 8px; }
  #W .points p { font-size: 15.5px; }
  #W .parts { display: grid; gap: 20px; }
  #W .part { position: relative; overflow: hidden; background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 30px 30px 18px; }
  #W .part::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 3px; background: linear-gradient(90deg, var(--barn), var(--violet), var(--blue)); }
  #W .part-label { display: block; font-size: 12px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--barn); margin-bottom: 6px; }
  #W .part h3 { font-size: 22px; margin-bottom: 12px; }
  #W .part > p { font-size: 16px; margin-bottom: 14px; }
  #W .part .list-title { font-size: 13px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink); margin-bottom: 10px; }
  #W .part .part-outro { border-top: 1px solid var(--border); padding-top: 16px; font-style: italic; }
  #W .results { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; }
  #W .r-group { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 22px 22px 8px; }
  #W .r-group h3 { font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--barn); margin-bottom: 6px; }
  #W .r-group ul { list-style: none; }
  #W .r-group li { padding: 14px 0; border-top: 1px solid var(--border); }
  #W .r-group li:first-child { border-top: 0; }
  #W .r-val { display: block; font-family: 'Newsreader', Georgia, serif; font-size: 30px; font-weight: 600; line-height: 1.1; color: var(--barn); }
  #W .r-label { display: block; font-size: 14.5px; line-height: 1.45; color: var(--ink); margin-top: 4px; }
  #W .r-note { display: block; font-size: 13px; line-height: 1.4; color: var(--ink-soft); margin-top: 2px; }
  #W .diff { display: grid; gap: 14px; }
  #W .diff-item { border-left: 4px solid var(--violet); background: var(--card); border-radius: 0 12px 12px 0; padding: 20px 24px; }
  #W .diff-item h3 { font-size: 19px; margin-bottom: 6px; }
  #W .diff-item p { font-size: 15.5px; }
  #W .disclaimer { font-size: 13.5px; line-height: 1.6; color: var(--ink-soft); border: 1px dashed var(--border); border-radius: 10px; padding: 16px 18px; margin-top: -16px; }
  #W .disclaimer strong { color: var(--ink); }

  /* ---------- CTA (same as the homepage) ---------- */
  #W .cta-sec { max-width: 1160px; margin: 0 auto; padding: 40px 24px 56px; }
  #W .sign { background: var(--ink); border-radius: 14px; padding: 60px 40px; text-align: center; position: relative; overflow: hidden; }
  #W .sign::before { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 25% 20%, rgba(108,92,231,0.25), transparent 55%), radial-gradient(circle at 80% 85%, rgba(181,72,45,0.22), transparent 55%); }
  #W .sign > * { position: relative; }
  #W .sign h2 { color: var(--paper); font-size: clamp(28px, 3.2vw, 38px); line-height: 1.1; margin-bottom: 14px; }
  #W .sign p { color: #c7d0d6; max-width: 520px; margin: 0 auto 28px; line-height: 1.65; }
  #W .sign .cta-note { font-size: 13px; color: rgba(244,237,224,0.55); margin: 16px auto 0; }
  #W .cta-row { display: flex; gap: 14px; flex-wrap: wrap; justify-content: center; }
  #W .btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; min-height: 48px; padding: 15px 28px; border-radius: 8px; font-weight: 700; font-size: 15.5px; text-decoration: none; cursor: pointer; font-family: 'DM Sans', sans-serif; transition: transform 0.15s ease, box-shadow 0.15s ease, background-color 0.15s ease; }
  #W .btn-primary { background: var(--barn); color: #fff9ef; box-shadow: 0 4px 0 #0d2d50; border: none; }
  #W .btn-primary:hover { transform: translateY(2px); box-shadow: 0 2px 0 #0d2d50; }
  #W .btn-ghost { background: transparent; color: var(--paper); border: 2px solid var(--paper); }
  #W .btn-ghost:hover { background: var(--paper); color: var(--ink); }

  /* ---------- NEWSLETTER ---------- */
  #W .nl-sec { max-width: 1160px; margin: 0 auto; padding: 0 24px 96px; }
  #W .nl { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.1fr); gap: 40px; align-items: center; background: var(--paper-2); border: 1px solid var(--border); border-radius: 14px; padding: 44px 44px; }
  #W .nl-tag { display: block; width: max-content; font-family: 'Caveat', cursive; font-size: 22px; font-weight: 700; color: var(--barn); transform: rotate(-2deg); margin-bottom: 6px; padding: 0 4px; }
  #W .nl h2 { font-size: clamp(24px, 2.6vw, 30px); margin-bottom: 10px; }
  #W .nl-copy p { font-size: 15.5px; }
  #W .nl-form { display: flex; gap: 10px; flex-wrap: wrap; }
  #W .nl-input { flex: 1 1 200px; min-width: 0; min-height: 48px; padding: 13px 16px; border-radius: 8px; border: 1px solid rgba(27,36,48,0.24); background: #fff; color: var(--ink); font-size: 16px; font-family: 'DM Sans', sans-serif; }
  #W .nl-input.nl-first { flex: 1 1 140px; }
  #W .nl-input::placeholder { color: #8a949b; }
  #W .nl-input:focus { outline: 2px solid var(--barn); outline-offset: 1px; }
  #W .nl-form .btn { flex: 0 0 auto; }
  #W .nl-form .btn:disabled { opacity: 0.7; cursor: wait; }
  #W .nl-hp { position: absolute; left: -9999px; width: 1px; height: 1px; overflow: hidden; }
  #W .nl-status { font-size: 14px; font-weight: 600; margin-top: 12px; }
  #W .nl-status:empty { display: none; }
  #W .nl-status.is-error { color: #a23b2a; }
  #W .nl-status.is-success { color: var(--ink); font-size: 16px; margin-top: 0; }
  #W .nl-fine { font-size: 12.5px; margin-top: 12px; }

  @media (max-width: 900px) {
    #W .hero { grid-template-columns: 1fr; padding: 64px 20px 36px; }
    #W .hero-head, #W .hero-copy, #W .board { grid-column: 1; grid-row: auto; }
    #W .hero-copy { margin-bottom: 36px; }
    #W .snap-wrap { padding: 0 20px 56px; }
    #W .snap-inner { grid-template-columns: 1fr; gap: 24px; padding: 30px 28px; }
    #W .snap-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    #W .snap-stats li, #W .snap-stats li:first-child, #W .snap-stats li:last-child { padding: 20px 28px 22px; }
    #W .snap-stats li:nth-child(2n) { border-right: 0; }
    #W .snap-stats li:nth-child(n+3) { border-top: 1px solid var(--snap-line); }
    #W .story { padding: 0 20px 32px; }
    #W .cta-sec { padding: 32px 20px 48px; }
    #W .nl-sec { padding: 0 20px 64px; }
    #W .nl { grid-template-columns: 1fr; gap: 24px; padding: 34px 28px; }
  }
  @media (max-width: 560px) {
    #W { overflow-x: clip; }
    #W .hero { padding-top: 40px; }
    #W .hero .dek { font-size: 17px; }
    /* Full-bleed illustration on phones, as on the other v2 pages. */
    #W .board { margin-left: calc(50% - 50vw); margin-right: calc(50% - 50vw); border-left: 0; border-right: 0; border-radius: 0; padding-left: 0; padding-right: 0; }
    #W .snap-wrap { padding: 0 16px 48px; }
    #W .snap-inner { padding: 26px 22px; }
    #W .snap dl { grid-template-columns: 1fr; }
    #W .snap dt { padding: 14px 0 4px; border-bottom: 0; }
    #W .snap dd { padding: 0 0 14px; }
    #W .snap-impact { padding: 22px 20px; }
    #W .snap-impact-number { font-size: 36px; }
    #W .snap-stats { grid-template-columns: 1fr; }
    #W .snap-stats li, #W .snap-stats li:first-child, #W .snap-stats li:last-child { padding: 18px 22px; border-right: 0; }
    #W .snap-stats li + li { border-top: 1px solid var(--snap-line); }
    #W .story { padding: 0 18px 24px; }
    #W .chapter > p { font-size: 16.5px; }
    #W .points li { grid-template-columns: 1fr; gap: 4px; padding: 20px; }
    #W .pt-n { text-align: left; }
    #W .part { padding: 26px 20px 14px; }
    #W .results { grid-template-columns: 1fr; }
    #W .sign { padding: 40px 22px; border-radius: 12px; }
    #W .cta-row { flex-direction: column; align-items: stretch; }
    #W .nl { padding: 28px 20px; }
    #W .nl-form { flex-direction: column; }
    #W .nl-input, #W .nl-input.nl-first { flex: 0 0 auto; width: 100%; }
    #W .nl-form .btn { width: 100%; }
  }
'''


# ---------------------------------------------------------------- page
def page(cs):
    sid = cs["sid"]
    disclaimer = (f'\n      <p class="disclaimer"><strong>About this case study.</strong> {e(DISCLAIMER)}</p>'
                  if cs["anonymized"] else "")
    return f'''<!--
ZOLEY CASE STUDY - {cs['title']}
GENERATED by tools/build-case-studies.py from tools/case_study_content.py. Do not edit
this file: change the content file (or the template in the script) and re-run it.

One section for the whole page: title / snapshot / story / CTA / newsletter.
Squarespace page {cs['url']} gets one Code Block:  <div data-zoley-page="cs-{cs['key']}"></div>
-->

<style>
{CSS.replace('#W', '#' + sid).strip(chr(10))}
</style>

<div id="{sid}">
  <section class="hero">
    <div class="hero-head">
      <a class="back" href="{INDEX_URL}">&larr; All case studies</a>
      <span class="tag">{e(cs['category'].lower())}</span>
    </div>
    <div class="hero-copy">
      <h1>{e(cs['title'])}</h1>
      <p class="dek">{e(cs['dek'])}</p>
    </div>
    <div class="board">
        {illustration(cs)}
    </div>
  </section>

{snapshot(cs)}

  <article class="story">
{story(cs)}{disclaimer}
  </article>

  <section class="cta-sec">
    <div class="sign">
      <h2>Let's build what your business needed 6 months ago.</h2>
      <p>Let's pinpoint what's slowing you down, build the right solution, and grow from there.</p>
      <div class="cta-row">
        <a href="{QUICKSTART}" class="btn btn-primary">Get your plan</a>
        <a href="{CALENDLY}" class="btn btn-ghost">Book an intro call</a>
      </div>
      <p class="cta-note">Prefer email? connect@zoley.io</p>
    </div>
  </section>

  <section class="nl-sec">
    <div class="nl">
      <div class="nl-copy">
        <span class="nl-tag">the espresso brief</span>
        <h2>One operational improvement, every week.</h2>
        <p>A single, specific change you can make to how your business runs, with the reasoning behind it. Short enough to act on the same day.</p>
      </div>
      <div>
        <form class="nl-form" novalidate>
          <input type="text" name="first_name" required placeholder="First name" class="nl-input nl-first" aria-label="First name" autocomplete="given-name">
          <input type="email" name="email" required placeholder="you@yourbusiness.com" class="nl-input" aria-label="Email address" autocomplete="email">
          <div class="nl-hp" aria-hidden="true"><label>Company <input type="text" name="company" tabindex="-1" autocomplete="off"></label></div>
          <button type="submit" class="btn btn-primary">Subscribe</button>
        </form>
        <p class="nl-status" role="status" aria-live="polite"></p>
        <p class="nl-fine">One email a week. One thing to improve your business.</p>
      </div>
    </div>
  </section>

  <script>
    (function () {{
      // Espresso Brief signup -> the same Apps Script web app as the homepage and footer.
      var ENDPOINT = "{NEWSLETTER_ENDPOINT}";
      var root = document.getElementById('{sid}');
      var form = root && root.querySelector('.nl-form');
      if (!form || form.getAttribute('data-ready')) return;
      form.setAttribute('data-ready', '1');
      var status = root.querySelector('.nl-status');
      var fine = root.querySelector('.nl-fine');
      var btn = form.querySelector('button[type="submit"]');

      function say(msg, kind) {{ status.textContent = msg; status.className = 'nl-status' + (kind ? ' is-' + kind : ''); }}

      form.addEventListener('submit', function (ev) {{
        ev.preventDefault();
        var first = form.first_name.value.trim();
        var email = form.email.value.trim();
        if (!first) {{ say('Mind adding your first name?', 'error'); form.first_name.focus(); return; }}
        if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{{2,}}$/.test(email)) {{ say("That email doesn't look right. Mind double-checking it?", 'error'); form.email.focus(); return; }}

        btn.disabled = true; say('');
        // Apps Script can't answer the browser's cross-site pre-check, so this is sent as
        // plain text without reading the reply. The script validates everything itself.
        fetch(ENDPOINT, {{
          method: 'POST', mode: 'no-cors',
          body: JSON.stringify({{ form: 'newsletter', first_name: first, email: email, company: form.company.value, source: 'case-study-{cs['key']}' }})
        }}).then(function () {{
          form.hidden = true; fine.hidden = true;
          say("You're in, " + first + ". Check your inbox for a welcome email.", 'success');
        }}).catch(function () {{
          btn.disabled = false;
          say("Something didn't go through. Try again, or email connect@zoley.io.", 'error');
        }});
      }});
    }})();
  </script>
</div>
'''


# ---------------------------------------------------------------- index cards
SPARK_COLORS = ["#6c5ce7", "#14457a", "#7a8b69"]
SPARK = "M0 36 L40 34 L80 33 L120 27 L160 22 L200 16 L240 11 L280 7"


def card(cs, i):
    c = cs["card"]
    col = SPARK_COLORS[i % len(SPARK_COLORS)]
    return f'''      <a class="cs-card" href="https://www.zoley.io{cs['url']}">
        <span class="cs-tag">{e(c['tag'])}</span>
        <h3>{e(c['title'])}</h3>
        <p class="cs-headline">{e(c['headline'])}</p>
        <p class="cs-did"><strong>What we did:</strong> {e(c['did'])}</p>
        <div class="cs-spark"><svg viewBox="0 0 280 44" preserveAspectRatio="none" aria-hidden="true"><path d="{SPARK}" stroke="{col}" stroke-width="2.5" fill="none" stroke-linecap="round"/><path d="{SPARK} L280 44 L0 44 Z" fill="{col}" opacity="0.1"/></svg></div>
        <div class="cs-stat"><span class="num">{e(c['stat'][0])}</span><span class="label">{e(c['stat'][1])}</span></div>
        <span class="cs-link">Read the case study &rarr;</span>
      </a>'''


def write_cards():
    p = os.path.join(SRC, "zoley-case-studies.v2.html")
    text = open(p).read()
    start = re.search(r'^\s*<!-- CASE STUDY CARDS START[^\n]*\n', text, re.M)
    end = re.search(r'^\s*<!-- CASE STUDY CARDS END -->', text, re.M)
    assert start and end, "card markers not found in zoley-case-studies.v2.html"
    cards = "\n\n".join(card(cs, i) for i, cs in enumerate(CASE_STUDIES))
    open(p, "w").write(text[:start.end()] + "\n" + cards + "\n\n" + text[end.start():])


if __name__ == "__main__":
    for cs in CASE_STUDIES:
        open(os.path.join(SRC, page_file(cs)), "w").write(page(cs))
    write_cards()
    print(f"wrote {len(CASE_STUDIES)} case study pages and refreshed the index cards")
