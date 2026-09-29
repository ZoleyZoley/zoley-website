/*!
 * Zoley section loader
 * ---------------------------------------------------------------------------
 * Put ONE of these in Squarespace -> Settings -> Advanced -> Code Injection -> HEADER:
 *
 *   <script async src="https://cdn.jsdelivr.net/gh/ZoleyZoley/zoley-website@v1.7.9/dist/zoley-loader.js"></script>
 *
 * Then each page just needs Code Blocks holding one line each:
 *
 *   <div data-zoley-page="ai"></div>
 *
 * That one line renders every section of that page, in the order the repo says.
 * Adding, removing or reordering a section then happens in git alone - Squarespace
 * never needs touching again. To place a single section somewhere specific instead:
 *
 *   <div data-zoley-section="ai/01-hero"></div>
 *
 * The loader reads the pinned version out of its own <script src>, so the tag
 * above is the ONLY place a version number appears. To ship a new release:
 * push, tag, and bump the tag in that URL to the new one. Nothing else changes.
 *
 * Why a pinned tag and not @main: jsDelivr caches branch URLs for 12h at the
 * edge and 7 days in a browser that has already loaded them. Exact tags are
 * immutable and go live instantly.
 *
 * Speed (v1.7.9): the loader no longer waits for DOMContentLoaded. On Squarespace
 * that event fires only after ~700KB of Squarespace's own deferred scripts have
 * downloaded and run, which held the whole page's content back by seconds on phones.
 * Now it mounts each placeholder the moment the HTML parser reaches it. An empty
 * placeholder is held at one screen tall until its content arrives, so the footer
 * doesn't paint under the header and then jump (that jump was a CLS of ~0.65).
 */
(function () {
  "use strict";

  var ATTR = "data-zoley-section";
  var PAGE = "data-zoley-page";
  var DONE = "data-zoley-loaded";
  var PENDING = "[" + PAGE + "]:not([" + DONE + "]),[" + ATTR + "]:not([" + DONE + "])";

  // Work out where to fetch sections from, based on this script's own URL.
  var self = document.currentScript || (function () {
    var s = document.getElementsByTagName("script");
    for (var i = s.length - 1; i >= 0; i--) {
      if (s[i].src && s[i].src.indexOf("zoley-loader") !== -1) return s[i];
    }
    return null;
  })();

  var BASE = (function () {
    if (self && self.getAttribute("data-base")) return self.getAttribute("data-base").replace(/\/$/, "");
    if (self && self.src) return self.src.replace(/\/dist\/zoley-loader(\.min)?\.js.*$/, "");
    return "";
  })();

  var cache = Object.create(null);
  var manifest = null;

  // sections.v2/manifest.json lists every page, its sections in order, and its
  // one-file bundle.
  function getManifest() {
    if (!manifest) {
      manifest = fetch(BASE + "/sections.v2/manifest.json", { credentials: "omit" })
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status + " for manifest.json");
          return r.json();
        });
    }
    return manifest;
  }

  function fetchFile(path) {
    if (!cache[path]) {
      cache[path] = fetch(BASE + "/sections.v2/" + path, { credentials: "omit" })
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status + " for " + path);
          return r.text();
        });
      cache[path].catch(function () { delete cache[path]; });   // allow a retry
    }
    return cache[path];
  }

  function fetchSection(key) { return fetchFile(key + ".html"); }

  // A page's whole content as one file when the build made one (it always does
  // from v1.7.9), else its sections one by one.
  function fetchPage(m, page) {
    var entry = m[page];
    if (!entry) return Promise.reject(new Error("no page '" + page + "' in manifest.json"));
    if (entry.bundle) return fetchFile(entry.bundle).then(function (html) { return [html]; });
    return Promise.all(entry.sections.map(function (s) { return fetchSection(s.key); }));
  }

  // innerHTML never runs <script>. Re-create each one so it executes in order.
  function runScripts(container) {
    var scripts = container.querySelectorAll("script");
    for (var i = 0; i < scripts.length; i++) {
      var old = scripts[i];
      var fresh = document.createElement("script");
      for (var a = 0; a < old.attributes.length; a++) {
        fresh.setAttribute(old.attributes[a].name, old.attributes[a].value);
      }
      fresh.text = old.textContent;
      old.parentNode.replaceChild(fresh, old);
    }
  }

  function inject(el, html, key) {
    el.innerHTML = html;
    runScripts(el);
    el.dispatchEvent(new CustomEvent("zoley:section-loaded", { bubbles: true, detail: { key: key } }));
  }

  function fail(el, what, err) {
    el.removeAttribute(DONE);              // let a later scan retry
    if (window.console) console.error("[zoley] could not load " + what + ":", err);
  }

  function mount(el) {
    var key = el.getAttribute(ATTR);
    if (!key || el.hasAttribute(DONE)) return;
    el.setAttribute(DONE, "");
    fetchSection(key).then(function (html) {
      inject(el, html, key);
    }).catch(function (err) { fail(el, "section '" + key + "'", err); });
  }

  function mountPage(el) {
    var page = el.getAttribute(PAGE);
    if (!page || el.hasAttribute(DONE)) return;
    el.setAttribute(DONE, "");
    getManifest().then(function (m) {
      return fetchPage(m, page).then(function (parts) {
        el.innerHTML = "";
        if (m[page].bundle) {
          inject(el, parts[0], page);
        } else {
          // Older layout: each section in its own child, same DOM as listing them by hand.
          var keys = m[page].sections.map(function (s) { return s.key; });
          parts.forEach(function (html, i) {
            var slot = document.createElement("div");
            slot.setAttribute(ATTR, keys[i]);
            slot.setAttribute(DONE, "");
            el.appendChild(slot);
            inject(slot, html, keys[i]);
          });
        }
        el.dispatchEvent(new CustomEvent("zoley:page-loaded", { bubbles: true, detail: { page: page } }));
      });
    }).catch(function (err) { fail(el, "page '" + page + "'", err); });
  }

  function scan() {
    var pending = document.querySelectorAll(PENDING);
    for (var i = 0; i < pending.length; i++) {
      if (pending[i].hasAttribute(PAGE)) mountPage(pending[i]); else mount(pending[i]);
    }
  }

  // Same rule as the header snippet, for pages whose header predates it.
  var hold = document.createElement("style");
  hold.textContent = "[" + PAGE + "]:empty,[" + ATTR + "]:empty{min-height:100vh}";
  (document.head || document.documentElement).appendChild(hold);

  // Mount placeholders as the parser adds them, and later when Squarespace swaps
  // page content on internal navigation. Each batch is one cheap selector query.
  if (window.MutationObserver) {
    new MutationObserver(function (muts) {
      for (var i = 0; i < muts.length; i++) {
        if (muts[i].addedNodes.length) { scan(); return; }
      }
    }).observe(document.documentElement, { childList: true, subtree: true });
  }
  scan();
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", scan);
})();
