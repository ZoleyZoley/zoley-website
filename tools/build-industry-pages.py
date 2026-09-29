#!/usr/bin/env python3
"""
Render the industry pages from tools/industry_content.py.

    python3 tools/build-industry-pages.py && python3 tools/build-sections.py

Writes one "main pages/zoley-industry-<key>.v2.html" per industry. Each is a single
self-contained section: hero / stat / problems / what we build / proof / how we
work / FAQ / CTA. build-sections.py publishes each as sections.v2/ind-<key>/01-page.html.

The generated pages are overwritten on every run: edit the content file or the
template below, never the generated .v2.html files.
"""
import os, sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC = os.path.join(REPO, "main pages")
sys.path.insert(0, HERE)
from industry_content import INDUSTRIES, STEPS, SERVICE_URLS, QUICKSTART, CALENDLY  # noqa: E402

FONTS = ("https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,500;0,600;1,500"
         "&family=DM+Sans:wght@400;500;700&family=Caveat:wght@700&display=swap")


def e(s):
    return escape(s, quote=False)


def page_file(ind):
    return f"zoley-industry-{ind['key']}.v2.html"


# ---------------------------------------------------------------- illustration
# Four pinned cards in a Z, joined by a dashed thread: the patient's path through
# the practice once the systems are in. Same corkboard language as the site.
POS = [(22, 40, -3), (218, 30, 2.5), (30, 170, 2), (222, 164, -2.5)]
PINS = ["#14457a", "#6c5ce7", "#e3a72e", "#7a8b69"]


def board(ind):
    b, gid = ind["board"], f"{ind['sid']}-grad"
    cards = []
    for i, ((title, sub), (x, y, rot)) in enumerate(zip(b["cards"], POS)):
        cx, cy = x + 90, y + 50
        check = ""
        if i == 3:
            check = (f'<circle cx="{x+162}" cy="{y+86}" r="13" fill="#7a8b69" stroke="#1b2430" stroke-width="2"/>'
                     f'<path d="M{x+156} {y+86} l4 4 l7.5 -8.5" stroke="#fff9ef" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        cards.append(f'''<g transform="rotate({rot} {cx} {cy})">
            <rect x="{x}" y="{y}" width="180" height="100" rx="8" fill="#fff9ef" stroke="#1b2430" stroke-width="2.5"/>
            <circle cx="{cx}" cy="{y+2}" r="7" fill="{PINS[i]}" stroke="#1b2430" stroke-width="1.5"/>
            <text x="{x+16}" y="{y+30}" font-family="Caveat, cursive" font-size="17" font-weight="700" fill="{PINS[i]}">step {i+1}</text>
            <text x="{x+16}" y="{y+56}" font-family="Newsreader, Georgia, serif" font-size="20" font-weight="600" fill="#1b2430">{e(title)}</text>
            <text x="{x+16}" y="{y+78}" font-family="DM Sans, sans-serif" font-size="12.5" fill="#5c6b76">{e(sub)}</text>
            {check}
          </g>''')
    label = "Illustration: " + ", then ".join(f"{t} ({s})" for t, s in b["cards"])
    return f'''<svg viewBox="0 0 420 320" fill="none" role="img" aria-label="{escape(label)}">
          <defs>
            <linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14457a"/><stop offset="1" stop-color="#6c5ce7"/></linearGradient>
          </defs>
          <path d="M202 90 C 210 70, 214 70, 222 80 M300 130 C 280 170, 150 150, 120 170 M210 225 C 214 208, 220 208, 226 214" stroke="url(#{gid})" stroke-width="2.2" stroke-dasharray="6 6" fill="none" opacity="0.85"/>
          {"".join(cards)}
          <text x="210" y="304" font-family="Caveat, cursive" font-size="22" font-weight="700" fill="#1b2430" text-anchor="middle" transform="rotate(-1.5 210 304)">{e(b["note"])}</text>
        </svg>'''


# ---------------------------------------------------------------- sections
def problems(ind):
    items = "\n".join(
        f'        <div class="prob"><span class="prob-n">{i}</span><h3>{e(t)}</h3><p>{e(x)}</p></div>'
        for i, (t, x) in enumerate(ind["problems"], 1))
    return f'''  <section class="sec">
    <div class="head">
      <span class="tag">the cost nobody sees</span>
      <h2>{e(ind["problems_title"])}</h2>
      <p>{e(ind["problems_intro"])}</p>
    </div>
    <div class="probs">
{items}
    </div>
  </section>'''


def builds(ind):
    items = []
    for i, (svc, t, x) in enumerate(ind["builds"], 1):
        items.append(f'''        <div class="build">
          <div class="build-top"><span class="build-n">{i}</span><a class="chip" href="{SERVICE_URLS[svc]}">{e(svc)}</a></div>
          <h3>{e(t)}</h3>
          <p>{e(x)}</p>
        </div>''')
    return f'''  <section class="sec">
    <div class="head">
      <span class="tag">what we build</span>
      <h2>{e(ind["builds_title"])}</h2>
      <p>{e(ind["builds_intro"])}</p>
    </div>
    <div class="builds">
{chr(10).join(items)}
    </div>
    <div class="center"><a href="{QUICKSTART}" class="btn btn-ink">Find out what to build first</a></div>
  </section>'''


def proof(ind):
    p = ind["proof"]
    if p.get("numbers"):
        detail = "\n".join(f'          <li><span class="pn">{e(n)}</span><span class="pl">{e(l)}</span></li>' for n, l in p["numbers"])
        detail = f'        <ul class="proof-nums">\n{detail}\n        </ul>'
    else:
        detail = "\n".join(f'          <li>{e(x)}</li>' for x in p["points"])
        detail = f'        <ul class="proof-points">\n{detail}\n        </ul>'
    quotes = "\n".join(f'''      <figure class="quote">
        <blockquote>{e(q)}</blockquote>
        <figcaption><strong>{e(who)}</strong><span>{e(biz)}</span></figcaption>
      </figure>''' for q, who, biz in ind["quotes"])
    href, label = p["link"]
    return f'''  <section class="sec">
    <div class="proof">
      <div class="proof-glow proof-glow-a" aria-hidden="true"></div>
      <div class="proof-glow proof-glow-b" aria-hidden="true"></div>
      <div class="proof-inner">
        <span class="proof-tag">{e(p["tag"])}</span>
        <h2>{e(p["title"])}</h2>
        <p>{e(p["text"])}</p>
{detail}
        <a class="proof-link" href="https://www.zoley.io{href}">{e(label)} &rarr;</a>
      </div>
    </div>
    <div class="quotes quotes-{len(ind["quotes"])}">
{quotes}
    </div>
  </section>'''


def steps():
    items = "\n".join(f'        <div class="step"><span class="step-n">0{i}</span><h3>{e(t)}</h3><p>{e(x)}</p></div>'
                      for i, (t, x) in enumerate(STEPS, 1))
    return f'''  <section class="sec">
    <div class="head">
      <span class="tag">how we work</span>
      <h2>We diagnose before we build. Every engagement.</h2>
    </div>
    <div class="steps">
{items}
    </div>
  </section>'''


def faq(ind):
    items = "\n".join(f'''      <details class="qa">
        <summary>{e(q)}</summary>
        <p>{e(a)}</p>
      </details>''' for q, a in ind["faq"])
    return f'''  <section class="sec sec-narrow">
    <div class="head">
      <span class="tag">questions we hear</span>
      <h2>Before you get in touch.</h2>
    </div>
    <div class="faq">
{items}
    </div>
  </section>'''


# ---------------------------------------------------------------- CSS
CSS = r'''
  @import url('FONTS');

  #W {
    --paper: #faf3e7; --paper-2: #f6e4b8; --card: #fff9ef; --ink: #1b2430; --ink-soft: #5c6b76;
    --marigold: #e3a72e; --barn: #14457a; --sage: #7a8b69; --violet: #6c5ce7; --blue: #4ea1ff;
    --border: rgba(27,36,48,0.14);
    font-family: 'DM Sans', -apple-system, sans-serif; background: var(--paper); color: var(--ink);
  }
  #W * { box-sizing: border-box; margin: 0; padding: 0; }
  #W h1, #W h2, #W h3 { font-family: 'Newsreader', Georgia, serif; font-weight: 600; line-height: 1.15; letter-spacing: -0.01em; color: var(--ink); }
  #W p { color: var(--ink-soft); line-height: 1.65; }
  #W .tag { display: block; width: max-content; max-width: 100%; font-family: 'Caveat', cursive; font-size: 22px; font-weight: 700; color: var(--barn); transform: rotate(-2deg); margin: 0 0 8px; padding: 0 4px; }

  /* buttons */
  #W .cta-row { display: flex; gap: 14px; flex-wrap: wrap; }
  #W .btn { display: inline-flex; align-items: center; justify-content: center; min-height: 48px; padding: 15px 28px; border-radius: 8px; font-weight: 700; font-size: 15.5px; text-decoration: none; font-family: 'DM Sans', sans-serif; transition: transform 0.15s ease, box-shadow 0.15s ease, background-color 0.15s ease; }
  #W .btn-primary { background: var(--barn); color: #fff9ef; box-shadow: 0 4px 0 #0d2d50; }
  #W .btn-primary:hover { transform: translateY(2px); box-shadow: 0 2px 0 #0d2d50; }
  #W .btn-ghost { background: transparent; color: var(--ink); border: 2px solid var(--ink); }
  #W .btn-ghost:hover { background: var(--ink); color: var(--paper); }
  #W .btn-ink { background: transparent; color: var(--ink); border: 2px solid var(--ink); }
  #W .btn-ink:hover { background: var(--ink); color: var(--paper); }
  #W .btn-light { background: transparent; color: var(--paper); border: 2px solid var(--paper); }
  #W .btn-light:hover { background: var(--paper); color: var(--ink); }

  /* hero */
  #W .hero { padding: 104px 24px 40px; max-width: 1160px; margin: 0 auto; display: grid; grid-template-columns: 1fr 0.95fr; column-gap: 56px; align-items: start; }
  #W .hero > .tag { grid-column: 1; grid-row: 1; }
  #W .hero-copy { grid-column: 1; grid-row: 2; }
  #W .board { grid-column: 2; grid-row: 2; background: var(--paper-2); border: 1px solid var(--border); border-radius: 14px; padding: 20px; }
  #W .board svg { width: 100%; height: auto; display: block; }
  #W .hero h1 { font-size: clamp(34px, 4.3vw, 52px); line-height: 1.08; }
  #W .hero .sub { font-size: 17.5px; margin: 20px 0 28px; max-width: 540px; }
  #W .hero .note { font-size: 13px; margin-top: 12px; }

  /* stat */
  #W .stat { max-width: 1160px; margin: 0 auto; padding: 16px 24px 24px; }
  #W .stat-inner { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: 26px; align-items: center; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); padding: 26px 8px; }
  #W .stat-num { font-family: 'Newsreader', Georgia, serif; font-size: clamp(40px, 5vw, 58px); font-weight: 600; line-height: 1; color: var(--barn); white-space: nowrap; }
  #W .stat-inner p { font-size: 16.5px; max-width: 720px; }

  /* shared section frame */
  #W .sec { max-width: 1160px; margin: 0 auto; padding: 72px 24px 8px; }
  #W .sec-narrow { max-width: 860px; }
  #W .head { max-width: 680px; margin: 0 auto 36px; text-align: center; }
  #W .head .tag { margin-left: auto; margin-right: auto; }
  #W .head h2 { font-size: clamp(28px, 3.3vw, 40px); }
  #W .head p { font-size: 16.5px; margin-top: 12px; }
  #W .center { text-align: center; margin-top: 32px; }

  /* problems */
  #W .probs { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }
  #W .prob { position: relative; background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 28px 28px 26px 64px; }
  #W .prob-n { position: absolute; left: 22px; top: 22px; font-family: 'Caveat', cursive; font-size: 32px; font-weight: 700; line-height: 1; color: var(--violet); }
  #W .prob h3 { font-size: 20px; margin-bottom: 8px; }
  #W .prob p { font-size: 15.5px; }

  /* builds */
  #W .builds { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; }
  #W .build { position: relative; overflow: hidden; background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 26px 26px 24px; transition: transform 0.2s ease, box-shadow 0.2s ease; }
  #W .build::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 3px; background: linear-gradient(90deg, var(--barn), var(--violet), var(--blue)); }
  #W .build:hover { transform: translateY(-4px); box-shadow: 0 18px 32px -16px rgba(27,36,48,0.28); }
  #W .build-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
  #W .build-n { font-family: 'Newsreader', Georgia, serif; font-size: 22px; font-weight: 600; color: var(--barn); }
  #W .chip { display: inline-flex; align-items: center; min-height: 30px; padding: 4px 12px; border-radius: 999px; border: 1px solid var(--border); background: var(--paper); font-size: 12px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--barn); text-decoration: none; }
  #W .chip:hover { border-color: var(--barn); }
  #W .build h3 { font-size: 20px; margin-bottom: 8px; }
  #W .build p { font-size: 15px; }

  /* proof */
  #W .proof { position: relative; overflow: hidden; background: var(--ink); border-radius: 16px; }
  #W .proof-glow { position: absolute; border-radius: 50%; pointer-events: none; }
  #W .proof-glow-a { top: -120px; left: -80px; width: 380px; height: 380px; background: radial-gradient(circle, rgba(108,92,231,0.28), transparent 65%); }
  #W .proof-glow-b { bottom: -140px; right: -60px; width: 400px; height: 400px; background: radial-gradient(circle, rgba(78,161,255,0.2), transparent 65%); }
  #W .proof-inner { position: relative; padding: 48px 52px; }
  #W .proof-tag { display: block; font-family: 'Caveat', cursive; font-size: 24px; font-weight: 700; color: var(--marigold); margin-bottom: 8px; }
  #W .proof h2 { color: var(--paper); font-size: clamp(26px, 3vw, 36px); max-width: 760px; margin-bottom: 14px; }
  #W .proof-inner > p { color: #c7d0d6; font-size: 16.5px; max-width: 760px; }
  #W .proof-nums { list-style: none; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0; margin-top: 30px; border-top: 1px solid rgba(250,243,231,0.14); }
  #W .proof-nums li { padding: 22px 24px 4px 0; }
  #W .proof-nums li + li { padding-left: 24px; border-left: 1px solid rgba(250,243,231,0.14); }
  #W .pn { display: block; font-family: 'Newsreader', Georgia, serif; font-size: 36px; font-weight: 600; line-height: 1.05; color: #fff9ef; margin-bottom: 6px; }
  #W .pl { display: block; font-size: 14px; line-height: 1.45; color: #d4dbe0; }
  #W .proof-points { list-style: none; margin-top: 24px; display: grid; gap: 10px; }
  #W .proof-points li { position: relative; padding-left: 30px; color: #fff9ef; font-size: 16px; line-height: 1.5; }
  #W .proof-points li::before { content: ''; position: absolute; left: 0; top: 4px; width: 18px; height: 18px; border-radius: 50%; background: var(--sage) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4.5 8.2l2.3 2.3 4.7-5' stroke='%23fff9ef' stroke-width='2' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / 18px no-repeat; }
  #W .proof-link { display: inline-flex; align-items: center; min-height: 44px; margin-top: 26px; color: var(--marigold); font-weight: 700; font-size: 15.5px; text-decoration: none; }
  #W .proof-link:hover { color: #fff9ef; }
  #W .quotes { display: grid; gap: 20px; margin-top: 20px; }
  #W .quotes-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  #W .quote { position: relative; background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 30px 30px 24px 40px; box-shadow: 0 16px 34px -24px rgba(27,36,48,0.35); }
  #W .quote::before { content: ''; position: absolute; left: 14px; top: 26px; bottom: 26px; width: 4px; border-radius: 4px; background: var(--violet); }
  #W .quote blockquote { font-size: 16.5px; line-height: 1.65; color: var(--ink); margin-bottom: 18px; }
  #W .quote figcaption { border-top: 1px solid var(--border); padding-top: 14px; }
  #W .quote strong { display: block; font-size: 15px; color: var(--ink); }
  #W .quote figcaption span { display: block; font-size: 13.5px; color: var(--ink-soft); margin-top: 3px; }

  /* steps */
  #W .steps { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; position: relative; }
  #W .steps::before { content: ''; position: absolute; left: 12%; right: 12%; top: 40px; border-top: 2px dashed rgba(108,92,231,0.5); }
  #W .step { position: relative; background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 24px 22px; }
  #W .step-n { display: block; font-family: 'Caveat', cursive; font-size: 22px; font-weight: 700; color: var(--barn); margin-bottom: 6px; }
  #W .step h3 { font-size: 19px; margin-bottom: 8px; }
  #W .step p { font-size: 14.5px; }

  /* faq */
  #W .faq { border-top: 1px solid var(--border); }
  #W .qa { border-bottom: 1px solid var(--border); }
  #W .qa summary { list-style: none; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 16px; min-height: 60px; padding: 18px 4px; font-family: 'Newsreader', Georgia, serif; font-size: 20px; font-weight: 600; color: var(--ink); }
  #W .qa summary::-webkit-details-marker { display: none; }
  #W .qa summary::after { content: '+'; flex: 0 0 auto; font-family: 'DM Sans', sans-serif; font-size: 24px; font-weight: 400; color: var(--barn); transition: transform 0.2s ease; }
  #W .qa[open] summary::after { transform: rotate(45deg); }
  #W .qa summary:focus-visible { outline: 2px solid var(--barn); outline-offset: 2px; }
  #W .qa p { font-size: 16px; padding: 0 4px 22px; max-width: 720px; }

  /* CTA (same as the homepage) */
  #W .cta-sec { max-width: 1160px; margin: 0 auto; padding: 72px 24px 96px; }
  #W .sign { background: var(--ink); border-radius: 14px; padding: 60px 40px; text-align: center; position: relative; overflow: hidden; }
  #W .sign::before { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 25% 20%, rgba(108,92,231,0.25), transparent 55%), radial-gradient(circle at 80% 85%, rgba(181,72,45,0.22), transparent 55%); }
  #W .sign > * { position: relative; }
  #W .sign h2 { color: var(--paper); font-size: clamp(28px, 3.2vw, 38px); line-height: 1.1; margin-bottom: 14px; }
  #W .sign p { color: #c7d0d6; max-width: 540px; margin: 0 auto 28px; }
  #W .sign .cta-row { justify-content: center; }
  #W .sign .cta-note { font-size: 13px; color: rgba(244,237,224,0.55); margin: 16px auto 0; }

  @media (max-width: 900px) {
    #W .hero { grid-template-columns: 1fr; padding: 64px 20px 32px; }
    #W .hero > .tag, #W .hero-copy, #W .board { grid-column: 1; grid-row: auto; }
    #W .hero-copy { margin-bottom: 36px; }
    #W .stat { padding: 8px 20px 16px; }
    #W .sec { padding: 56px 20px 8px; }
    #W .builds { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    #W .steps { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    #W .steps::before { display: none; }
    #W .proof-inner { padding: 40px 32px; }
    #W .cta-sec { padding: 56px 20px 64px; }
  }
  @media (max-width: 640px) {
    #W .probs, #W .builds, #W .steps, #W .quotes-2 { grid-template-columns: 1fr; }
    #W .proof-nums { grid-template-columns: 1fr; }
    #W .proof-nums li, #W .proof-nums li + li { padding: 18px 0 14px; border-left: 0; }
    #W .proof-nums li + li { border-top: 1px solid rgba(250,243,231,0.14); }
  }
  @media (max-width: 560px) {
    #W { overflow-x: clip; }
    #W .hero { padding-top: 44px; }
    #W .cta-row { flex-direction: column; align-items: stretch; }
    /* Full-bleed illustration on phones, as on the other v2 pages. */
    #W .board { margin-left: calc(50% - 50vw); margin-right: calc(50% - 50vw); border-left: 0; border-right: 0; border-radius: 0; padding-left: 0; padding-right: 0; }
    #W .stat-inner { grid-template-columns: 1fr; gap: 10px; text-align: left; }
    #W .sec { padding: 48px 16px 8px; }
    #W .head { text-align: left; }
    #W .head .tag { margin-left: 0; }
    #W .prob { padding: 24px 20px 22px 56px; }
    #W .prob-n { left: 18px; }
    #W .proof-inner { padding: 32px 22px; }
    #W .quote { padding: 26px 22px 20px 34px; }
    #W .qa summary { font-size: 18px; }
    #W .sign { padding: 40px 22px; border-radius: 12px; }
    #W .cta-sec { padding: 48px 16px 56px; }
  }
'''


def page(ind):
    sid = ind["sid"]
    css = CSS.replace("#W", "#" + sid).replace("FONTS", FONTS).strip("\n")
    num, stat_text = ind["stat"]
    return f'''<!--
ZOLEY INDUSTRY PAGE - {ind['tag']}
GENERATED by tools/build-industry-pages.py from tools/industry_content.py. Do not edit
this file: change the content file (or the template in the script) and re-run it.

One section for the whole page. Squarespace page {ind['url']} gets one Code Block:
<div data-zoley-page="ind-{ind['key']}"></div>
-->

<style>
{css}
</style>

<div id="{sid}">
  <section class="hero">
    <span class="tag">{e(ind['tag'])}</span>
    <div class="hero-copy">
      <h1>{e(ind['title'])}</h1>
      <p class="sub">{e(ind['sub'])}</p>
      <div class="cta-row">
        <a href="{QUICKSTART}" class="btn btn-primary">Get your plan</a>
        <a href="{CALENDLY}" class="btn btn-ghost">Book an intro call</a>
      </div>
      <p class="note">A written recommendation. No obligation.</p>
    </div>
    <div class="board">
        {board(ind)}
    </div>
  </section>

  <div class="stat">
    <div class="stat-inner">
      <span class="stat-num">{e(num)}</span>
      <p>{e(stat_text)}</p>
    </div>
  </div>

{problems(ind)}

{builds(ind)}

{proof(ind)}

{steps()}

{faq(ind)}

  <section class="cta-sec">
    <div class="sign">
      <h2>{e(ind['cta_title'])}</h2>
      <p>{e(ind['cta_text'])}</p>
      <div class="cta-row">
        <a href="{QUICKSTART}" class="btn btn-primary">Get your plan</a>
        <a href="{CALENDLY}" class="btn btn-light">Book an intro call</a>
      </div>
      <p class="cta-note">Prefer email? connect@zoley.io</p>
    </div>
  </section>
</div>
'''


if __name__ == "__main__":
    for ind in INDUSTRIES:
        open(os.path.join(SRC, page_file(ind)), "w").write(page(ind))
    print(f"wrote {len(INDUSTRIES)} industry pages")
