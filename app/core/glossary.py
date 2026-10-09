"""Terimler sözlüğü (`content/glossary.json`).

Sıfırdan öğrenen biri dersin ortasında "parametre neydi?" diye takılınca
bölümü bırakıp aramaya gidiyordu. Şimdi terim derste ilk geçtiği yerde
noktalı altı çizgiyle işaretli; üzerine gelince kısa açıklaması çıkıyor.
Bütün terimler Hakkında › Sözlük sekmesinde ve `Ctrl+K` aramasında.

**Terim yalnızca kendi patikasının derslerinde işaretleniyor** (`group` →
`GROUP_CHAPTERS`, artı `also`): "fonksiyon" Python'da `def`, matematikte
f(x); "dizin" SQL'de index, matematikte başka bir şey. Aynı kelimenin iki
anlamı iki ayrı terim olarak yazılıyor, kapsamları çakışmıyor.

İşaretleme sayfanın içinde, betikle yapılıyor (`page_script`): metin
düğümleri dolaşılıyor, kod, başlık, bağlantı, formül ve figür atlanıyor,
her terim sayfada **bir kez** (ilk geçtiği yerde) işaretleniyor. Açıklama
kartı tamamen sayfa içi (CSS + birkaç satır betik); uygulamaya haber
gitmiyor.
"""

from __future__ import annotations

import html
import json
import re
from functools import lru_cache

from ..paths import content_dir

GROUPS = ("python", "data", "ml", "sql", "math", "ts", "api", "docker", "git", "bigdata", "algorithm")

GROUP_CHAPTERS = {
    "python": ("00-python-temelleri",),
    "data": ("01-veri-bilimi",),
    "ml": ("02-makine-ogrenmesi",),
    "sql": ("03-sql",),
    "math": ("04-temel-matematik", "05-ileri-matematik"),
    "ts": ("06-zaman-serileri",),
    "api": ("07-api-kullanmak", "08-api-yazmak"),
    "docker": ("09-docker",),
    "git": ("10-git",),
    "bigdata": ("11-buyuk-veri",),
    "algorithm": ("12-temel-algoritmalar", "13-algoritma-teknikleri", "14-ml-algoritmalari"),
}

_CODE = re.compile(r"`([^`]+)`")


@lru_cache(maxsize=1)
def load() -> tuple[dict, ...]:
    """Sözlükteki terimler (dosyadaki sırayla)."""
    yol = content_dir() / "glossary.json"
    if not yol.exists():
        return ()
    with yol.open(encoding="utf-8") as dosya:
        return tuple(json.load(dosya).get("terms", []))


def chapters_of(term: dict) -> set[str]:
    return set(GROUP_CHAPTERS.get(term.get("group", ""), ())) | set(term.get("also", []))


def text_html(text: str) -> str:
    """Açıklama metni: HTML kaçışlı, `kod` parçaları <code>."""
    return _CODE.sub(r"<code>\1</code>", html.escape(text, quote=False))


def anchor(term_id: str) -> str:
    return f"term-{term_id}"


def page_terms(chapter: str, language: str) -> list[dict]:
    """O patikanın derslerinde işaretlenecek terimler (betiğe giden veri)."""
    sonuc = []
    for term in load():
        eslesme = list(term.get("match", {}).get(language, []))
        if not eslesme or chapter not in chapters_of(term):
            continue
        if language == "tr":
            # Büyük/küçük harf duyarsız eşleşme Türkçe İ'yi i saymıyor
            # (cümle başındaki "İndeks"); büyük hâli ayrıca aranıyor.
            eslesme += ["İ" + s[1:] for s in eslesme if s.startswith("i")]
        sonuc.append({
            "id": term["id"],
            "m": eslesme,
            "t": term["title"].get(language, ""),
            "d": text_html(term["text"].get(language, "")),
        })
    return sonuc


def chapter_from_path(path) -> str:
    """İçerik klasörünün altındaki bir yoldan patika klasörünün adı."""
    if path is None:
        return ""
    try:
        parcalar = path.resolve().relative_to(content_dir().resolve()).parts
    except (ValueError, OSError):
        return ""
    return parcalar[0] if parcalar else ""


# Sayfa betiği. Metin düğümleri dolaşılıyor; her terimin ilk geçtiği yer
# <span class="term"> ile sarılıyor, içine açıklama kartı konuyor. Kart
# sağ kenardan taşacaksa sola açılıyor (`flip`), alttan taşacaksa yukarı
# (`up`). Eşleşme kelime başında; kelimenin geri kalanı (Türkçe ekler)
# da altı çizili kısma giriyor.
_SCRIPT = """<script>
(function () {
  var TERMS = %s;
  if (!TERMS.length) return;
  var SKIP = /^(PRE|CODE|A|H[1-6]|FIGURE|SVG|BUTTON|SCRIPT|STYLE|TEXTAREA|KBD)$/i;
  var root = document.querySelector('.content') || document.body;
  function skip(el) {
    for (; el && el !== root; el = el.parentElement) {
      if (SKIP.test(el.tagName)) return true;
      var c = el.classList;
      if (c && (c.contains('math') || c.contains('katex') || c.contains('term') ||
                c.contains('banner') || c.contains('meta') || c.contains('foot') ||
                c.contains('hintbox') || c.contains('cmp') || c.contains('chips'))) return true;
    }
    return false;
  }
  var L = '[\\\\p{L}\\\\p{N}_]';
  TERMS.forEach(function (t) {
    t.re = new RegExp('(^|[^\\\\p{L}\\\\p{N}_])((?:' + t.m.map(function (s) {
      return s.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
    }).join('|') + ')' + L + '*)', 'iu');
  });
  var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
  var nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  var left = TERMS.slice();
  nodes.forEach(function (node) {
    if (!left.length || !node.nodeValue.trim() || skip(node.parentElement)) return;
    var best = null;
    left.forEach(function (t) {
      var m = t.re.exec(node.nodeValue);
      if (m && (!best || m.index + m[1].length < best.at)) best = {t: t, at: m.index + m[1].length, len: m[2].length};
    });
    if (!best) return;
    left.splice(left.indexOf(best.t), 1);
    var rest = node.splitText(best.at);
    var after = rest.splitText(best.len);
    var span = document.createElement('span');
    span.className = 'term';
    span.tabIndex = 0;
    span.appendChild(rest.cloneNode());
    var card = document.createElement('span');
    card.className = 'term-card';
    card.innerHTML = '<b></b>' + best.t.d;
    card.firstChild.textContent = best.t.t;
    span.appendChild(card);
    rest.parentNode.replaceChild(span, rest);
    // Aynı düğümün geri kalanında başka terimler olabilir.
    nodes.push(after);
  });
  document.querySelectorAll('.term').forEach(function (s) {
    s.addEventListener('mouseenter', function () {
      var c = s.querySelector('.term-card');
      s.classList.remove('flip', 'up');
      var r = s.getBoundingClientRect();
      if (r.left + 320 > window.innerWidth) s.classList.add('flip');
      if (r.bottom + c.offsetHeight + 16 > window.innerHeight && r.top > c.offsetHeight + 16) s.classList.add('up');
    });
  });
})();
</script>"""


def page_script(chapter: str, language: str) -> str:
    """Ders sayfasının sonuna eklenen işaretleme betiği; terim yoksa boş."""
    terimler = page_terms(chapter, language)
    if not terimler:
        return ""
    veri = json.dumps(terimler, ensure_ascii=False).replace("</", "<\\/")
    return _SCRIPT % veri


_TR_ORDER = "aAbBcCçÇdDeEfFgGğĞhHıIiİjJkKlLmMnNoOöÖpPqQrRsSşŞtTuUüÜvVwWxXyYzZ"


def sort_key(title: str) -> list[int]:
    """Abece sırası (Türkçe harfler yerinde: ç c'den sonra, ı i'den önce)."""
    return [_TR_ORDER.find(ch) // 2 if ch in _TR_ORDER else 100 + ord(ch) for ch in title]


def search_entries(language: str) -> list[tuple[str, str, str]]:
    """Arama için (id, başlık, açıklama düz metin)."""
    return [
        (t["id"], t["title"].get(language, ""), _CODE.sub(r"\1", t["text"].get(language, "")))
        for t in load()
    ]
