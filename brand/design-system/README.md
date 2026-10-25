# Китобхонаи Азим

**Китобхонаи Азим** ("The Great Library") is a private digital library of rare books from the «Башанд Китобен» collection: history, poetry, philosophy, languages and folklore of Tajikistan, Badakhshan and the Pamirs. The brand should feel like an old reading room that has been carefully digitised: calm, learned and rooted in the mountains, never flashy.

Tagline: **Электронная библиотека редких книг** · **Китобхонаи электронии китобҳои нодир** · *Digital library of rare books*.

## The main logo: the arch

**The main logo is the arch version.** The К monogram stands inside a pointed arch (пештоқ), the doorway of old libraries and madrasas of Central Asia. The arch is the door into the library; the К inside it is the book.

The logo follows the device theme:

| Mode | Arch | Spine | Name | Tagline |
|---|---|---|---|---|
| **Light mode (default)** | Pamir Green `#1F4D3A` | warm white | Pamir Green | Gold text `#8F6B22` |
| **Dark mode** | Warm White `#FAF8F3` | Pamir Green | white | Tillo Gold `#C9A24A` |
| **On the brand green** | Warm White | Pamir Green | white | Tillo Gold |

On the website, the header logo and the favicon switch automatically with the device's light or dark setting (`prefers-color-scheme`). Use the green arch everywhere else, unless the background is dark or green.

Favicon and app icon: the arch alone, with the two-layer mark. Keep the arch's flat base and its pointed top; never crop it into a square.

### Inside the arch: the К monogram

The symbol is the letter **К** (for *Китобхона*) drawn as a book:

1. **The upright is a book's spine**, with the head- and tail-bands of a real hardcover. It stands for the book itself: wisdom and knowledge.
2. **The two arms are fans of pages.** The upper fan is gold and lifts like pages being turned: reading. The lower fan is green and settles: pages already read.
3. **Three layers in each fan** show many pages, many books: the size of the collection, the "big information" the library holds.

Colours of the mark: spine in Pamir Green, upper pages in three golds (`#C9A24A`, `#D9B862`, `#EBD49A`), lower pages in three greens (`#1F4D3A`, `#2E6B4F`, `#4F8A6B`). The pages are separated by thin lines in the background colour. On green the spine and lower pages turn white and pale sage, the gold stays. Below 32px use the two-layer favicon version.

## Logo versions

| Where | Files | Notes |
|---|---|---|
| **Main logo (arch)** | `logo-arch`, `logo-arch-dark-mode`, `logo-arch-stacked`, `logo-arch-stacked-dark-mode`, `logo-arch-on-green`, `logo-arch-tajik`, `logo-arch-latin`, `symbol-arch`, `symbol-arch-dark-mode` | `logo-arch` is the default (light mode); `-dark-mode` is for dark screens. Stacked for centred and square spaces. |
| **Badge and seal** | `badge-round`, `badge-round-gold`, `badge-round-mono`, `badge-arch`, `badge-arch-light` | Round seal with «Китобхонаи Азим · Электронная библиотека» for stamps, stickers and certificates; arch badge for avatars and covers. |
| **On the books** | `bookplate-ex-libris`, `pdf-cover-stamp`, `pdf-cover-stamp-green`, `book-spine`, `page-watermark` | Ex libris for the inside cover, a stamp for the first page of each PDF, a spine label, a 14% watermark for page corners. |
| **Website** | `header-logo`, `header-logo-dark-mode`, `favicon` (adaptive), `favicon-dark-mode`, `og-share-image` | The header logo is centred at the top of the site. The favicon is the arch: green in light mode, warm white in dark mode. |
| **Monogram (secondary)** | `logo-primary`, `logo-primary-on-green`, `logo-stacked`, `symbol`, `symbol-white` | The К without the arch, for wide strips, embossing and the round seal. Not the main logo. |
| **Mobile app** | `app-icon-ios-1024`, `app-icon-rounded`, `pwa-icon-192/512`, `pwa-maskable-512`, `android-foreground-432`, `app-icon-light`, `splash-screen` | White and gold mark on Pamir Green; maskable and Android versions keep the mark inside the safe zone. |
| **Social** | `avatar`, `cover-banner` | Avatar works in a circle crop. |
| **One colour** | `logo-green`, `logo-white-on-dark`, `logo-gold-foil`, `symbol-night`, `symbol-on-gold` | For stamps, embossing and gold-foil print. |

The complete set (SVG and PNG, 83 files) is in the `kitobxona-brand.zip` package.

**Clear space**: at least the width of the spine around the logo. **Minimum size**: horizontal logo 150px wide (35 mm in print); symbol 24px; below that the two-layer favicon.

**Don't**: use the green arch on a dark background (switch to the dark-mode version), crop the arch, swap the gold and green fans, add more than three pages per fan, outline or shadow the mark, or set the name in another typeface.

## Colour

Three colours carry the brand: **Pamir Green**, **warm white** and **Tillo Gold**. Green leads, white gives room, gold is the spark: used little, so it is noticed.

| Colour | Token | Hex (light) | Role |
|---|---|---|---|
| Pamir Green | `green-900` | `#1F4D3A` | Brand colour: logo, top bar, primary buttons |
| Green, lighter | `green-700` | `#2E6B4F` | Hover / pressed state |
| Sage | `sage-100` | `#E7EFE9` | Soft tinted fills, selected rows |
| Warm White | `paper` | `#FAF8F3` | Page background |
| White | `surface` | `#FFFFFF` | Cards and panels |
| Tillo Gold | `gold-500` | `#C9A24A` | Accent: the mountain, bookmarks, rules |
| Gold, text | `gold-700` | `#8F6B22` | Gold that must be read: labels, taglines |
| Ink | `ink` | `#12201A` | Text |

Proportion on a typical screen: about 60% white/paper, 30% green, 10% gold. The dark theme ("Шаб") swaps the paper for deep forest `#0F1A15` and lightens gold and green for text (`gold-700`, `green-300`), so the same brand reads at night.

**Contrast**: text uses `ink`, `muted` or `gold-700` on paper (all ≥ 4.5:1); white on Pamir Green is 9.1:1. `gold-500` is never used for body text on white (2.3:1). Exception: the logo's tagline is gold on green in the reversed logos (4.0:1); logos are exempt, but don't repeat that pairing for interface text.

## Typography

Two families, both free on Google Fonts and both covering every Tajik letter (ӣ ӯ ҳ қ ғ ҷ):

- **Cormorant Garamond** (700, 600): the voice of the library. A classical book serif for the name, book titles and headings. Use it large; below 18px switch to the sans.
- **Golos Text** (400–600): a clear modern sans designed for Cyrillic. Everything the reader operates: search, buttons, lists, metadata.

Hierarchy: `display` (name) → `title-1` (book title) → `title-2` (sections) → `body` → `ui` → `caption` → `eyebrow` (uppercase gold labels, letter-spaced 0.14em). In the logo the name is outlined Cormorant Garamond 700 and the tagline is Golos Text 500 spaced at 2.2.

## Shapes and imagery

- Corners are gently rounded (`radius-md` for controls, `radius-lg` for panels); chips are pills.
- Book covers are the only pictures. Show them at a 2:3 ratio with `radius-sm` and `shadow-book` so they sit on the page like real books.
- The fanned pages are the brand's motif: they may open in the opening animation or decorate empty states. The pointed arch is the frame of the main logo, and it also frames the badge and the bookplate.
- No stock photography, emoji or illustrations of people.

## Voice

The library speaks **Russian and Tajik equally**: every label exists in both, and the switch is always one tap away. The tone is that of a helpful librarian: short, plain, respectful. "Скачать PDF", not "Получить документ сейчас!". Names keep the spelling their language uses (Носири Хусрав in Tajik, Насир Хусрав in Russian), and search treats them as the same person.
