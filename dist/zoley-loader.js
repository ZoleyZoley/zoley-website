/*!
 * Zoley section loader
 * ---------------------------------------------------------------------------
 * Put ONE of these in Squarespace -> Settings -> Advanced -> Code Injection -> HEADER:
 *
 *   <script src="https://cdn.jsdelivr.net/gh/ZoleyZoley/zoley-website@v1.0.5/dist/zoley-loader.js"></script>
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
 * push, tag, and bump @v1.0.0 to the new tag. Nothing else changes.
 *
 * Why a pinned tag and not @main: jsDelivr caches branch URLs for 12h at the
 * edge and 7 days in a browser that has already loaded them. Exact tags are
 * immutable and go live instantly.
 */
(function () {
  "use strict";

  var ATTR = "data-zoley-section";
  var PAGE = "data-zoley-page";
  var DONE = "data-zoley-loaded";

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

  // sections.v2/manifest.json lists every page and its sections in order. It is
  // what lets one data-zoley-page line stand in for the whole page.
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

  function fetchSection(key) {
    if (!cache[key]) {
      cache[key] = fetch(BASE + "/sections.v2/" + key + ".html", { credentials: "omit" })
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status + " for " + key);
          return r.text();
        });
    }
    return cache[key];
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

  // One line renders the whole page: each section gets its own child element, so
  // the result is the same DOM as listing them by hand.
  function mountPage(el) {
    var page = el.getAttribute(PAGE);
    if (!page || el.hasAttribute(DONE)) return;
    el.setAttribute(DONE, "");
    getManifest().then(function (m) {
      var entry = m[page];
      if (!entry) throw new Error("no page '" + page + "' in manifest.json");
      var keys = entry.sections.map(function (s) { return s.key; });
      return Promise.all(keys.map(fetchSection)).then(function (parts) {
        el.innerHTML = "";
        parts.forEach(function (html, i) {
          var slot = document.createElement("div");
          slot.setAttribute(ATTR, keys[i]);
          slot.setAttribute(DONE, "");
          el.appendChild(slot);
          inject(slot, html, keys[i]);
        });
        el.dispatchEvent(new CustomEvent("zoley:page-loaded", { bubbles: true, detail: { page: page, count: keys.length } }));
      });
    }).catch(function (err) { fail(el, "page '" + page + "'", err); });
  }

  function scan(root) {
    root = root || document;
    var pages = root.querySelectorAll("[" + PAGE + "]:not([" + DONE + "])");
    for (var p = 0; p < pages.length; p++) mountPage(pages[p]);
    var nodes = root.querySelectorAll("[" + ATTR + "]:not([" + DONE + "])");
    for (var i = 0; i < nodes.length; i++) mount(nodes[i]);
  }

  function start() {
    scan(document);
    // Squarespace swaps page content on internal navigation; pick up new blocks.
    if (window.MutationObserver) {
      new MutationObserver(function (muts) {
        for (var i = 0; i < muts.length; i++) {
          if (muts[i].addedNodes.length) { scan(document); return; }
        }
      }).observe(document.body, { childList: true, subtree: true });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
