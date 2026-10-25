/* Shared catalogue logic for all design options */
window.LIB = (function () {
  const T = {
    ru: {
      name: "Китобхонаи Азим", tag: "Электронная библиотека редких книг",
      books: n => `${n} ${pl(n, ["книга", "книги", "книг"])}`,
      search: "Название, автор или тема…", all: "Все", allLangs: "Все языки",
      sNew: "Новые поступления", sTitle: "По названию", sAuthor: "По автору",
      more: "Показать ещё", seeAll: "Смотреть все", back: "Назад",
      read: "Открыть PDF", dl: "Скачать", dlPdf: "Скачать PDF", soon: "Ссылка на файл появится после загрузки книг.",
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
      read: "Кушодани PDF", dl: "Боргирӣ", dlPdf: "Боргирии PDF", soon: "Пайванди файл пас аз боргузории китобҳо пайдо мешавад.",
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
  /* phonetic skeleton: makes Russian, Tajik and Latin spellings of the same word meet */
  const TR = { а:"a",б:"b",в:"v",г:"g",д:"d",е:"e",ж:"zh",з:"z",и:"i",й:"i",к:"k",л:"l",м:"m",н:"n",о:"o",п:"p",р:"r",с:"s",т:"t",у:"u",ф:"f",х:"h",ц:"ts",ч:"ch",ш:"sh",щ:"sh",ъ:"",ы:"i",ь:"",э:"e",ю:"yu",я:"ya","ʼ":"","’":"","'":"" };
  const skel = s => norm(s).replace(/[а-яъь'’ʼ]/g, c => TR[c] ?? c)
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/dzh|dj/g, "j").replace(/kh/g, "h").replace(/gh/g, "g").replace(/q/g, "k").replace(/w/g, "v")
    .replace(/[yj](?=[aeiou])/g, m => m === "j" ? "j" : "")
    .replace(/o/g, "a").replace(/e/g, "i").replace(/y/g, "i").replace(/v/g, "u")
    .replace(/([a-z])\1+/g, "$1").replace(/[^a-z0-9؀-ۿ ]+/g, " ");
  /* names and words that are spelled very differently across languages */
  const SYN = [
    "фирдавси|фирдоуси|фирдавсӣ|ferdowsi|firdausi|firdawsi|فردوسی","шахнаме|шахнама|шоҳнома|shahnameh|shahnama|shohnoma|شاهنامه",
    "хайям|хайём|khayyam|khayyām|خیام","руми|румӣ|rumi|mevlana|mawlana|мавлоно|мевляна|مولانا","носири хусрав|насир хусрав|насир хосров|насир-и хусрав|nasir khusraw|nasir khusrau|nasir-i khusraw|ناصر خسرو",
    "ибн сина|ибни сино|авиценна|avicenna|ibn sina|ابن سینا","рудаки|рӯдакӣ|rudaki|رودکی","хафиз|ҳофиз|hafez|hafiz|حافظ","саади|саъдӣ|сади|saadi|sadi|سعدی",
    "аттар|аттор|attar|عطار","джами|ҷомӣ|jami|جامی","бедил|bedil|بیدل","низами|низомӣ|nizami|نظامی","навои|навоӣ|navoi|navai","айни|айнӣ|aini|ayni",
    "бадахшан|бадахшон|badakhshan|бадахшанский|бадахшӣ","памир|помир|pamir|памирский|помирӣ","исмаилит|исмоилия|исмаили|ismaili|ismaʿili","ага хан|ога хон|aga khan|agha khan",
    "авеста|авесто|авасто|avesta","зардушт|заратустра|зороастр|zoroaster|zarathustra","навруз|наврӯз|новруз|nowruz|navruz|نوروز",
    "таджик|тоҷик|tajik|تاجیک","шугнан|шуғнон|shughni|shugnan","вахан|вахон|wakhan|wakhi","рушан|рӯшон|rushan","бухара|бухоро|bukhara","самарканд|самарқанд|samarkand|samarqand",
    "согд|суғд|sogd|sogdian","история|таърих|history|tarikh|تاریخ","язык|забон|language","словарь|луғат|фарҳанг|dictionary|lughat","сказки|афсона|афсонаҳо|tales|fairy",
    "поэзия|стихи|шеър|назм|ашъор|poetry|poems","философия|фалсафа|philosophy","религия|дин|religion","суфизм|тасаввуф|суфи|sufism|sufi","коран|қуръон|quran|koran|قرآن",
    "этнография|мардумшиносӣ|ethnography","археология|бостоншиносӣ|archaeology","архитектура|меъморӣ|architecture"
  ].map(g => g.split("|"));
  const SYNSK = SYN.map(g => g.map(skel).map(x => x.trim()).filter(Boolean));
  const clean = s => " " + s.replace(/[^\p{L}\p{N}]+/gu, " ").replace(/\s+/g, " ").trim() + " ";
  const SYNW = SYN.map(g => g.filter(x => !/\s/.test(x.trim())).map(norm));
  const SYNWK = SYNW.map(ws => ws.map(w => skel(w).trim()));
  function variants(w) {
    const n = norm(w).replace(/[^\p{L}\p{N}]/gu, ""), k = skel(w).replace(/\s/g, "");
    const out = new Set([n]), groups = [];
    if (k.length >= Math.min(3, n.length)) out.add(k);
    if (n.length >= 3) SYN.forEach((g, i) => {
      const hit = SYNW[i].some(x => x.length >= 3 && (x.startsWith(n) || (n.length >= 4 && n.startsWith(x)))) || (k.length >= 3 && SYNWK[i].some(y => y.length >= 3 && (y.startsWith(k) || (k.length >= 4 && k.startsWith(y)))));
      if (hit) { SYNW[i].forEach(x => x.length >= 3 && out.add(x)); SYNWK[i].forEach(y => y.length >= 3 && out.add(y)); groups.push(i); }
    });
    return { v: [...out].filter(Boolean), g: groups };
  }
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const hash = s => { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) | 0; return Math.abs(h); };
  const S = { lang: store.get("lang", "ru"), q: "", cat: "", bl: "", sort: "new" };
  let BOOKS = [];
  const L = () => T[S.lang];

  function load(cb) {
    fetch("books.json").then(r => r.json()).then(d => {
      BOOKS = d.map(b => { const txt = [b.title, b.author, b.desc, b.year, T.ru.cats[b.cat], T.tg.cats[b.cat], T.ru.langs[b.lang], T.tg.langs[b.lang]].join(" "); return { ...b, _s: clean(norm(txt)) + clean(skel(txt)) }; });
      cb();
    }).catch(() => cb());
  }
  function matches(b, o = {}) {
    if (!o.skipCat && S.cat && b.cat !== S.cat) return false;
    if (S.bl && b.lang !== S.bl) return false;
    return qv.every(c => (c.v && c.v.some(v => b._s.includes(" " + v))) || (c.rx && c.rx.some(r => r.test(b._s))));
  }
  let qv = [], qlast = null;
  const esc2 = x => x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const stem = w => w.length >= 4 ? w.replace(/[аеиоуыяэюёaeiou]$/u, "") : w;
  const phraseRx = p => new RegExp(" " + p.trim().split(/\s+/).map(w => esc2(stem(w))).join("\\S* ") + "\\S*");
  const PHR = SYN.map(g => g.filter(x => /\s/.test(x.trim())));
  function prepQuery() {
    if (S.q === qlast) return; qlast = S.q; qv = [];
    let qn = " " + norm(S.q).replace(/[^\p{L}\p{N}]+/gu, " ") + " ", qk = " " + skel(S.q).replace(/\s+/g, " ") + " ";
    SYN.forEach((g, i) => PHR[i].forEach(p => {
      const pn = norm(p), pk = skel(p).trim();
      const rn = phraseRx(pn), rk = phraseRx(pk);
      if (rn.test(qn) || rk.test(qk)) {
        const rxs = g.flatMap(x => [phraseRx(norm(x)), phraseRx(skel(x).trim())]);
        qv.push({ rx: rxs });
        qn = qn.replace(rn, " "); qk = qk.replace(rk, " ");
        pn.split(/\s+/).forEach(w => { qn = qn.replace(new RegExp(" " + esc2(w) + "\\S*"), " "); });
      }
    }));
    qn.trim().split(/\s+/).filter(Boolean).forEach(w => { const r = variants(w); qv.push({ v: r.v, rx: r.g.flatMap(i => PHR[i].flatMap(p => [phraseRx(norm(p)), phraseRx(skel(p).trim())])) }); });
  }
  function list(o) {
    prepQuery();
    const loc = S.lang, out = BOOKS.filter(b => matches(b, o));
    const cmp = { title: (a, b) => a.title.localeCompare(b.title, loc), author: (a, b) => (a.author || "яяя").localeCompare(b.author || "яяя", loc), new: (a, b) => b.added - a.added };
    return out.sort(cmp[S.sort] || cmp.new);
  }
  function counts(o) { prepQuery(); const c = {}; BOOKS.filter(b => matches(b, o)).forEach(b => c[b.cat] = (c[b.cat] || 0) + 1); return c; }
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
  const links = b => b.file && /github\.com/.test(b.file) ? { view: b.file, dl: b.file, only: true } : b.file ? { view: fid(b.file) ? `https://drive.google.com/file/d/${fid(b.file)}/view` : b.file, dl: fid(b.file) ? `https://drive.google.com/uc?export=download&id=${fid(b.file)}` : b.file } : null;
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
