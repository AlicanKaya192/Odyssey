"""Genel arama (`Ctrl+K`): dizin ve eşleştirme.

Arayüzden bağımsız; kutunun kendisi `ui/search_palette.py`.

**Neler aranıyor:** bölüm adları, konu anlatımı (başlık başlık: sonuca
basınca o başlığa kaydırılıyor), ders notları, alıştırmalar (adı ve
yönergesi), kullanıcının kendi notları ve ekranlar. Dizin seçili dilde
kuruluyor; dil değişince yeniden.

**Türkçe harfler katlanıyor** (`fold`): İngilizce klavyeyle "dongu"
yazan "döngü"yü buluyor. Alıştırma kodunun ASCII olmasının sebebi de
aynıydı: klavyede ş, ğ, ı olmayabiliyor. Katlama harf sayısını
değiştirmiyor; eşleşmenin metindeki yeri alıntı parçası için doğrudan
kullanılabiliyor.

**Sıralama:** önce adında geçenler (adı aranan sözle başlıyorsa en üstte),
sonra yalnızca metninde geçenler. Aynı puanda tür sırası (ekran, bölüm,
alıştırma, not, ders notu, konu anlatımı), o da eşitse katalog sırası.
Aramadaki bütün sözcükler geçmeli (VE).
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field

from .catalog import resolve_localized

_FOLD = str.maketrans({
    "İ": "i", "I": "i", "ı": "i",
    "Ş": "s", "ş": "s", "Ç": "c", "ç": "c", "Ğ": "g", "ğ": "g",
    "Ö": "o", "ö": "o", "Ü": "u", "ü": "u",
    "Â": "a", "â": "a", "Î": "i", "î": "i", "Û": "u", "û": "u",
})

KIND_WEIGHT = {
    "screen": 12,
    "command": 11,
    "section": 10,
    "term": 8,
    "exercise": 6,
    "note": 6,
    "course_note": 4,
    "lesson": 3,
}

MAX_RESULTS = 8
SNIPPET_RADIUS = 44

_TAG = re.compile(r"<[^>]+>")
# Markdown işaretleri alıntıda görünmesin. `_` bırakılıyor: `random_state`
# gibi adlar aranabilsin.
_MARKS = re.compile(r"[`*>#|]+")
_SPACE = re.compile(r"\s+")


def fold(text: str) -> str:
    """Aramada kullanılan hâl: küçük harf, Türkçe harfler katlanmış."""
    return text.translate(_FOLD).lower()


def plain(text: str) -> str:
    """Markdown/HTML'den düz metin (alıntı parçası ve eşleştirme için).

    HTML kaçışları çözülüyor: figürlerin içindeki kod `&gt;` diye yazılı,
    çözülmezse alıntıda "score &gt;= 80" görünüyordu.
    """
    return html.unescape(_SPACE.sub(" ", _MARKS.sub(" ", _TAG.sub(" ", text))).strip())


@dataclass
class SearchItem:
    """Aranabilecek bir şey ve basınca nereye gidileceği (`target`)."""

    kind: str
    title: str
    subtitle: str
    target: dict
    body: str = ""
    # Konu anlatımının başlıksız ilk parçası: adı bölümün adı, bölüm zaten
    # ayrı bir sonuç; adıyla ikinci kez çıkmasın, yalnızca metniyle.
    match_title: bool = True
    title_key: str = field(init=False, default="")
    body_key: str = field(init=False, default="")

    def __post_init__(self) -> None:
        self.title_key = fold(self.title) if self.match_title else ""
        self.body_key = fold(self.body)


@dataclass
class SearchResult:
    item: SearchItem
    score: int
    snippet: str = ""


def lesson_chunks(source: str) -> list[tuple[str, str]]:
    """Konu anlatımını `## ` başlıklarına göre böler: (başlık, metin).

    İlk parça başlıksız (girişi). Kod bloğunun içindeki `## ` başlık
    sayılmıyor; sayılsaydı başlıklarla çapalar kayardı.
    """
    parcalar: list[tuple[str, list[str]]] = [("", [])]
    kodda = False
    for line in source.splitlines():
        if line.strip().startswith("```"):
            kodda = not kodda
        if not kodda and line.startswith("## "):
            parcalar.append((line[3:].strip(), []))
            continue
        if not kodda and line.startswith("# ") and len(parcalar) == 1:
            continue  # belgenin kendi başlığı
        parcalar[-1][1].append(line)
    return [(baslik, "\n".join(satirlar)) for baslik, satirlar in parcalar]


_HEADING_LINE = re.compile(r"^#{1,6}\s")


def heading_ids(source: str) -> list[str]:
    """Konu anlatımındaki `## ` başlıklarının çapaları, sırasıyla.

    Ders okuyucusunun kendi markdown ayarlarıyla üretiliyor; aynı
    başlık iki kez geçerse kütüphane ikinciye `_1` ekliyor, burada da aynısı.

    **Yalnızca başlık satırları çevriliyor.** Bütün dersi çevirmek dizin
    kurmanın %83'üydü (54 derste ~1 sn, ilk açılışta arayüz bekliyordu).
    Çapa yalnızca başlığın kendi metninden ve önceki başlıklardan
    (tekilleştirme) çıkıyor; bütün düzeyler dahil edildiği için sıra
    bozulmuyor. Tam çeviriyle birebir aynı sonucu verdiği her derste
    sınandı.
    """
    import markdown

    from ..ui.lesson_view import MARKDOWN_EXTENSIONS

    satirlar = []
    kodda = False
    for line in source.splitlines():
        if line.strip().startswith("```"):
            kodda = not kodda
            continue
        if not kodda and _HEADING_LINE.match(line):
            satirlar.append(line)

    converter = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
    converter.convert("\n\n".join(satirlar))
    return [
        token["id"]
        for token in getattr(converter, "toc_tokens", [])
        for token in [token, *token.get("children", [])]
        if token["level"] == 2
    ]


def _read(path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def build_index(catalog, language: str, pick) -> list[SearchItem]:
    """Katalogdaki her şeyin dizini (kullanıcı notları ve ekranlar hariç).

    `pick` iki dilli bir sözlükten seçili dildeki metni veriyor
    (`LanguageManager.pick`).
    """
    items: list[SearchItem] = []
    for chapter in catalog.chapters:
        patika = pick(chapter.title)
        for section in chapter.sections:
            bolum = pick(section.title)
            yer = f"{patika}  ›  {bolum}"
            base = {"chapter": chapter.id, "section": section.id}
            items.append(SearchItem("section", bolum, patika, {"type": "section", **base}))

            for block in section.blocks:
                if block.type == "lesson":
                    resolved = block.file_for(language)
                    if not resolved or not resolved.exists:
                        continue
                    source = _read(resolved.path)
                    ids = heading_ids(source)
                    for index, (baslik, metin) in enumerate(lesson_chunks(source)):
                        anchor = ids[index - 1] if 0 < index <= len(ids) else ""
                        items.append(
                            SearchItem(
                                "lesson",
                                baslik or bolum,
                                yer,
                                {"type": "lesson", **base, "anchor": anchor},
                                body=plain(metin),
                                match_title=bool(baslik),
                            )
                        )
                elif block.type == "notes":
                    for index, document in enumerate(block.documents):
                        resolved = resolve_localized(
                            block.directory, document.get("file", ""), language
                        )
                        items.append(
                            SearchItem(
                                "course_note",
                                pick(document.get("title")),
                                yer,
                                {"type": "course_note", **base, "document": index},
                                body=plain(_read(resolved.path)) if resolved else "",
                            )
                        )

            for index, exercise in enumerate(section.exercises):
                prompt = exercise.prompt_for(language)
                items.append(
                    SearchItem(
                        "exercise",
                        pick(exercise.title),
                        yer,
                        {"type": "exercise", **base, "exercise": index},
                        body=plain(_read(prompt.path)) if prompt else "",
                    )
                )
    return items


def _snippet(item: SearchItem, token: str) -> str:
    """Metinde ilk eşleşmenin çevresi; kelime ortasından başlamıyor."""
    konum = item.body_key.find(token)
    if konum < 0:
        return ""
    bas = max(0, konum - SNIPPET_RADIUS)
    son = min(len(item.body), konum + len(token) + SNIPPET_RADIUS)
    if bas > 0:
        bosluk = item.body.find(" ", bas)
        bas = bosluk + 1 if 0 <= bosluk < konum else bas
    if son < len(item.body):
        bosluk = item.body.rfind(" ", konum + len(token), son)
        son = bosluk if bosluk > 0 else son
    parca = item.body[bas:son].strip()
    return ("…" if bas > 0 else "") + parca + ("…" if son < len(item.body) else "")


def search(query: str, items: list[SearchItem], limit: int = MAX_RESULTS) -> list[SearchResult]:
    """Aramanın sonuçları, en iyisi başta."""
    tokens = fold(query).split()
    if not tokens:
        return []
    butun = " ".join(tokens)

    sonuclar: list[SearchResult] = []
    for item in items:
        ad = item.title_key
        if ad and all(token in ad for token in tokens):
            puan = 100
            if ad.startswith(butun):
                puan += 50
            elif any(word.startswith(tokens[0]) for word in ad.split()):
                puan += 25
            alinti = ""
        elif item.body_key and all(token in item.body_key or token in ad for token in tokens):
            puan = 40
            ilk = next((token for token in tokens if token in item.body_key), tokens[0])
            alinti = _snippet(item, ilk)
        else:
            continue
        sonuclar.append(SearchResult(item, puan + KIND_WEIGHT.get(item.kind, 0), alinti))

    # Sıralama kararlı: aynı puanda katalog sırası korunuyor.
    sonuclar.sort(key=lambda sonuc: -sonuc.score)
    return sonuclar[:limit]
