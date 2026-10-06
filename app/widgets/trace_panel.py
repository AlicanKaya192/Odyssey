"""Adım adım izleme paneli.

Alıştırmada "Adım adım" düğmesine basılınca kod denetleyicide izlenerek
çalışıyor (`sandbox/harness.py` → `run_traced`): her satırdan önce
değişkenler ve o ana kadarki çıktı kaydediliyor. Bu panel kaydı ileri geri
oynatıyor; editör sıradaki satırı işaretliyor (`CodeEditor.set_trace_line`).

Sıfırdan öğrenen biri döngünün içinde değişkenin nasıl değiştiğini kafasında
canlandıramıyor; burada her adımda hangi değişkenin **yeni** geldiğini ve
hangisinin **değiştiğini** renkle görüyor.

Terminalin yerinde açılıyor ve onun koyu renklerini kullanıyor: aynı yer,
aynı görünüm. Klavye: ← → adım, Home / End baş ve son, Esc kapatır.

**İki kaynak** (Alican: kod yazmamış, soruyu anlamamış ya da yanlış yazmış
biri doğru yolun nasıl ilerlediğini göremiyordu): "Kendi kodum" editördeki
kodu, "Örnek çözüm" alıştırmanın çözümünü oynatıyor. Çözüm panelin içindeki
ayrı, salt okunur kod alanında; kişinin editöründeki koda dokunulmuyor.
Hangisinin çalıştırılacağına `ExerciseView` karar veriyor (çözüm cevabı
gösterdiği için ilk seferde onay soruyor); panel yalnızca
`source_requested` yayıyor.
"""

from __future__ import annotations

import html

from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..resources.icons import icon
from ..resources.theme.tokens import FONTS
from .code_editor import CodeEditor
from .terminal_view import COLORS

_BUTTON_CSS = (
    f"QPushButton {{ background:transparent; color:{COLORS['title']}; border:1px solid"
    f" {COLORS['button_border']}; border-radius:6px; padding:2px 8px; font-size:11.5px;"
    f" min-height:0px; }}"
    f"QPushButton:hover {{ background:{COLORS['button_hover']}; }}"
    f"QPushButton:disabled {{ border-color:{COLORS['border']}; }}"
)


def _esc(text: str) -> str:
    return html.escape(text, quote=False)


class TracePanel(QFrame):
    """Kaydedilmiş adımları gösterir; `step_changed(satır, tür)` yayar.

    tür: "line" (sıradaki satır), "return" (fonksiyon dönüyor), "error"
    (program bu satırda hata verdi) ya da "" (işaret yok).
    """

    step_changed = Signal(object, str)
    closed = Signal()
    # "user" ya da "solution": kişi kaynağı değiştirmek istiyor.
    source_requested = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("trace")
        self.setStyleSheet(
            f"QFrame#trace {{ background:{COLORS['bg']};"
            f" border:1px solid {COLORS['border']}; border-radius:16px; }}"
        )
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._t = lambda key, **kw: key
        self._steps: list[dict] = []
        self._stdout = ""
        self._error: dict | None = None
        self._truncated = False
        self._hint = ""
        self._index = 0
        self._source = "user"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- başlık ve düğmeler ------------------------------------------
        bar = QFrame()
        bar.setObjectName("traceBar")
        bar.setStyleSheet(
            f"QFrame#traceBar {{ background:transparent; border:none;"
            f" border-bottom:1px solid {COLORS['border']}; border-radius:0; }}"
        )
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(14, 8, 10, 8)
        bar_layout.setSpacing(6)
        self._title = QLabel()
        self._title.setStyleSheet(
            f"background:transparent; color:{COLORS['title']}; font-size:12.5px; font-weight:600;"
        )
        bar_layout.addWidget(self._title)
        self._counter = QLabel()
        self._counter.setStyleSheet(f"background:transparent; color:{COLORS['dim']}; font-size:12px;")
        bar_layout.addWidget(self._counter)
        bar_layout.addSpacing(10)
        # Kaynak seçimi: kendi kodum / örnek çözüm.
        self._source_buttons: dict[str, QPushButton] = {}
        for kaynak in ("user", "solution"):
            dugme = QPushButton()
            dugme.setCheckable(True)
            dugme.setCursor(Qt.CursorShape.PointingHandCursor)
            dugme.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            dugme.setStyleSheet(
                _BUTTON_CSS
                + f"QPushButton:checked {{ background:{COLORS['button_hover']}; color:{COLORS['accent']};"
                f" border-color:{COLORS['prompt']}; }}"
            )
            dugme.clicked.connect(lambda _=False, k=kaynak: self._on_source(k))
            self._source_buttons[kaynak] = dugme
            bar_layout.addWidget(dugme)
        bar_layout.addStretch(1)

        self._buttons: dict[str, QPushButton] = {}
        for ad, simge, adim in (("first", "skip-start", None), ("prev", "chevron-left", -1),
                                ("next", "chevron-right", 1), ("last", "skip-end", None)):
            dugme = QPushButton()
            dugme.setIcon(icon(simge, COLORS["title"], 14))
            dugme.setCursor(Qt.CursorShape.PointingHandCursor)
            dugme.setStyleSheet(_BUTTON_CSS)
            dugme.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            if ad == "first":
                dugme.clicked.connect(lambda: self.set_index(0))
            elif ad == "last":
                dugme.clicked.connect(lambda: self.set_index(len(self._steps) - 1))
            else:
                dugme.clicked.connect(lambda _=False, d=adim: self.set_index(self._index + d))
            self._buttons[ad] = dugme
            bar_layout.addWidget(dugme)
        bar_layout.addSpacing(6)
        self.close_button = QPushButton()
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.setStyleSheet(_BUTTON_CSS)
        self.close_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.close_button.clicked.connect(self.closed.emit)
        bar_layout.addWidget(self.close_button)
        layout.addWidget(bar)

        # --- kaydırıcı ve açıklama ---------------------------------------
        ust = QVBoxLayout()
        ust.setContentsMargins(14, 10, 14, 4)
        ust.setSpacing(8)
        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._slider.setStyleSheet(
            f"QSlider {{ background:transparent; }}"
            f"QSlider::groove:horizontal {{ height:4px; background:{COLORS['border']}; border-radius:2px; }}"
            f"QSlider::sub-page:horizontal {{ background:{COLORS['prompt']}; border-radius:2px; }}"
            f"QSlider::handle:horizontal {{ background:{COLORS['accent']}; width:12px; height:12px;"
            f" margin:-4px 0; border-radius:6px; }}"
        )
        self._slider.valueChanged.connect(self.set_index)
        ust.addWidget(self._slider)
        self._message = QLabel()
        self._message.setWordWrap(True)
        self._message.setTextFormat(Qt.TextFormat.RichText)
        self._message.setStyleSheet(f"background:transparent; color:{COLORS['text']}; font-size:13px;")
        ust.addWidget(self._message)
        layout.addLayout(ust)

        # --- (örnek çözüm) | değişkenler | çıktı --------------------------
        govde = QHBoxLayout()
        govde.setContentsMargins(4, 0, 4, 6)
        govde.setSpacing(0)
        self._code_title, _bos = self._pane()
        _bos.deleteLater()
        # Örnek çözümün kodu: salt okunur, sıradaki satır işaretli. Kişinin
        # editöründeki kod yerinde kalıyor.
        self._code = CodeEditor(mode="dark")
        self._code.setProperty("card", "true")
        self._code.setReadOnly(True)
        self._code.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._code.setStyleSheet(f"QTextEdit {{ background:transparent; border:none; color:{COLORS['text']}; }}")
        self._vars_title, self._vars = self._pane()
        self._out_title, self._out = self._pane()
        self._code_column = QWidget()
        self._code_column.setStyleSheet("background:transparent;")
        for baslik, alan, pay in ((self._code_title, self._code, 3), (self._vars_title, self._vars, 3),
                                  (self._out_title, self._out, 2)):
            kap = self._code_column if alan is self._code else QWidget()
            kap.setStyleSheet("background:transparent;")
            sutun = QVBoxLayout(kap)
            sutun.setContentsMargins(0, 0, 0, 0)
            sutun.setSpacing(0)
            sutun.addWidget(baslik)
            sutun.addWidget(alan, 1)
            govde.addWidget(kap, pay)
        self._code_column.hide()
        layout.addLayout(govde, 1)

    def _pane(self) -> tuple[QLabel, QTextEdit]:
        baslik = QLabel()
        baslik.setStyleSheet(
            f"background:transparent; color:{COLORS['dim']}; font-size:11px; font-weight:700;"
            f" letter-spacing:0.5px; padding:4px 10px 0 10px;"
        )
        alan = QTextEdit()
        alan.setReadOnly(True)
        alan.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        alan.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        alan.setStyleSheet(
            f"QTextEdit {{ background:transparent; color:{COLORS['text']}; border:none;"
            f" border-radius:0; padding:2px 6px; font-family:{FONTS['mono']}; font-size:13px;"
            f" selection-background-color:#34405A; }}"
        )
        return baslik, alan

    # --- veri ------------------------------------------------------------

    def load(self, steps: list[dict], stdout: str, error: dict | None, truncated: bool,
             hint: str = "", source: str = "user", code: str = "") -> None:
        """Kaydı yükler; `hint` hatanın ne anlama geldiği (son adımda).

        `source` "solution" ise `code` panelin kendi kod alanında gösteriliyor
        ve sıradaki satır orada işaretleniyor.
        """
        self._hint = hint
        self._source = source
        for kaynak, dugme in self._source_buttons.items():
            dugme.setChecked(kaynak == source)
        cozum = source == "solution"
        self._code_column.setVisible(cozum)
        if cozum:
            self._code.set_language("python")
            self._code.setPlainText(code)
        self._steps = steps or [{"line": 0, "event": "end", "out": len(stdout), "stack": []}]
        self._stdout = stdout
        self._error = error
        self._truncated = truncated
        self._slider.blockSignals(True)
        self._slider.setRange(0, len(self._steps) - 1)
        self._slider.blockSignals(False)
        self._index = -1
        self.set_index(0)

    @property
    def index(self) -> int:
        return self._index

    @property
    def source(self) -> str:
        return self._source

    def _on_source(self, kaynak: str) -> None:
        # Düğme kendiliğinden işaretlenmesin; yükleme bitince `load` işaretliyor.
        for k, dugme in self._source_buttons.items():
            dugme.setChecked(k == self._source)
        if kaynak != self._source:
            self.source_requested.emit(kaynak)

    def _has_lines(self) -> bool:
        return any(adim["event"] != "end" for adim in self._steps)

    @property
    def count(self) -> int:
        return len(self._steps)

    def set_index(self, index: int) -> None:
        if not self._steps:
            return
        index = max(0, min(index, len(self._steps) - 1))
        if index == self._index:
            return
        self._index = index
        self._slider.blockSignals(True)
        self._slider.setValue(index)
        self._slider.blockSignals(False)
        self._buttons["first"].setEnabled(index > 0)
        self._buttons["prev"].setEnabled(index > 0)
        self._buttons["next"].setEnabled(index < len(self._steps) - 1)
        self._buttons["last"].setEnabled(index < len(self._steps) - 1)
        self._render()
        adim = self._steps[index]
        if adim["event"] == "end":
            satir = (self._error or {}).get("line")
            satir, tur = (satir, "error") if isinstance(satir, int) else (None, "")
        else:
            satir, tur = adim["line"], adim["event"]
        if self._source == "solution":
            # Çözüm panelin kendi kod alanında; editördeki işaret kalkıyor.
            self._code.set_trace_line(satir, tur or "line")
            self.step_changed.emit(None, "")
        else:
            self.step_changed.emit(satir, tur)

    # --- çizim -----------------------------------------------------------

    def _render(self) -> None:
        t = self._t
        adim = self._steps[self._index]
        onceki = self._steps[self._index - 1] if self._index > 0 else None
        self._counter.setText(t("trace.counter", step=self._index + 1, total=len(self._steps)))

        yigin = adim["stack"]
        icteki = yigin[-1]["func"] if yigin else ""
        olay = adim["event"]
        if olay == "line":
            mesaj = t("trace.next_line", line=adim["line"])
            if icteki:
                mesaj += " " + t("trace.inside", func=icteki)
            renk = "text"
        elif olay == "return":
            mesaj, renk = t("trace.returned", func=icteki, value=adim.get("value", "")), "accent"
        elif self._error:
            mesaj = t("trace.error", type=self._error.get("type", ""), message=self._error.get("message", ""))
            renk = "fail"
        elif not self._has_lines() and self._source == "user":
            # Kodda çalışacak satır yok (yalnızca yorum): örnek çözüme yönlendir.
            mesaj, renk = t("trace.empty"), "warn"
        else:
            mesaj, renk = t("trace.finished", total=len(self._steps)), "ok"
        metin = f'<span style="color:{COLORS[renk]};">{_esc(mesaj)}</span>'
        if olay == "end" and self._error and self._hint:
            metin += f'<br><span style="color:{COLORS["warn"]};">💡 {_esc(self._hint)}</span>'
        if self._truncated and self._index == len(self._steps) - 1:
            metin += f'<br><span style="color:{COLORS["warn"]};">{_esc(t("trace.truncated", count=len(self._steps) - 1))}</span>'
        self._message.setText(metin)

        self._vars.setHtml(self._vars_html(yigin, onceki["stack"] if onceki else []))
        self._out.setHtml(self._out_html(adim["out"], onceki["out"] if onceki else 0))

    def _vars_html(self, yigin: list[dict], onceki: list[dict]) -> str:
        t = self._t
        if not any(c["vars"] for c in yigin):
            return f'<div style="color:{COLORS["dim"]};">{_esc(t("trace.no_vars"))}</div>'
        parcalar = []
        # En içteki çerçeve (şu an çalışan fonksiyon) üstte.
        for derinlik in range(len(yigin) - 1, -1, -1):
            cerceve = yigin[derinlik]
            eski = {}
            if derinlik < len(onceki) and onceki[derinlik]["func"] == cerceve["func"]:
                eski = {ad: deger for ad, deger, _tur in onceki[derinlik]["vars"]}
            baslik = t("trace.frame_func", func=cerceve["func"]) if cerceve["func"] else t("trace.frame_main")
            soluk = derinlik != len(yigin) - 1
            parcalar.append(
                f'<div style="color:{COLORS["dim"] if soluk else COLORS["title"]};'
                f' font-weight:700; margin-top:4px;">{_esc(baslik)}</div>'
            )
            satirlar = []
            for ad, deger, tur in cerceve["vars"]:
                if ad not in eski and onceki:
                    renk, etiket = COLORS["ok"], t("trace.new")
                elif ad in eski and eski[ad] != deger:
                    renk, etiket = COLORS["warn"], t("trace.changed")
                else:
                    renk, etiket = (COLORS["dim"] if soluk else COLORS["text"]), ""
                satirlar.append(
                    f'<tr><td style="color:{renk}; padding-right:10px;">{_esc(ad)}</td>'
                    f'<td style="color:{COLORS["dim"]}; padding-right:10px;">=</td>'
                    f'<td style="color:{renk}; padding-right:14px;">{_esc(deger)}</td>'
                    f'<td style="color:{COLORS["dim"]}; padding-right:10px;">{_esc(tur)}</td>'
                    f'<td style="color:{renk};">{_esc(etiket)}</td></tr>'
                )
            if satirlar:
                parcalar.append('<table cellspacing="0" cellpadding="1">' + "".join(satirlar) + "</table>")
            else:
                parcalar.append(f'<div style="color:{COLORS["dim"]};">{_esc(t("trace.no_vars"))}</div>')
        return "".join(parcalar)

    def _out_html(self, son: int, onceki: int) -> str:
        if son <= 0:
            return f'<div style="color:{COLORS["dim"]};">{_esc(self._t("trace.no_output"))}</div>'
        eski, yeni = self._stdout[:onceki], self._stdout[onceki:son]

        def satirlar(metin: str, renk: str) -> str:
            return _esc(metin).replace("\n", "<br>") if renk == "text" else (
                f'<span style="color:{COLORS[renk]};">{_esc(metin).replace(chr(10), "<br>")}</span>'
            )

        # Bu adımda yazılan kısım yeşil: hangi satırın neyi yazdırdığı görünsün.
        return (
            f'<div style="color:{COLORS["text"]}; white-space:pre;">'
            f'{satirlar(eski, "text")}{satirlar(yeni, "ok")}</div>'
        )

    # --- klavye ----------------------------------------------------------

    def event(self, event) -> bool:  # noqa: D102
        # Pencerenin Esc kısayolu (bölümden çık) tuşu önce yakalıyor;
        # panel odaktayken Esc paneli kapatsın.
        if event.type() == QEvent.Type.ShortcutOverride and event.key() == Qt.Key.Key_Escape:
            event.accept()
            return True
        return super().event(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        tus = event.key()
        if tus in (Qt.Key.Key_Right, Qt.Key.Key_Down, Qt.Key.Key_Space):
            self.set_index(self._index + 1)
        elif tus in (Qt.Key.Key_Left, Qt.Key.Key_Up):
            self.set_index(self._index - 1)
        elif tus == Qt.Key.Key_Home:
            self.set_index(0)
        elif tus == Qt.Key.Key_End:
            self.set_index(len(self._steps) - 1)
        elif tus == Qt.Key.Key_Escape:
            self.closed.emit()
        else:
            super().keyPressEvent(event)

    # --- metinler --------------------------------------------------------

    def retranslate(self, t) -> None:
        self._t = t
        self._title.setText(t("trace.title"))
        self.close_button.setText(t("trace.close"))
        self._vars_title.setText(t("trace.vars"))
        self._code_title.setText(t("trace.solution_code"))
        self._source_buttons["user"].setText(t("trace.source_user"))
        self._source_buttons["solution"].setText(t("trace.source_solution"))
        self._source_buttons["solution"].setToolTip(t("trace.source_solution_tip"))
        self._out_title.setText(t("trace.output"))
        for ad in ("first", "prev", "next", "last"):
            self._buttons[ad].setToolTip(t(f"trace.{ad}"))
        if self._steps and self._index >= 0:
            self._render()
