# Китобхонаи Азим (Kitobkhona)

Private, link-only digital library of ~1,200 rare-book PDFs from the Telegram channel «Башанд Китобен»
(history, poetry, philosophy, languages and folklore of Tajikistan, Badakhshan and the Pamirs).
Interface in Russian (default) with a Tajik toggle. Owner: Afraz Alidodkhonov.

- Live site: https://kitobxona.vercel.app (Vercel, auto-deploys every push to `main`)
- Repo: https://github.com/Alidodkhonov/kitobxona
- Not meant to be indexed: `robots.txt`, `X-Robots-Tag: noindex` (vercel.json) and meta robots stay on.

## How it fits together

| Part | Where | Notes |
|---|---|---|
| Catalogue app | `index.html` (markup, CSS, UI script) + `core.js` (data, search, strings) | Plain static files, no build step. |
| Book data | `books.json` | 1,200 records: `id, title, author, desc, lang, cat, pages, mb, year, added, cv, fname, file`. |
| PDFs | GitHub **releases** `b1`–`b4` (300 books each) | URL `https://github.com/Alidodkhonov/kitobxona/releases/download/b{N}/{id}.pdf`. Not in the git tree. |
| Reader | `reader.html` + `vendor/pdfjs/` (PDF.js 3.11.174 legacy) | Loads `/api/pdf?t=bN&id=ID`. Modes: original / night / sepia / day; zoom; resume position. |
| PDF relay | `api/pdf.js` (Vercel Edge function) | GitHub release files have no CORS, so this forwards them with Range support. Only runs on Vercel. |
| Covers | `covers/s{sheet}-{row}.webp` + `.jpg` fallback, one strip of 10 covers each | `cv: [sheet, col, row, rows]` (`coverBg()` in core.js). Strips keep slow connections to ~27 KB per row on screen; cut from the original 10×10 sheets (in git history before `fix/slow-connection`). Books without a cover get a generated cloth cover (`PAL` in index.html). |
| Offline / app | `sw.js`, `manifest.webmanifest`, `icons/`, `favicon.svg/.ico` | Page and `books.json` are served from the saved copy first and refreshed in the background, so a change reaches a visitor on their second visit. **Bump `CACHE` in sw.js whenever shipped files change**, or visitors keep the old version. |
| Uploading new books | `.github/workflows/attach-books.yml` | Push a branch named `upload/b<N>-<anything>` whose `books/` folder holds `<id>.pdf` files; the workflow attaches them to release `b<N>` (creating it if needed) and deletes the branch. Files over 95 MB: `split -b 90m -d -a 3 x.pdf x.pdf.part` (parts `.part000`…), the workflow joins them. Then add the records to `books.json`. |
| Brand | `brand/` | Logos, favicons, fonts, animations, generators. Excluded from the deployment by `.vercelignore`. |

Categories (`cat`): pamir, history, philosophy, religion, poetry, ethno, language, prose, science, other.

## Search (core.js)

Multilingual and forgiving: `norm()` folds Tajik letters (ӣ ӯ ҳ қ ғ ҷ), `skel()` builds a phonetic Latin skeleton
(o→a, e→i, kh→h …) so Cyrillic and Latin spellings meet, `SYN` groups treat name variants as one person
(Носир Хусрав / Насир Хусрав / Nasir Khusraw), phrase regexes use `stem()` for Russian endings, and words match by
prefix on a cleaned index `_s`. Short queries are length-gated to avoid noise. Test changes with real names
("Ибн Сины", "Насира Хусрава", "zzzz" should return nothing).

## Design and brand (keep to these)

- Colours: Pamir Green `#1F4D3A` (lead), Green 700 `#2E6B4F`, Sage `#E7EFE9`, Warm White `#FAF8F3` (page),
  Tillo Gold `#C9A24A` (accent, never body text on white), Gold text `#8F6B22`, Ink `#12201A`,
  dark theme ground `#0F1A15`. Proportion ≈ 60 white / 30 green / 10 gold.
- Fonts: Cormorant Garamond 700/600 for the name, headings and book titles; Golos Text 400–600 for all UI.
  Both cover every Tajik letter.
- **Main logo = the arch**: the К monogram (spine = book, upper gold fan = pages being read, lower green fan =
  pages read) inside a pointed arch. Light mode: green arch. Dark mode and on green: warm-white arch.
  The inline SVG uses CSS variables `--lg-*` so one markup serves both themes (`.onband` forces the white arch).
- Layout chosen by the owner (keep it): green header band with the logo and name centred and a large centred
  search field; sections + book language on the left; list/cards in the middle; preview on the right.
  Phone: app shell with bottom tabs, chips row, full-screen book page with Read / Download / Save.
- Opening animation (`.intro` in index.html) mirrors `brand/animations/arch.mp4`; it runs once per visit and is
  skipped for reduced motion and deep links (`#book-ID`). The arch with leaves opening/closing (`.loop`) is the
  loading indicator, also in the reader.
- The owner removed the tagline «Электронная библиотека редких книг» from the animations and the header; don't
  add it back there.
- Full brand rules: `brand/design-system/README.md`, tokens in `brand/design-system/tokens.json`.

## Working on it

- Run locally: `python3 -m http.server 8000` in the repo root, open http://localhost:8000. The reader needs the
  Vercel `/api/pdf` relay, so test reading on the live site or with `vercel dev`.
- Check desktop (≥1100 px), tablet, and phone (390 px) widths in both light and dark mode.
- Deploy: commit and push to `main`; Vercel builds automatically.
- Regenerate brand files: `cd brand && python3 f2build.py` (needs `fonttools`, `cairosvg`, `pillow`);
  animations: `python3 animations/arch.py out_dir` then `ffmpeg -framerate 30 -i out_dir/f%04d.png -c:v libx264 -pix_fmt yuv420p arch.mp4`.

## Open items

- 123 books have no author and about 860 have no description (left empty on purpose until sourced).
- The original Telegram export and working files are on the owner's Mac in
  `~/Desktop/Bashand Kitoben/` (`_catalog_work/` holds ids.txt, batches.json, manifest.json, pages.tsv).
