/* Китобхонаи Азим: keeps the catalogue and covers available offline and fast.
   Network first for the page and data (always fresh when online), cache first for covers and fonts. */
const CACHE = "kitobxona-v3";
const SHELL = ["/", "/core.js", "/books.json", "/reader.html", "/vendor/pdfjs/pdf.min.js", "/vendor/pdfjs/pdf.worker.min.js", "/manifest.webmanifest", "/icons/icon-192.png", "/favicon.svg"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const r = e.request; if (r.method !== "GET") return;
  const u = new URL(r.url);
  if (u.origin === location.origin && u.pathname.startsWith("/api/")) return; // book pages stream straight through
  if (u.hostname === "github.com" || u.hostname.endsWith("githubusercontent.com")) return; // book downloads go straight to GitHub
  const cacheFirst = u.pathname.startsWith("/covers/") || u.pathname.startsWith("/icons/") || u.pathname.startsWith("/vendor/") || u.hostname.includes("fonts.g");
  if (cacheFirst) {
    e.respondWith(caches.match(r).then(hit => hit || fetch(r).then(res => { const cp = res.clone(); caches.open(CACHE).then(c => c.put(r, cp)); return res; })));
  } else if (u.origin === location.origin) {
    e.respondWith(fetch(r).then(res => { const cp = res.clone(); caches.open(CACHE).then(c => c.put(r, cp)); return res; }).catch(() => caches.match(r).then(h => h || caches.match("/"))));
  }
});
