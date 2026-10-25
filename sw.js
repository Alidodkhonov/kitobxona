/* Китобхонаи Азим: keeps the catalogue and covers available offline and fast, even on a slow connection.
   Page and data: saved copy first, refreshed in the background (bump CACHE to force everyone onto a new release).
   Covers, icons, fonts, PDF.js: cache first. Only good responses are ever saved. */
const CACHE = "kitobxona-v4";
const SHELL = ["/", "/core.js", "/books.json", "/manifest.webmanifest", "/icons/icon-192.png", "/favicon.svg"];
const LATER = ["/reader.html", "/vendor/pdfjs/pdf.min.js", "/vendor/pdfjs/pdf.worker.min.js"]; // big, fetched after the catalogue

const ok = res => res && !res.redirected && (res.ok || res.type === "opaque"); // a saved redirect breaks page loads
const save = (req, res) => { if (ok(res)) { const cp = res.clone(); caches.open(CACHE).then(c => c.put(req, cp)); } return res; };
// Each file on its own, so one failed download on a bad connection doesn't throw away the rest.
const fill = list => caches.open(CACHE).then(c => Promise.allSettled(list.map(u => fetch(u).then(res => ok(res) && c.put(u, res)))));

self.addEventListener("install", e => { e.waitUntil(fill(SHELL).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()).then(() => { fill(LATER); }));
});
self.addEventListener("fetch", e => {
  const r = e.request; if (r.method !== "GET") return;
  const u = new URL(r.url);
  if (u.origin === location.origin && u.pathname.startsWith("/api/")) return; // book pages stream straight through
  if (u.hostname === "github.com" || u.hostname.endsWith("githubusercontent.com")) return; // book downloads go straight to GitHub
  const cacheFirst = u.pathname.startsWith("/covers/") || u.pathname.startsWith("/icons/") || u.pathname.startsWith("/vendor/") || u.hostname.includes("fonts.g");
  if (cacheFirst) {
    e.respondWith(caches.match(r).then(hit => hit || fetch(r).then(res => save(r, res))));
  } else if (u.origin === location.origin) {
    const nav = r.mode === "navigate";
    const key = nav ? (u.pathname === "/index.html" ? "/" : u.pathname) : r; // pages saved once, without ?query
    const net = fetch(r).then(res => save(key, res));
    e.waitUntil(net.catch(() => {})); // let the background refresh finish after the saved copy is shown
    e.respondWith(caches.match(key, { ignoreSearch: nav }).then(hit => {
      if (hit) return hit;
      return net.catch(() => nav ? caches.match("/") : Response.error());
    }));
  }
});
