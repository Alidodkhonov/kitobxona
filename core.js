/* Shared catalogue logic for all design options */
window.LIB = (function () {
  const T = {
    ru: {
      name: "Китобхонаи Азим", tag: "Электронная библиотека редких книг",
      books: n => `${n} ${pl(n, ["книга", "книги", "книг"])}`,
      search: "Название, автор или тема…", all: "Все", allLangs: "Все языки",
      sNew: "Новые поступления", sTitle: "По названию", sAuthor: "По автору",
      more: "Показать ещё", seeAll: "Смотреть все", back: "Назад",
      read: "Открыть PDF", dl: "Скачать", soon: "Ссылка на файл появится после загрузки книг.",
      author: "Автор", year: "Год", pages: "Страниц", size: "Размер", mb: "МБ", lang: "Язык", cat: "Раздел",
      emptyT: "Ничего не найдено", emptyD: "Попробуйте другое слово или сбросьте фильтры.", reset: "Сбросить",
      results: n => `Найдено: ${n}`, unknown: "Автор не указан", sections: "Разделы", featured: "Избранное собрание",
      cats: { pamir: "Памир и Бадахшан", history: "История", philosophy: "Философия", religion: "Религия", poetry: "Поэзия", ethno: "Этнография и фольклор", language: "Языкознание", prose: "Проза", science: "Наука и общество", other: "Разное" },
      langs: { ru: "Русский", tg: "Таджикский", fa: "Персидский", en: "Английский", other: "Другой" }
    },
    tg: {
      name: "Китобхонаи Азим", tag: "Китобхонаи электронии китобҳои нодир",
      books: n => `${n} китоб`,
      search: "Ном, муаллиф ё мавзӯъ…", all: "Ҳама", allLangs: "Ҳама забонҳо",
      sNew: "Иловаҳои нав", sTitle: "Аз рӯи ном", sAuthor: "Аз рӯи муаллиф",
      more: "Боз нишон диҳед", seeAll: "Ҳамаашро дидан", back: "Бозгашт",
      read: "Кушодани PDF", dl: "Боргирӣ", soon: "Пайванди файл пас аз боргузории китобҳо пайдо мешавад.",
      author: "Муаллиф", year: "Сол", pages: "Саҳифа", size: "Ҳаҷм", mb: "МБ", lang: "Забон", cat: "Бахш",
      emptyT: "Ҳеҷ чиз ёфт нашуд", emptyD: "Калимаи дигарро санҷед ё филтрҳоро бекор кунед.", reset: "Бекор кардан",
      results: n => `Ёфт шуд: ${n}`, unknown: "Муаллиф нишон дода нашудааст", sections: "Бахшҳо", featured: "Маҷмӯаи интихобӣ",
      cats: { pamir: "Помир ва Бадахшон", history: "Таърих", philosophy: "Фалсафа", religion: "Дин", poetry: "Назм", ethno: "Мардумшиносӣ ва фолклор", language: "Забоншиносӣ", prose: "Наср", science: "Илм ва ҷомеа", other: "Гуногун" },
      langs: { ru: "Русӣ", tg: "Тоҷикӣ", fa: "Форсӣ", en: "Англисӣ", other: "Дигар" }
    }
  };
  function pl(n, f) { const a = n % 10, b = n % 100; return a == 1 && b != 11 ? f[0] : a >= 2 && a <= 4 && (b < 10 || b >= 20) ? f[1] : f[2]; }
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
  };
  const norm = s => (s || "").toLowerCase().replace(/ё/g, "е").replace(/ӣ/g, "и").replace(/ӯ/g, "у").replace(/ҳ/g, "х").replace(/қ/g, "к").replace(/ғ/g, "г").replace(/ҷ/g, "ч");
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const hash = s => { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) | 0; return Math.abs(h); };
  const S = { lang: store.get("lang", "ru"), q: "", cat: "", bl: "", sort: "new" };
  let BOOKS = [];
  const L = () => T[S.lang];

  function load(cb) {
    fetch("books.json").then(r => r.json()).then(d => {
      BOOKS = d.map(b => ({ ...b, _s: norm([b.title, b.author, b.desc, b.year, b.fname].join(" ")) }));
      cb();
    }).catch(() => cb());
  }
  function matches(b, o = {}) {
    if (!o.skipCat && S.cat && b.cat !== S.cat) return false;
    if (S.bl && b.lang !== S.bl) return false;
    const q = norm(S.q).trim().split(/\s+/).filter(Boolean);
    return q.every(w => b._s.includes(w));
  }
  function list(o) {
    const loc = S.lang, out = BOOKS.filter(b => matches(b, o));
    const cmp = { title: (a, b) => a.title.localeCompare(b.title, loc), author: (a, b) => (a.author || "яяя").localeCompare(b.author || "яяя", loc), new: (a, b) => b.added - a.added };
    return out.sort(cmp[S.sort] || cmp.new);
  }
  function counts(o) { const c = {}; BOOKS.filter(b => matches(b, o)).forEach(b => c[b.cat] = (c[b.cat] || 0) + 1); return c; }
  function langsPresent() { return [...new Set(BOOKS.map(b => b.lang))]; }

  /* covers: real Telegram cover from sprite sheet, else a generated cloth cover */
  function cover(b, palette) {
    if (b.cv) {
      const [s, c, r, rows] = b.cv;
      return `<div class="cover img" role="img" aria-label="${esc(b.title)}" style="background-image:url(covers/c${s}.jpg);background-size:1000% ${rows * 100}%;background-position:${c / 9 * 100}% ${rows > 1 ? r / (rows - 1) * 100 : 0}%"></div>`;
    }
    const col = palette[hash(b.title + b.author) % palette.length];
    return `<div class="cover gen" style="--c:${col}"><span class="ca">${esc(b.author)}</span><span class="ct">${esc(b.title)}</span></div>`;
  }
  const fid = f => (f.match(/\/d\/([\w-]+)/) || f.match(/[?&]id=([\w-]+)/) || [])[1];
  const links = b => b.file && /github\.com|githubusercontent/.test(b.file) ? { view: b.file, dl: b.file } : b.file ? { view: fid(b.file) ? `https://drive.google.com/file/d/${fid(b.file)}/view` : b.file, dl: fid(b.file) ? `https://drive.google.com/uc?export=download&id=${fid(b.file)}` : b.file } : null;
  function meta(b) {
    const l = L(), m = [];
    if (b.year) m.push([l.year, b.year]);
    m.push([l.lang, l.langs[b.lang] || "—"]);
    if (b.pages) m.push([l.pages, b.pages]);
    if (b.mb) m.push([l.size, `${b.mb} ${l.mb}`]);
    return m;
  }
  function setLang(x) { S.lang = x; store.set("lang", x); document.documentElement.lang = x; }
  document.documentElement.lang = S.lang;
  return { T, S, L, load, list, counts, langsPresent, cover, links, meta, setLang, esc, get books() { return BOOKS; } };
})();
