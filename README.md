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

1. Edit a file in `sections.v2/`.
2. `git add -A && git commit -m "..." && git push`
3. `git tag v1.0.2 && git push --tags`
4. In Squarespace → Settings → Advanced → Code Injection → Header, change `@v1.0.1` to `@v1.0.2`.

Step 4 is one character in one box. Everything else on the site updates from it.

**Rollback** is the same edit pointing at the older tag.

### Why a version tag instead of `@main`

jsDelivr caches a branch URL for 12 hours at its edge and **7 days in a browser that has
already loaded it**. A push to `main` would reach visitors unpredictably over the following
week. Exact tags are immutable, so they go live the moment you bump the number.

## One-time Squarespace setup

Header code injection (site-wide):

```html
<script src="https://cdn.jsdelivr.net/gh/ZoleyZoley/zoley-website@v1.0.1/dist/zoley-loader.js"></script>
```

Then each page gets one Code Block per section, each holding a single line:

```html
<div data-zoley-section="ai/01-hero"></div>
```

`sections.v2/README.md` lists the exact lines for every page, in order.

## Notes

- Sections are injected by JavaScript, so their text is not in the initial HTML response.
  Google renders JS and will index it, but if a page's search ranking matters a lot, paste
  that page's HTML into the Code Block directly instead — the section files are plain HTML
  and work either way.
- Every section carries its own scoped CSS, so it renders correctly on its own and can be
  reordered or reused on any page.
- To regenerate `sections.v2/` after editing a `main pages/*.v2.html` file, run the scripts
  in `tools/`. They overwrite `sections.v2/` from the full-page builds.
