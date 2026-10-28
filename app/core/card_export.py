"""Hızlı başvuru kartını dışa aktarmak: Markdown ya da yazdırılabilir PDF.

Kişinin kendi "kopya kâğıdı" (Alican 28 Ekim). Parçalar müfredat sırasında
bölüm bölüm, her bölümün içinde eklendiği sırayla; kod parçaları kod
bloğu, ötekiler paragraf. Parçanın metni olduğu gibi (seçildiği dilde);
başlıklar ve bölüm adları arayüz dilinde.

PDF, Qt'nin metin belgesiyle (`QTextDocument` + `QPdfWriter`) yazılıyor:
tarayıcı bileşeni gerekmiyor, sayfalara kendisi bölüyor.
"""

from __future__ import annotations

import html
from pathlib import Path

from PySide6.QtCore import QMarginsF
from PySide6.QtGui import QFont, QPageLayout, QPageSize, QPdfWriter, QTextDocument

PDF_MARGIN_MM = 16
PDF_RESOLUTION = 300


def _pick(values, language: str) -> str:
    if not isinstance(values, dict):
        return str(values or "")
    return values.get(language) or values.get("tr") or ""


def grouped(cards: list[dict], catalog, language: str) -> list[tuple[str, list[dict]]]:
    """(başlık "Modül · Bölüm", parçalar): müfredat sırasında; katalogda
    artık olmayan bölümün parçaları sonda, bölüm kimliğiyle."""
    sira = {(s.chapter_id, s.id): i for i, s in enumerate(catalog.all_sections)}
    gruplar: dict[tuple[str, str], list[dict]] = {}
    for kart in sorted(cards, key=lambda k: k["id"]):  # eklendiği sıra
        gruplar.setdefault((kart["chapter_id"], kart["section_id"]), []).append(kart)
    sonuc = []
    for anahtar in sorted(gruplar, key=lambda a: (sira.get(a, len(sira)), a)):
        modul = catalog.chapter(anahtar[0])
        bolum = catalog.section(*anahtar)
        if bolum is None:
            baslik = anahtar[1]
        else:
            baslik = f"{_pick(modul.title, language)} · {_pick(bolum.title, language)}"
        sonuc.append((baslik, gruplar[anahtar]))
    return sonuc


def _fence(body: str) -> str:
    """Parçanın içindekinden uzun bir ters tırnak çiti."""
    en_uzun = cit = 0
    for harf in body:
        cit = cit + 1 if harf == "`" else 0
        en_uzun = max(en_uzun, cit)
    return "`" * max(3, en_uzun + 1)


def to_markdown(groups: list[tuple[str, list[dict]]], title: str) -> str:
    satirlar = [f"# {title}", ""]
    for baslik, parcalar in groups:
        satirlar += [f"## {baslik}", ""]
        for parca in parcalar:
            govde = parca["body"].strip("\n")
            if parca["is_code"]:
                cit = _fence(govde)
                satirlar += [cit, govde, cit, ""]
            else:
                satirlar += [govde, ""]
    return "\n".join(satirlar).rstrip("\n") + "\n"


def to_html(groups: list[tuple[str, list[dict]]], title: str) -> str:
    parcalar = [f"<h1>{html.escape(title)}</h1>"]
    for baslik, kartlar in groups:
        parcalar.append(f"<h2>{html.escape(baslik)}</h2>")
        for kart in kartlar:
            govde = html.escape(kart["body"].strip("\n"))
            if kart["is_code"]:
                parcalar.append(f'<pre class="code">{govde}</pre>')
            else:
                parcalar.append("<p>" + govde.replace("\n", "<br>") + "</p>")
    return "".join(parcalar)


# Qt'nin metin belgesi kenar boşluğunu `pt` ile değil `px` ile alıyor (ölçüldü).
STYLE = """
h1 { font-size: 18pt; font-weight: 600; margin-bottom: 14px; }
h2 { font-size: 12.5pt; font-weight: 600; margin-top: 26px; margin-bottom: 10px; color: #5b3cc4; }
p { font-size: 10pt; margin-top: 0; margin-bottom: 12px; line-height: 130%; }
pre.code { font-family: 'Consolas'; font-size: 9pt; background-color: #f3f1f8;
           margin-top: 0; margin-bottom: 14px; }
"""


def write_pdf(groups: list[tuple[str, list[dict]]], title: str, path: Path) -> None:
    """A4 PDF; yazılamazsa `OSError`."""
    yazici = QPdfWriter(str(path))
    if not yazici.setPageSize(QPageSize(QPageSize.PageSizeId.A4)):
        raise OSError(f"PDF açılamadı: {path}")
    yazici.setPageMargins(QMarginsF(PDF_MARGIN_MM, PDF_MARGIN_MM, PDF_MARGIN_MM, PDF_MARGIN_MM),
                          QPageLayout.Unit.Millimeter)
    yazici.setResolution(PDF_RESOLUTION)
    yazici.setTitle(title)
    yazici.setCreator("Odyssey")
    belge = QTextDocument()
    belge.setDefaultFont(QFont("Segoe UI", 10))
    belge.setDefaultStyleSheet(STYLE)
    belge.setHtml(to_html(groups, title))
    belge.print_(yazici)
    del yazici  # dosya yazıcı kapanınca tamamlanıyor
    if not path.is_file() or path.stat().st_size == 0:
        raise OSError(f"PDF yazılamadı: {path}")
