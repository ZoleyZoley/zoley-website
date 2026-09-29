# Zoley website

Front-end HTML for zoley.io. Squarespace renders the site; this repo holds the markup,
and sections are pulled into Squarespace from jsDelivr so nothing is copy-pasted twice.

## Layout

| Path | What it is |
|---|---|
| `sections.v2/` | **What the live site uses.** One self-contained HTML file per page section. |
| `main pages/*.v2.html` | Full-page reference builds. `sections.v2/` is generated from these. |
| `main pages/*.html` | The original (pre-v2) pages. Kept for reference; nothing points at them. |
| `sections/` | Original (pre-v2) sections. Kept for reference. |
| `dist/zoley-loader.js` | The script Squarespace loads. Fetches sections and injects them. |
| `tools/` | The scripts that generated `sections.v2/` from `main pages/`. |
| `Secondary Pages/`, `blogs/`, `case studies/` | Standalone pages, still pasted by hand. |

Nothing in this repo was deleted or rewritten to build v2 — the originals are all intact.

## How a change reaches the live site

1. Edit the page in `main pages/` (the `.v2.html` file), then run `python3 tools/build-sections.py`.
   Never hand-edit `sections.v2/`: the build overwrites it.
2. `git add -A && git commit -m "..." && git push`
3. `git tag v1.7.10 && git push --tags` (the next unused tag; the live one is v1.7.9)
4. In Squarespace → Settings → Advanced → Code Injection → Header, change `@v1.7.9` to `@v1.7.10`.

**Never reuse a tag name**, even one you deleted. jsDelivr remembers which commit a
tag pointed to the first time it was requested and keeps serving those files. (v1.7.3
was lost this way on 9/28/26: it serves an older commit, so v1.7.4 replaced it.)

Step 4 is one character in one box. Everything else on the site updates from it.

**Rollback** is the same edit pointing at the older tag.

### The homepage hero is pasted, not loaded

The homepage hero lives directly in its Squarespace Code Block, so it paints with the
page instead of after the loader (on a throttled phone: hero at 2.8s instead of 4.8s).
A tag bump does **not** update it. After changing the hero in
`main pages/zoley-homepage.v2.html`, run the build and re-paste
`sections.v2/_inline/homepage-01-hero.html` into that Code Block. `INLINE` in
`tools/build-sections.py` lists every section handled this way.

### Why a version tag instead of `@main`

jsDelivr caches a branch URL for 12 hours at its edge and **7 days in a browser that has
already loaded it**. A push to `main` would reach visitors unpredictably over the following
week. Exact tags are immutable, so they go live the moment you bump the number.

## One-time Squarespace setup

Header code injection (site-wide). This is the whole box - replace everything in it:

```html
<style>[data-zoley-page]:empty,[data-zoley-section]:empty{min-height:100vh}</style>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,500;0,600;1,500&family=DM+Sans:wght@400;500;700&family=Caveat:wght@700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,500;0,600;1,500&family=DM+Sans:wght@400;500;700&family=Caveat:wght@700&display=swap"></noscript>
<script async src="https://cdn.jsdelivr.net/gh/ZoleyZoley/zoley-website@v1.7.9/dist/zoley-loader.js"></script>
```

Why each line is there (v1.7.9, 9/29/26 speed pass):
- The `<style>` holds each empty placeholder at one screen tall until its content arrives,
  so Squarespace's footer never paints under the header and then jumps (CLS was up to 0.65).
- The fonts load without blocking the first paint, and the loader is `async`, so neither
  holds up the page. The font URL must match the `@import` in every section exactly, or
  the browser downloads the fonts twice.

Then each page gets **one** Code Block holding a single line:

```html
<div data-zoley-page="ai"></div>
```

That renders every section of that page, in the order `sections.v2/manifest.json` gives.
Adding, removing or reordering a section is then a git change alone - Squarespace never
needs touching again.

To place a single section somewhere specific, use its own key instead:

```html
<div data-zoley-section="ai/01-hero"></div>
```

`sections.v2/README.md` lists the page names and every section key.

## Notes

- Sections are injected by JavaScript, so their text is not in the initial HTML response.
  Google renders JS and will index it, but if a page's search ranking matters a lot, paste
  that page's HTML into the Code Block directly instead — the section files are plain HTML
  and work either way.
- Every section carries its own scoped CSS, so it renders correctly on its own and can be
  reordered or reused on any page.
- To regenerate `sections.v2/` after editing a `main pages/*.v2.html` file, run the scripts
  in `tools/`. They overwrite `sections.v2/` from the full-page builds.
