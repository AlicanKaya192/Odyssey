"""Rotalar ekranı: hangi patikanın hangi sırayla çalışılacağı.

Öğrenme Yolu "ne var" sorusuna cevap veriyor; bu ekran "nereden
başlamalıyım" sorusuna. Kişinin durumuna göre üç rota var — hiç kod
yazmamış biri, Python bilip veri bilimine geçmek isteyen biri ve ML
mühendisi olmak isteyen biri — ve rota başlıktaki seçiciyle değişiyor.

Rotalar `content/roadmaps.json` içinde; sıra ve gerekçeler içerik işi, kod
değil. **Henüz yazılmamış patikalar da rotada duruyor** ve "Yakında"
diye işaretleniyor: rota bugün uygulamada olanı değil, önerilen sırayı
anlatıyor.

Adımların ilerlemesi hesaplanıyor, saklanmıyor. Adımda `sections`
listesi varsa (örneğin Python'u bilen biri için yalnızca dört bölüm)
ilerleme o bölümler üzerinden, yoksa patikanın tamamı üzerinden.

Her adım kendini anlatıyor (Alican 29 Eylül: "daha açıklayıcı"): neden bu
sırada (`text`), bu adımda neler var (`learn`), sonunda ne yapabileceksin
(`gain`), toplam süre ve odak bölümlerinin her biri için neden o bölüm
(`sections[].why`). Odak bölümü açıksa tıklanınca doğrudan açılıyor.
"""

from __future__ import annotations

import html
import json

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ..core.catalog import Catalog
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..core.unlock import is_unlocked
from ..paths import content_dir
from ..resources.logos import logo_key, logo_svg
from ..widgets.document_view import DocumentView

# Seçilen rota hatırlanıyor; ekrana her dönüşte baştan seçtirmek gereksiz.
ROUTE_SETTING = "roadmap_route"

TRACK_ACTION = "track:"
SECTION_ACTION = "section:"


def section_ref(entry) -> str:
    """Odak bölümü girdisinin "modül/bölüm" adresi (düz metin ya da `ref`'li sözlük)."""
    return entry.get("ref", "") if isinstance(entry, dict) else str(entry)


def load_routes() -> list[dict]:
    """`content/roadmaps.json` dosyasındaki rotalar."""
    path = content_dir() / "roadmaps.json"
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return json.load(handle).get("routes", [])


class RoadmapView(QWidget):
    """Seçili rotanın adımlarını gösterir."""

    # Adımdaki "Patikaya git" bağlantısı.
    track_opened = Signal(str)
    # Odak bölümüne tıklanınca: (modül, bölüm).
    section_opened = Signal(str, str)

    def __init__(
        self,
        catalog: Catalog,
        language: LanguageManager,
        store: ProgressStore,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._catalog = catalog
        self._language = language
        self._store = store
        self._routes = load_routes()
        # Sıralı giriş her rotanın oturumdaki ilk gösteriminde (B8); ekrana
        # her dönüşte baştan oynamasın.
        self._shown_routes: set[int] = set()

        ids = [route.get("id") for route in self._routes]
        saved = store.setting(ROUTE_SETTING, "")
        self._index = ids.index(saved) if saved in ids else 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._document = DocumentView(self)
        self._document.action.connect(self._on_action)
        layout.addWidget(self._document)

        self.refresh()

    # --- seçim ------------------------------------------------------------

    @property
    def route_index(self) -> int:
        return self._index

    def route_labels(self) -> list[str]:
        return [self._language.pick(route.get("label")) for route in self._routes]

    def show_index(self, index: int) -> None:
        """Başlıktaki seçiciden gelen sıra numarası."""
        if not 0 <= index < len(self._routes) or index == self._index:
            return
        self._index = index
        self._store.set_setting(ROUTE_SETTING, self._routes[index].get("id", ""))
        self.refresh(animate=True)

    def _on_action(self, action: str) -> None:
        if action.startswith(TRACK_ACTION):
            self.track_opened.emit(action[len(TRACK_ACTION):])
        elif action.startswith(SECTION_ACTION):
            chapter_id, _, section_id = action[len(SECTION_ACTION):].partition("/")
            if section_id:
                self.section_opened.emit(chapter_id, section_id)

    # --- çizim ------------------------------------------------------------

    def refresh(self, keep_scroll: bool = False, animate: bool = False) -> None:
        """Rotayı yeniden çizer.

        İlerleme bölümlerde değiştiği için ekrana her gelişte çağrılıyor;
        o durumda kaydırma korunuyor, rota değişince sayfa başa dönüyor.
        """
        self._document.set_lang(self._language.language)
        if not self._routes:
            self._document.set_body("")
            return

        route = self._routes[self._index]
        pick = self._language.pick
        states = [self._step_state(step) for step in route.get("steps", [])]

        # "Sıradaki" işareti bitmemiş ilk adıma gidiyor. İsteğe bağlı ve
        # henüz yazılmamış adımlar atlanıyor: kimse onlarda bekletilmemeli.
        next_index = next(
            (
                i for i, (step, state) in enumerate(zip(route["steps"], states))
                if not state["soon"] and not state["done"] and not step.get("optional")
            ),
            -1,
        )

        steps = "".join(
            self._step_html(number, step, state, number - 1 == next_index)
            for number, (step, state) in enumerate(zip(route["steps"], states), start=1)
        )

        body = (
            f'<p class="route-intro">{html.escape(self._language.t("roadmap.intro"))}</p>'
            f"<h1 class=\"route-title\">{html.escape(pick(route.get('title')))}</h1>"
            f'<p class="route-intro">{html.escape(pick(route.get("intro")))}</p>'
            f'<ol class="route">{steps}</ol>'
        )
        giris = " pre-enter" if animate and self._index not in self._shown_routes else ""
        if giris:
            self._shown_routes.add(self._index)
        self._document.set_body(
            f'<div class="page narrow{giris}"><div class="content">{body}</div></div>',
            keep_scroll=keep_scroll,
        )

    def _step_state(self, step: dict) -> dict:
        """Adımın durumu: yazılmış mı, kaç bölümün kaçı bitti."""
        track = self._catalog.track(step.get("track", ""))
        if track is None or track.locked:
            return {"soon": True, "done": False, "completed": 0, "total": 0}

        if step.get("sections"):
            sections = [
                self._catalog.section(*section_ref(entry).split("/", 1))
                for entry in step["sections"]
            ]
            sections = [section for section in sections if section is not None]
        else:
            sections = [s for chapter in track.chapters for s in chapter.sections]

        completed = sum(1 for section in sections if self._completed(section))
        total = len(sections)
        return {
            "soon": False,
            "done": total > 0 and completed == total,
            "completed": completed,
            "total": total,
            "minutes": sum(section.estimated_minutes for section in sections),
        }

    def _completed(self, section) -> bool:
        state = self._store.section_state(
            section.chapter_id, section.id, section.exercises
        )
        return state.status(
            section.requires_quiz, section.requires_exercises
        ) == "completed"

    def _step_html(self, number: int, step: dict, state: dict, is_next: bool) -> str:
        t = self._language.t
        pick = self._language.pick
        track = self._catalog.track(step.get("track", ""))
        title = pick(track.title) if track else step.get("track", "")
        color = track.color if track else "#6B7280"
        # Patikanın logosu (ui-taslak.md E2); yazılmamış patikada gri.
        icon_svg = logo_svg(logo_key(track.icon if track else "", track.id if track else ""), color,
                            locked=bool(state["soon"]))

        classes = ["rstep"]
        tags = []
        if state["done"]:
            classes.append("done")
            tags.append(("ok", t("roadmap.done")))
        elif is_next:
            classes.append("next")
            tags.append(("next", t("roadmap.next")))
        if state["soon"]:
            classes.append("soon")
            tags.append(("soon", t("roadmap.soon")))
        if step.get("optional"):
            tags.append(("opt", t("roadmap.optional")))

        tag_html = "".join(
            f'<span class="rtag {kind}">{html.escape(text)}</span>'
            for kind, text in tags
        )
        marker = "✓" if state["done"] else str(number)

        learn = ""
        maddeler = (step.get("learn") or {}).get(self._language.language) or []
        if maddeler:
            learn = (
                f'<div class="rlearn"><span class="rlabel">{html.escape(t("roadmap.learn"))}</span>'
                "<ul>" + "".join(f"<li>{html.escape(m)}</li>" for m in maddeler) + "</ul></div>"
            )
        gain = ""
        if step.get("gain"):
            gain = (
                f'<div class="rgain"><b>{html.escape(t("roadmap.gain"))}</b> '
                f"{html.escape(pick(step['gain']))}</div>"
            )

        focus = ""
        if step.get("sections"):
            rows = []
            for entry in step["sections"]:
                ref = section_ref(entry)
                section = self._catalog.section(*ref.split("/", 1))
                if section is None:
                    continue
                why = pick(entry.get("why")) if isinstance(entry, dict) else ""
                bitti = self._completed(section)
                acik = is_unlocked(self._catalog, self._store, section.chapter_id, section.id)
                icerik = (
                    f'<i>{"✓" if bitti else ""}</i>'
                    f'<span><b>{html.escape(pick(section.title))}</b>'
                    + (f"<small>{html.escape(why)}</small>" if why else "")
                    + "</span>"
                )
                sinif = "rsec" + (" done" if bitti else "") + ("" if acik else " locked")
                if acik:
                    rows.append(
                        f'<a class="{sinif}" href="app:{SECTION_ACTION}{html.escape(ref)}">{icerik}</a>'
                    )
                else:
                    rows.append(
                        f'<div class="{sinif}" title="{html.escape(t("roadmap.section_locked"))}">{icerik}</div>'
                    )
            focus = (
                f'<div class="rfocus"><span class="rlabel">{html.escape(t("roadmap.focus"))}</span>'
                f"{''.join(rows)}</div>"
            )

        foot = ""
        if not state["soon"]:
            percent = round(state["completed"] * 100 / state["total"]) if state["total"] else 0
            sayac = t("roadmap.sections", done=state["completed"], total=state["total"])
            if state.get("minutes"):
                sayac += " · " + t("roadmap.hours", hours=max(1, round(state["minutes"] / 60)))
            foot = (
                '<div class="rfoot">'
                f'<div class="bar"><i style="width:{percent}%;background:{color}"></i></div>'
                f'<span class="rcount">{html.escape(sayac)}</span>'
                f'<a class="rgo" href="app:{TRACK_ACTION}{html.escape(track.id)}">'
                f'{html.escape(t("roadmap.open"))} →</a>'
                "</div>"
            )

        classes.append("stg")
        return (
            f'<li class="{" ".join(classes)}" style="--n:{number - 1}">'
            f'<div class="rnum">{marker}</div>'
            '<div class="rcard">'
            f'<span class="rlogo">{icon_svg}</span><div class="rbody">'
            f'<div class="rhead"><b>{html.escape(title)}</b>{tag_html}</div>'
            f"<p>{html.escape(pick(step.get('text')))}</p>"
            f"{learn}{gain}{focus}{foot}"
            "</div></div></li>"
        )

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._document.set_mode(mode)

    def retranslate(self) -> None:
        self.refresh(keep_scroll=True)
