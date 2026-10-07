"""Alıştırma görünümü: yönerge, kademeli ipuçları, kod editörü ve sonuçlar.

Kod arka planda ayrı bir süreçte çalıştırılır; çalışırken arayüz donmaz.

İki tasarım kararı burada belirleyici:

- **Kademeli ipucu.** Tek bir "çözümü göster" düğmesi kullanıcıyı ya hiç
  yardım almamaya ya da doğrudan cevabı görmeye zorluyor. Üç kademe, tıkanan
  kişinin ihtiyacı kadar yardım almasını sağlıyor.
- **Hata açıklaması.** Python'un hata mesajları doğru ama öğretmiyor. Hatanın
  altında ne anlama geldiği ve nasıl düzeltileceği yazıyor.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

import html
import json
import textwrap
import time
from pathlib import Path

from ..widgets.feedback import ButtonSpinner, EdgeFlash
from ..core import workspace_files
from ..core.catalog import Exercise
from ..core.grader import describe, summarise
from ..core.language import LanguageManager
from ..core.mistakes import explain
from ..core.progress import ProgressStore
from ..core.runner import RunResult, run_code
from ..core.stuck import STUCK_AFTER, failures_since_pass, find_spot
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, SPACING
from ..version import APP_VERSION
from ..widgets.code_editor import CodeEditor
from ..widgets.common import SegmentedControl
from ..widgets.draw_pad import clean_drawing, empty_drawing
from ..widgets.file_tabs import FileTabs
from ..widgets.grip_splitter import GripSplitter
from ..widgets.problem_panel import ProblemPanel
from ..widgets.request_panel import RequestPanel
from ..widgets.terminal_view import TerminalView, block, line
from ..widgets.trace_panel import TracePanel
from .attempt_history import exercise_markdown, run_detail
from .git_exercise import GitWork, saved_commands
from .lesson_view import LessonView, render_markdown
from .tables_window import TablesWindow

# Zorluk göstergesi: dolu/boş daire. Renk körlüğü için renge ek olarak biçim.
DIFFICULTY_LABELS = {1: "●○○", 2: "●●○", 3: "●●●"}


def exercise_key(exercise: Exercise) -> str:
    """Alıştırmayı bütün içerik içinde tek olarak adlandırır.

    SQL alıştırmalarının veritabanı bu adla açılıyor. Yalnızca alıştırma
    kimliği yetmiyor: iki farklı bölümde aynı adlı alıştırma olabiliyor ve
    ikisi aynı veritabanını paylaşırsa biri ötekinin tohumunu eziyor.
    """
    parcalar = exercise.directory.parts
    if len(parcalar) >= 4:
        return "/".join((parcalar[-4], parcalar[-3], exercise.id))
    return exercise.id


# Kaç yanlış denemeden sonra çözüm yolları kendiliğinden açılıyor.
REVEAL_AFTER_ATTEMPTS = 2

# Sol paneldeki sekmeler: yönerge ve ikinci sekme. İkinci sekme problemde
# "Çözüm yolları", kod alıştırmasında "Çıktı" (grafikler ve tutmayan çok
# satırlı çıktılar). Yığındaki sayfa sırası: yönerge, çözümler, çıktı.
BRIEF_PROMPT = 0
BRIEF_SOLUTIONS = 1
PAGE_OUTPUT = 2
PAGE_HISTORY = 3
PAGE_REQUEST = 4
# Sol paneldeki sekmelerin anahtarı → yığındaki sayfa.
PAGES = {"prompt": BRIEF_PROMPT, "solutions": BRIEF_SOLUTIONS, "output": PAGE_OUTPUT,
         "history": PAGE_HISTORY, "request": PAGE_REQUEST}
TAB_LABELS = {"prompt": "problem.tab_prompt", "solutions": "problem.tab_solutions",
              "output": "exercise.tab_output", "history": "history.tab",
              "request": "request.tab"}

# Nota eklenen kodun markdown etiketi (editör dili → kod bloğu etiketi).
NOTE_TAGS = {"tsql": "sql", "shell": "bash", "text": "text"}

# Terminal ile editör arasındaki ilk bölüşüm (piksel).
EDITOR_SHARE = 560
TERMINAL_SHARE = 240

# Terminaldeki düz yazı satırları bu genişlikte sarılıyor; satırlar
# kaydırılmadığı için uzun bir açıklama yoksa ekrandan taşardı.
PROSE_WIDTH = 92

# Terminalde gösterilen en fazla istek satırı (API alıştırması).
REQUEST_LINES = 12


class RunWorker(QThread):
    """Kodu arka planda çalıştırır."""

    completed = Signal(object)

    def __init__(self, code: str | dict, exercise: Exercise, parent=None) -> None:
        # Ebeveyn veriliyor: pencere kapanırken çalışan iş parçacıkları
        # `findChildren` ile bulunup bekleniyor (`MainWindow.closeEvent`).
        # `code` çok dosyalı alıştırmada ad → metin sözlüğü.
        super().__init__(parent)
        self._code = code
        self._exercise = exercise

    def run(self) -> None:  # noqa: D102
        self.completed.emit(
            run_code(
                self._code,
                self._exercise.checks,
                self._exercise.timeout_sec,
                self._exercise.directory,
                language=self._exercise.language,
                exercise_key=exercise_key(self._exercise),
                entry=self._exercise.entry,
            )
        )




class TraceWorker(QThread):
    """Kodu adım adım izleyerek çalıştırır (kontrol yok, kayıt yok)."""

    completed = Signal(object)

    def __init__(self, code: str | dict, exercise: Exercise, parent=None) -> None:
        super().__init__(parent)
        self._code = code
        self._exercise = exercise

    def run(self) -> None:  # noqa: D102
        # İzleme kodu yavaşlatıyor; süre normal çalıştırmanın üç katı.
        self.completed.emit(
            run_code(
                self._code,
                [],
                max(30, self._exercise.timeout_sec * 3),
                self._exercise.directory,
                trace=True,
                entry=self._exercise.entry,
            )
        )


class RequestWorker(QThread):
    """API 2 istek paneli: isteği kodun şu anki hâline gönderir (kayıt yok)."""

    completed = Signal(object)

    def __init__(self, code: str | dict, exercise: Exercise, step: dict, parent=None) -> None:
        super().__init__(parent)
        self._code = code
        self._exercise = exercise
        self._step = step

    def run(self) -> None:  # noqa: D102
        http = next(c for c in self._exercise.checks if c.get("type") == "http")
        check = {"type": "http", "app": http.get("app", "app"), "steps": [dict(self._step, capture=True)]}
        if http.get("module"):
            check["module"] = http["module"]
        self.completed.emit(run_code(self._code, [check], self._exercise.timeout_sec,
                                     self._exercise.directory, entry=self._exercise.entry))


class ServerWorker(QThread):
    """API 2: kişinin uygulamasını uvicorn ile açar ve hazır olmasını bekler."""

    completed = Signal(object, bool)

    def __init__(self, files: dict, exercise: Exercise, parent=None) -> None:
        super().__init__(parent)
        self._files = files
        self._exercise = exercise

    def run(self) -> None:  # noqa: D102
        from ..core import live_server

        http = next((c for c in self._exercise.checks if c.get("type") == "http"), {})
        try:
            server = live_server.start(self._files, self._exercise.directory, self._exercise.entry,
                                       module=str(http.get("module", "")), app=str(http.get("app", "app")))
        except Exception:  # noqa: BLE001 - açılamazsa kişiye söyleniyor
            from ..core import log

            log.get(__name__).exception("Sunucu başlatılamadı")
            self.completed.emit(None, False)
            return
        self.completed.emit(server, server.wait_ready())


class SnapshotWorker(QThread):
    """Kod çalıştırmadan yalnızca tabloların hâlini alır.

    Boş SQL gönderiliyor: hiçbir toplu iş çalışmıyor ama veritabanı
    kuruluyor ve anlık görüntü alınıyor. Normal çalıştırma yolundan
    geçirilmiyor, çünkü orası ilerlemeyi kaydediyor ve deneme sayıyor —
    "Tablolar"a basmak bir deneme değil.
    """

    completed = Signal(object)

    def __init__(self, exercise: Exercise, parent=None) -> None:
        super().__init__(parent)
        self._exercise = exercise

    def run(self) -> None:  # noqa: D102
        self.completed.emit(
            run_code(
                "",
                [],
                self._exercise.timeout_sec,
                self._exercise.directory,
                language=self._exercise.language,
                exercise_key=exercise_key(self._exercise),
            )
        )


class ExerciseView(QWidget):
    """Bir alıştırmanın tamamı."""

    solved = Signal(str)
    # Yönergenin altındaki "devam" düğmesi: sonraki alıştırma ya da bölüm.
    advance = Signal()
    # "Takıldın mı?" kartındaki "Derse git": dersin o başlığına (çapa; "" başı).
    lesson_requested = Signal(str)

    def __init__(
        self,
        language: LanguageManager,
        store: ProgressStore,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._store = store
        self._mode = "light"
        self._exercise: Exercise | None = None
        self._chapter_id = ""
        self._section_id = ""
        self._worker: RunWorker | None = None
        self._trace_worker: TraceWorker | None = None
        # API 2: istek paneli ve "Sunucuyu başlat".
        self._request_worker: RequestWorker | None = None
        self._server_worker: ServerWorker | None = None
        self._server = None
        # "Takıldın mı?" (core/stuck.py): bu oturumdaki başarısız çalıştırma
        # sayısı ve bölümün ders metnini veren işlev (TopicView veriyor).
        self._session_fails = 0
        self._stuck_announced = False
        self._stuck_cache: tuple[str, str, object] | None = None
        self.lesson_source = lambda: ""
        self._trace_started = 0.0
        self._sizes_before_trace: list[int] | None = None
        self._trace_source = "user"
        self._trace_code = ""
        # Örnek çözümü izlemeyi onaylanan alıştırmalar (oturum boyunca).
        self._solution_confirmed: set[str] = set()
        self.confirm_dialog = None
        self._snapshot: SnapshotWorker | None = None
        # Son çalıştırmanın sonundaki tablo hâli ve onu gösteren pencere.
        self._tables: list[dict] = []
        self._tables_window: TablesWindow | None = None
        # Açılmış ipucu kademeleri. Her kademe kendi başına açılıyor:
        # "kaçıncıya kadar açık" diye tek bir sayı tutulduğunda son
        # kademeye basmak öncekileri de açıyor ve kademeli yardım fikri
        # ortadan kalkıyor.
        self._revealed: set[int] = set()
        self._advance_label: str | None = None
        # Sol paneldeki "Çıktı" sekmesinin içeriği var mı (kod alıştırması).
        self._has_output = False
        self._run_started = 0.0
        self._revealed_solution = False
        # Sol paneldeki sekmeler duruma göre değişiyor (Yönerge her zaman;
        # Çıktı, Çözüm yolları ve Denemelerim gerektiğinde).
        self._tab_keys = ["prompt"]
        self._tab_current = "prompt"
        self._attempt_count = 0
        self._git_study_marked = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Tutamağı görünen ayırıcı: sürüklenebildiği fark edilsin.
        splitter = GripSplitter(Qt.Orientation.Horizontal)
        self._splitter = splitter
        splitter.addWidget(self._build_brief())
        # Sağ taraf alıştırmanın türüne göre: kod alıştırmasında editör,
        # matematik probleminde cevap alanları.
        self._work_stack = QStackedWidget()
        self._code_work = self._build_work()
        self._work_stack.addWidget(self._code_work)
        self._work_stack.addWidget(self._build_problem_work())
        # Git patikası: kod yok, terminale komut yazılıyor.
        self._git = GitWork(self._language)
        self._git.changed.connect(self._on_git_changed)
        self._git.solved.connect(self._on_git_solved)
        self._work_stack.addWidget(self._git)
        splitter.addWidget(self._work_stack)
        # Maketteki oran: yönerge 340-430 arası, kalanı çalışma alanı.
        splitter.setSizes([430, 770])
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)

    # --- sol: yönerge -----------------------------------------------------

    def _build_brief(self) -> QWidget:
        """Sol panel: başlık, etiketler, yönerge ve ipuçları.

        Hepsi tek bir belge olarak çiziliyor. Önceden başlık ve etiketler Qt
        widget'ı, yönerge ise HTML'di; iki ayrı motorun yazı tipleri ve
        boşlukları tutmadığı için ekran sıkışık ve orantısız duruyordu.
        """
        panel = QFrame()
        panel.setProperty("surface", "plain")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Problemde çözüm açılınca "Yönerge / Çözüm yolları" sekmeleri
        # beliriyor. Çözüm sağdaki kâğıdın altına açıldığında kâğıdı
        # eziyordu (Alican bildirdi); solda açılınca kişi kendi kâğıdı sağda
        # dururken çözümü okuyup satır satır karşılaştırabiliyor.
        self._brief_tabs = SegmentedControl()
        self._brief_tabs.changed.connect(self._on_brief_tab)
        tabs_row = QHBoxLayout()
        tabs_row.setContentsMargins(SPACING["lg"], SPACING["sm"], SPACING["lg"], 0)
        tabs_row.addWidget(self._brief_tabs)
        tabs_row.addStretch(1)
        self._brief_tabs_holder = QWidget()
        self._brief_tabs_holder.setProperty("role", "bare")
        self._brief_tabs_holder.setLayout(tabs_row)
        self._brief_tabs_holder.hide()
        layout.addWidget(self._brief_tabs_holder)

        self._brief_stack = QStackedWidget()
        self._prompt = LessonView(self._language, compact=True, glossary=True)
        self._prompt.action.connect(self._on_prompt_action)
        self._brief_stack.addWidget(self._prompt)
        self._solutions = LessonView(self._language, compact=True)
        self._brief_stack.addWidget(self._solutions)
        # Kod alıştırmasında çalıştırmanın ürettiği grafikler ve tutmayan
        # çok satırlı çıktılar. Terminalin dar alanında tablolar ve
        # grafikler okunmuyordu; burada tam genişlikte.
        self._output_view = LessonView(self._language, compact=True)
        self._brief_stack.addWidget(self._output_view)
        # Geçmiş denemeler: yanlış kodlar ve son doğru kod (Alican istedi).
        self._history_view = LessonView(self._language, compact=True)
        self._brief_stack.addWidget(self._history_view)
        # API 2: kişinin yazdığı API'ye istek gönderen panel.
        self._request_panel = RequestPanel(self._language)
        self._request_panel.send_requested.connect(self._send_request)
        self._brief_stack.addWidget(self._request_panel)
        layout.addWidget(self._brief_stack)

        return panel

    def _on_brief_tab(self, index: int) -> None:
        anahtar = self._tab_keys[index] if 0 <= index < len(self._tab_keys) else "prompt"
        self._tab_current = anahtar
        self._brief_stack.setCurrentIndex(PAGES[anahtar])

    def _update_tabs(self, focus: str | None = None) -> None:
        """Sol paneldeki sekmeleri durumdan kurar; `focus` verilirse ona geçer.

        Yönerge her zaman var. Problemde çözüm açılınca "Çözüm yolları", kod
        alıştırmasında grafik ya da tutmayan çok satırlı çıktı varsa "Çıktı",
        en az bir deneme kaydedildiyse "Denemelerim". Tek sekme kalırsa
        sekme şeridi gizleniyor.
        """
        ex = self._exercise
        anahtarlar = ["prompt"]
        if ex is not None:
            if ex.is_problem:
                if self._revealed_solution:
                    anahtarlar.append("solutions")
            elif ex.is_terminal:
                pass
            else:
                if self._is_api_app():
                    anahtarlar.append("request")
                if self._has_output:
                    anahtarlar.append("output")
            if self._attempt_count:
                anahtarlar.append("history")
        if focus in anahtarlar:
            self._tab_current = focus
        if self._tab_current not in anahtarlar:
            self._tab_current = "prompt"
        etiketler = [self._language.t(TAB_LABELS[k]) for k in anahtarlar]
        if anahtarlar != self._tab_keys:
            self._tab_keys = anahtarlar
            self._brief_tabs.set_items(etiketler)
        else:
            self._brief_tabs.set_labels(etiketler)
        self._brief_tabs_holder.setVisible(len(anahtarlar) > 1)
        self._brief_tabs.set_current(anahtarlar.index(self._tab_current), notify=False)
        self._brief_stack.setCurrentIndex(PAGES[self._tab_current])

    def _load_history(self) -> None:
        """Bu alıştırmanın denemelerini okuyup "Denemelerim" sayfasını çizer."""
        ex = self._exercise
        if ex is None:
            self._attempt_count = 0
            return
        denemeler = self._store.exercise_attempts(self._chapter_id, self._section_id, ex.id)
        self._attempt_count = len(denemeler)
        if denemeler:
            self._history_view.set_base_dir(ex.directory)
            self._history_view.show_text(
                exercise_markdown(self._language, denemeler, "bash" if ex.is_terminal else ex.language, ex.is_problem)
            )

    def _on_prompt_action(self, action: str) -> None:
        """Yönerge içindeki bağlantılar: ipucu kademeleri ve alttaki
        "devam" düğmesi."""
        if action == "advance":
            self.advance.emit()
            return
        # Açılan ipucu "Gizle" ile yeniden kapatılabiliyor; kutu uzayınca
        # kişi istediği kademeye dönebilsin.
        if action.startswith("hint-"):
            gizle = action.startswith("hint-hide-")
            try:
                level = int(action.rsplit("-", 1)[1])
            except ValueError:
                return
            if gizle:
                self._revealed.discard(level)
            else:
                self._revealed.add(level)
            self._prompt.update_extra(self._extra_html())
            return
        if action == "lesson-spot":
            spot = self._stuck_spot()
            self.lesson_requested.emit(spot.anchor if spot else "")
        elif action == "trace-solution":
            self.trace_solution()

    def set_advance_label(self, label: str | None) -> None:
        """Yönergenin en altındaki "devam" düğmesi.

        Ders ve not sayfalarının altında ileri düğmesi vardı, alıştırmada
        yoktu; bir alıştırmayı bitiren kişi sonrakine geçmek için sağ
        üstteki numaraları aramak zorunda kalıyordu. `None` verilirse
        düğme çizilmiyor (son alıştırmadayken sonraki bölüm kilitli).
        """
        self._advance_label = label
        self._prompt.set_footer(
            [("advance" if label else "", f"{label or ''}  →", True)]
        )

    def _hint_label(self, level: int) -> str:
        """Kapalı bir kademenin etiketi.

        Etiket kademenin **sırasına** göre seçiliyor, numarasına göre değil:
        dört ipuçlu bir alıştırmada üçüncü kademe "çözümün tamamı" değil,
        yalnızca sonuncusu öyle.
        """
        toplam = len(self._exercise.hints) if self._exercise else 0
        # Problemde çözüm ipuçlarda değil, çözüm yollarında; son ipucu da
        # yalnızca bir yönlendirme.
        if self._exercise is not None and self._exercise.is_problem:
            return "hint.level1" if level == 1 else "hint.level2"
        if level >= toplam:
            return "hint.level3"
        if level == 1:
            return "hint.level1"
        return "hint.level2"

    def _hints_html(self) -> str:
        """İpucu kutusunu maketteki yapıyla üretir.

        Kademeler kapalı başlar; kullanıcı istediği kadarını açar. Açılmış
        kademe metni markdown olarak çevriliyor, böylece içindeki kod
        blokları da renklendiriliyor.
        """
        if self._exercise is None or not self._exercise.hints:
            return ""

        rows = []
        for level, hint in enumerate(self._exercise.hints, start=1):
            text = self._language.pick(hint)
            if not text:
                continue

            if level in self._revealed:
                body, _ = render_markdown(text)
                inner = f'<div class="tx open">{body}</div>'
                button = (
                    f'<a class="show hide" href="app:hint-hide-{level}">'
                    f'{html.escape(self._language.t("hint.hide"))}</a>'
                )
            else:
                label = html.escape(self._language.t(self._hint_label(level)))
                inner = f'<div class="tx">{label}</div>'
                button = (
                    f'<a class="show" href="app:hint-{level}">'
                    f'{html.escape(self._language.t("hint.show"))}</a>'
                )

            rows.append(
                f'<div class="hint"><div class="lv">{level}</div>{inner}{button}</div>'
            )

        if not rows:
            return ""

        title = html.escape(self._language.t("hint.title"))
        return f'<div class="hintbox"><div class="hd">{title}</div>{"".join(rows)}</div>'

    def _chips_html(self) -> str:
        if self._exercise is None:
            return ""

        # Ölçek üç kademe; beklenmedik bir değer boş bir "Zorluk:" etiketi
        # bırakmasın, en yakın kademeye çekiliyor (içerik denetimi de bakıyor).
        difficulty = min(max(self._exercise.difficulty, 1), 3)
        tone = {1: "easy", 2: "mid", 3: "hard"}.get(difficulty, "")
        label = html.escape(
            f"{self._language.t('exercise.difficulty')}: "
            f"{DIFFICULTY_LABELS.get(difficulty, '')}"
        )
        return (
            f'<div class="chips"><span class="chip {tone}">{label}</span></div>'
        )

    def _refresh_prompt(self) -> None:
        """Yönergeyi başlık, etiket ve ipuçlarıyla birlikte yeniden çizer."""
        if self._exercise is None:
            return

        prompt = self._exercise.prompt_for(self._language.language)
        body = prompt.path.read_text(encoding="utf-8") if prompt and prompt.exists else ""
        title = self._language.pick(self._exercise.title)

        self._prompt.set_base_dir(self._exercise.directory)
        self._prompt.show_text(
            f"# {title}\n\n{self._chips_html()}\n\n{body}", extra=self._extra_html()
        )

    # --- takıldın mı? -------------------------------------------------------

    def _failures(self) -> int:
        """Son başarılı denemeden bu yana başarısız deneme sayısı.

        Kayıttaki denemeler (aynı kod + aynı sonuç bir kez yazılıyor) ile bu
        oturumda düşen çalıştırmaların büyüğü: aynı kodu üç kez çalıştıran
        da sayılsın.
        """
        if self._exercise is None:
            return 0
        kayit = failures_since_pass(
            self._store.exercise_attempts(self._chapter_id, self._section_id, self._exercise.id)
        )
        return max(kayit, self._session_fails)

    def _stuck_spot(self):
        """Alıştırmanın dayandığı ders başlığı (dil ve alıştırma başına bir kez)."""
        if self._exercise is None:
            return None
        anahtar = (self._exercise.id, self._language.language)
        if self._stuck_cache is not None and self._stuck_cache[:2] == anahtar:
            return self._stuck_cache[2]
        dil = self._language.language
        prompt = self._exercise.prompt_for(dil)
        metin = prompt.path.read_text(encoding="utf-8") if prompt and prompt.exists else ""
        if self._exercise.is_problem:
            kod = self._exercise.solution_text(0, dil)
        elif self._exercise.is_terminal:
            kod = "\n".join(self._exercise.solution_commands)
        elif self._exercise.is_multi_file:
            kod = "\n".join(self._exercise.solution_files(dil).values())
        else:
            kod = self._exercise.solution_code_for(dil) or ""
        spot = find_spot(self.lesson_source() or "", kod, metin,
                         override=str(self._exercise.raw.get("lesson_anchor", "")),
                         title=self._language.pick(self._exercise.title))
        self._stuck_cache = (*anahtar, spot)
        return spot

    def _stuck_html(self) -> str:
        """Üç başarısız denemeden sonra yönergenin altındaki kart."""
        if self._exercise is None or self._failures() < STUCK_AFTER:
            return ""
        spot = self._stuck_spot()
        if spot is None:
            return ""
        t = self._language.t
        baslik = spot.title.replace("`", "")
        metin = t("stuck.text", title=baslik) if baslik else t("stuck.text_start")
        return (
            '<div class="stuck"><div class="hd">'
            f'{html.escape(t("stuck.title"))}</div>'
            f'<p>{html.escape(metin)}</p>'
            f'<a class="go" href="app:lesson-spot">{html.escape(t("stuck.go"))}</a>'
            + (f'<a class="go alt" href="app:trace-solution">{html.escape(t("stuck.trace"))}</a>'
               if not self._exercise.is_problem and self._exercise.language == "python" else "")
            + "</div>"
        )

    def _extra_html(self) -> str:
        return self._stuck_html() + self._hints_html()

    # --- sağ: editör ve sonuçlar -----------------------------------------

    def _build_work(self) -> QWidget:
        """Sağ taraf: editör ve çalıştırma şeridi, altında terminal.

        İkisinin arasındaki ayırıcı sürüklenebiliyor (tutamağı görünür).
        Terminal her zaman duruyor; sonuç için ayrıca bir panel açılmıyor.
        """
        top = QWidget()
        top_layout = QVBoxLayout(top)
        # Prototip `.work`: editör ve terminal kenarlardan boşluklu kartlar.
        top_layout.setContentsMargins(8, 14, 18, 0)
        top_layout.setSpacing(0)

        # Editör kartı (prototip `.editor`): yuvarlak köşeli zemini kart
        # boyuyor; editör saydam ve köşelere taşmasın diye içeriden boşluklu.
        self._editor_card = QFrame()
        self._editor_card.setProperty("role", "editor-card")
        kart = QVBoxLayout(self._editor_card)
        kart.setContentsMargins(4, 6, 4, 6)
        kart.setSpacing(0)
        # Çok dosyalı alıştırmada üstte dosya sekmeleri, her dosyanın kendi
        # editörü (geri alma geçmişi dosya başına). Tek dosyada yalnızca ana
        # editör var ve sekmeler gizli.
        self._file_tabs = FileTabs()
        self._file_tabs.current_changed.connect(lambda name: self._show_file(name, focus=True))
        self._file_tabs.hide()
        kart.addWidget(self._file_tabs)
        self._editor_stack = QStackedWidget()
        self._editor_stack.setProperty("role", "bare")
        self._main_editor = self._new_editor()
        self._editor = self._main_editor
        self._editors: dict[str, CodeEditor] = {}
        self._editor_stack.addWidget(self._main_editor)
        kart.addWidget(self._editor_stack)
        for tus, adim in (("Ctrl+PgDown", 1), ("Ctrl+PgUp", -1)):
            kisayol = QShortcut(QKeySequence(tus), self)
            kisayol.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
            kisayol.activated.connect(lambda adim=adim: self._file_tabs.step(adim))
        self._editor_flash = EdgeFlash(self._editor_card, radius=16)
        top_layout.addWidget(self._editor_card, 1)
        top_layout.addWidget(self._build_runbar())

        self._terminal = TerminalView()
        # Adım adım izleme terminalin yerinde açılıyor (aynı yer, aynı renkler).
        self._trace = TracePanel()
        self._trace.step_changed.connect(self._on_trace_step)
        self._trace.closed.connect(self.close_trace)
        self._trace.source_requested.connect(self._on_trace_source)
        self._bottom_stack = QStackedWidget()
        self._bottom_stack.addWidget(self._terminal)
        self._bottom_stack.addWidget(self._trace)
        alt = QWidget()
        alt.setProperty("role", "bare")
        alt_layout = QVBoxLayout(alt)
        alt_layout.setContentsMargins(8, 0, 18, 14)
        alt_layout.addWidget(self._bottom_stack)

        self._work_splitter = GripSplitter(Qt.Orientation.Vertical)
        self._work_splitter.addWidget(top)
        self._work_splitter.addWidget(alt)
        self._work_splitter.setSizes([EDITOR_SHARE, TERMINAL_SHARE])
        self._work_splitter.setStretchFactor(0, 1)
        return self._work_splitter

    def _new_editor(self) -> CodeEditor:
        editor = CodeEditor(mode=self._mode)
        editor.setProperty("card", "true")
        editor.run_requested.connect(self.run)
        editor.edited.connect(lambda: self._on_editor_edited(editor))
        return editor

    def _on_editor_edited(self, editor: CodeEditor) -> None:
        # Kişi kendi kodunu değiştirince kayıt artık o koda ait değil; örnek
        # çözüm izlenirken ise yazmaya devam edebilir.
        if self._trace.source == "user":
            self.close_trace()
        if self._exercise is not None and self._exercise.is_multi_file and self._editors.get(self._file_tabs.current) is editor:
            self._file_tabs.set_error("")

    def _setup_editors(self, exercise: Exercise) -> None:
        """Alıştırmanın dosyaları için editörler; ilk dosya ana editörde."""
        for editor in self._editors.values():
            if editor is not self._main_editor:
                self._editor_stack.removeWidget(editor)
                editor.deleteLater()
        self._editors = {}
        files = exercise.files
        for index, item in enumerate(files):
            editor = self._main_editor if index == 0 else self._new_editor()
            if index:
                editor.set_mode(self._mode)
                self._editor_stack.addWidget(editor)
            editor.set_language(item.language)
            editor.setReadOnly(item.readonly)
            editor.set_error_line(None)
            editor.set_trace_line(None)
            self._editors[item.name] = editor
        self._file_tabs.set_files([(item.name, item.language, item.readonly) for item in files])
        self._file_tabs.setVisible(exercise.is_multi_file)
        self._editor = self._main_editor
        self._editor_stack.setCurrentWidget(self._main_editor)

    def _show_file(self, name: str, focus: bool = False) -> None:
        """Dosyanın editörünü öne getirir (sekme de seçiliyor)."""
        editor = self._editors.get(name)
        if editor is None:
            return
        self._file_tabs.blockSignals(True)
        self._file_tabs.set_current(name)
        self._file_tabs.blockSignals(False)
        self._editor = editor
        self._editor_stack.setCurrentWidget(editor)
        if focus:
            editor.setFocus()

    def _code_now(self) -> str | dict[str, str]:
        """Çalıştırılacak kod: tek dosyada metin, çok dosyada bütün dosyalar."""
        if self._exercise is not None and self._exercise.is_multi_file:
            return {name: editor.toPlainText() for name, editor in self._editors.items()}
        return self._main_editor.toPlainText()

    def _code_to_save(self) -> str:
        """Kayda giden metin; çok dosyada yalnızca düzenlenebilir dosyalar (JSON)."""
        if self._exercise is not None and self._exercise.is_multi_file:
            return workspace_files.encode({
                item.name: self._editors[item.name].toPlainText()
                for item in self._exercise.files
                if not item.readonly and item.name in self._editors
            })
        return self._main_editor.toPlainText()

    def _build_problem_work(self) -> QWidget:
        """Problemin sağ tarafı: çalışma kâğıdı ve cevap. Tamamı kâğıda ait;
        çözüm yolları sol panelde açılıyor."""
        self._problem = ProblemPanel(self._language)
        self._problem.checked.connect(self._on_problem_checked)
        self._problem.work_changed.connect(self._save_problem_state)
        self._problem.reveal_requested.connect(lambda: self._reveal_solutions(True))

        # Çözüm açık mı; kayıtta da tutuluyor, bölüme dönünce açık kalsın.
        self._revealed_solution = False
        return self._problem

    def _build_runbar(self) -> QWidget:
        bar = QFrame()
        bar.setProperty("role", "bare")

        # Prototip `.runrow`: solda tuş kutucukları (Ctrl + Enter), sağda düğmeler.
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(10)

        self._shortcut_hint = QWidget()
        self._shortcut_hint.setProperty("role", "bare")
        kisayol = QHBoxLayout(self._shortcut_hint)
        kisayol.setContentsMargins(0, 0, 0, 0)
        kisayol.setSpacing(4)
        for parca in ("Ctrl", "+", "Enter"):
            etiket = QLabel(parca)
            etiket.setProperty("role", "kbd" if parca != "+" else "muted")
            kisayol.addWidget(etiket, 0, Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self._shortcut_hint)
        layout.addStretch(1)

        # Yalnızca SQL alıştırmalarında görünüyor: Python alıştırmasında
        # gösterilecek bir tablo yok.
        self._tables_button = QPushButton()
        self._tables_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._tables_button.clicked.connect(self._show_tables)
        self._tables_button.hide()
        layout.addWidget(self._tables_button)

        self._reset_button = QPushButton()
        self._reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._reset_button.clicked.connect(self._reset)
        layout.addWidget(self._reset_button)

        # Adım adım: yalnızca Python alıştırmalarında (SQL'de satır satır
        # izlenecek bir program yok).
        self._trace_button = QPushButton()
        self._trace_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._trace_button.clicked.connect(self.start_trace)
        self._trace_spinner = ButtonSpinner(self._trace_button)
        layout.addWidget(self._trace_button)

        # API 2: uygulamayı gerçekten açıp tarayıcıda `/docs` göstermek.
        self._server_button = QPushButton()
        self._server_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._server_button.clicked.connect(self._toggle_server)
        self._server_spinner = ButtonSpinner(self._server_button)
        self._server_button.hide()
        layout.addWidget(self._server_button)

        self._run_button = QPushButton()
        self._run_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._run_button.setProperty("variant", "primary")
        self._run_button.clicked.connect(self.run)
        # Çalışırken düğmede dönen yay; sonuçta editörün çerçevesi yanıp söner (C6).
        self._run_spinner = ButtonSpinner(self._run_button)
        layout.addWidget(self._run_button)

        return bar

    # --- içerik -----------------------------------------------------------

    def code_for_note(self) -> tuple[str, str] | None:
        """Nota eklenecek kod ve dili: seçim varsa seçim, yoksa editörün tamamı.

        Dil etiketi markdown'ın tanıdığı ad: T-SQL alıştırması `sql`.
        """
        if self._exercise is None or self._exercise.is_problem:
            return None
        if self._exercise.is_terminal:
            komutlar = [c for c in self._git.commands if c.strip()]
            return ("\n".join(komutlar), "bash") if komutlar else None
        cursor = self._editor.textCursor()
        if cursor.hasSelection():
            code = cursor.selectedText().replace(" ", "\n")
        else:
            code = self._editor.toPlainText()
        if not code.strip():
            return None
        dil = self._editor._code_language()  # noqa: SLF001
        return code, NOTE_TAGS.get(dil, dil)

    @property
    def current_exercise_id(self) -> str:
        """Açık alıştırmanın kimliği (yoksa boş); hata bildiriminde kullanılıyor."""
        return self._exercise.id if getattr(self, "_exercise", None) is not None else ""

    def show_exercise(self, exercise: Exercise, chapter_id: str, section_id: str) -> None:
        """Alıştırmayı yükler ve varsa daha önce yazılan kodu geri getirir."""
        self._exercise = exercise
        self._chapter_id = chapter_id
        self._section_id = section_id

        # Yeni alıştırmada ipuçları kapalı başlar.
        self._revealed = set()
        self._session_fails = 0
        self._stuck_announced = False
        self._refresh_prompt()

        if exercise.is_problem:
            state = problem_state(self._store.exercise_code(chapter_id, section_id, exercise.id))
            self._problem.show_problem(
                exercise.answers, state["answers"], state["drawing"], exercise.symbols
            )
            # Yeni problem her zaman yönergeyle açılıyor; önceki problemin
            # çözüm sekmesi açık kalırsa kişi yanlış problemin çözümünü görür.
            # Bu problemin çözümü daha önce açıldıysa sekmesi hazır bekliyor.
            self._revealed_solution = False
            self._tab_current = "prompt"
            self._load_history()
            self._reveal_solutions(state["revealed"], save=False, focus=False)
            self._work_stack.setCurrentIndex(1)
            self.retranslate()
            return
        if exercise.is_terminal:
            self.stop_server()
            self.close_trace()
            self._revealed_solution = False
            self._tab_current = "prompt"
            self._load_history()
            self._git.show_exercise(exercise, self._store.exercise_code(chapter_id, section_id, exercise.id))
            self._work_stack.setCurrentIndex(2)
            self.retranslate()
            self._git.focus()
            return
        self._work_stack.setCurrentIndex(0)
        self._revealed_solution = False
        self._tab_current = "prompt"
        self._load_history()

        # Kaydedilen kod hâlâ başlangıç kodunun kendisiyse (kullanıcı bir
        # şey yazmadan çalıştırmış) o kayda tutunmuyoruz: dili şimdiki dile
        # göre seçiyoruz. Yazılmış bir kod varsa dokunulmuyor.
        saved = self._store.exercise_code(chapter_id, section_id, exercise.id)
        self._setup_editors(exercise)
        dil = self._language.language
        if exercise.is_multi_file:
            # Alıştırma sonradan çok dosyalı olduysa eski kayıt düz kod:
            # giriş dosyasına konuyor.
            kayit = workspace_files.decode(saved)
            if kayit is None:
                kayit = {exercise.entry: saved} if saved else {}
            for item in exercise.files:
                metin = kayit.get(item.name)
                if item.readonly or metin is None or item.is_untouched(metin):
                    metin = item.starter_for(dil)
                self._editors[item.name].setPlainText(metin)
        else:
            if saved and exercise.is_untouched(saved):
                saved = ""
            self._editor.setPlainText(saved or exercise.starter_code_for(dil))

        # Tablolar önceki alıştırmanın verisini göstermesin.
        self._tables = []
        self._tables_button.setVisible(exercise.language == "tsql")
        # Adım adım izleme yalnızca Python'da (SQL ve Docker'da satır yok).
        self._trace_button.setVisible(exercise.language == "python")
        # API 2: önceki alıştırmanın sunucusu kapanıyor, istek paneli sıfırlanıyor.
        self.stop_server()
        self._server_button.setVisible(self._is_api_app())
        self._request_panel.reset(self._first_path())
        self.close_trace()
        if self._tables_window is not None:
            self._tables_window.set_tables(
                [], self._language.t("tables.not_run")
            )

        self._clear_results()
        self.retranslate()

    # --- API 2: istek paneli ve sunucu ---------------------------------------

    def _is_api_app(self) -> bool:
        ex = self._exercise
        return ex is not None and not ex.is_problem and any(c.get("type") == "http" for c in ex.checks)

    def _first_path(self) -> str:
        """İstek panelinin başlangıç adresi: alıştırmanın ilk denediği yol."""
        for check in (self._exercise.checks if self._exercise else []):
            if check.get("type") == "http" and check.get("steps"):
                yol = str(check["steps"][0].get("path", "/"))
                return yol if "{" not in yol else "/"
        return "/"

    def _code_files(self) -> dict:
        """Sunucu için dosyalar: tek dosyalıda giriş dosyasının adıyla."""
        kod = self._code_now()
        if isinstance(kod, dict):
            return kod
        return {self._exercise.entry or "main.py": kod}

    def _send_request(self, method: str, path: str, body) -> None:
        if self._exercise is None or not self._is_api_app():
            return
        if self._request_worker is not None and self._request_worker.isRunning():
            return
        adim = {"method": method, "path": path}
        if body is not None:
            adim["json"] = body
        self._request_worker = RequestWorker(self._code_now(), self._exercise, adim, self)
        self._request_worker.completed.connect(self._on_request_done)
        self._request_worker.start()

    def _on_request_done(self, result: RunResult) -> None:
        t = self._language.t
        if result.status == "timeout":
            self._request_panel.show_error(t("request.timeout"))
            return
        if result.checks and result.checks[0].passed:
            values = result.checks[0].detail.get("values", {})
            self._request_panel.show_response(int(values.get("status", 0)), str(values.get("body", "")))
            return
        if result.checks:
            detay = result.checks[0].detail or {}
            degerler = detay.get("values", {})
            if detay.get("reason") in ("server_error", "server_error_at"):
                # Panelde adım yok, tek istek var: "1. adımda" yazılmıyor.
                yer = (t("request.where", file=degerler.get("file", ""), line=degerler.get("line", 0))
                       if degerler.get("file") else "")
                self._request_panel.show_error(t("request.server_error", error=degerler.get("error", ""))
                                               + yer)
                return
            self._request_panel.show_error(describe(result, self._language)[0].message)
            return
        hata = result.error or {}
        self._request_panel.show_error(f"{hata.get('type', '')}: {hata.get('message', '')}".strip(": "))

    def _toggle_server(self) -> None:
        if self._server is not None:
            self.stop_server()
            self._terminal.begin(line("❯ Ctrl+C", "prompt", bold=True), "")
            self._terminal.finish(line(self._language.t("server.stopped"), "dim"))
            return
        if self._exercise is None or (self._server_worker is not None and self._server_worker.isRunning()):
            return
        self._server_spinner.start()
        self._server_button.setText("  " + self._language.t("server.starting"))
        modul = Path(self._exercise.entry or "main.py").stem
        self._terminal.begin(line(f"❯ uvicorn {modul}:app", "prompt", bold=True),
                             line(self._language.t("server.starting"), "dim"))
        self._server_worker = ServerWorker(self._code_files(), self._exercise, self)
        self._server_worker.completed.connect(self._on_server_ready)
        self._server_worker.start()

    def _on_server_ready(self, server, ok: bool) -> None:
        self._server_spinner.stop()
        t = self._language.t
        if server is None or not ok:
            gunluk = server.log_tail() if server is not None else ""
            if server is not None:
                server.stop()
            satirlar = [line(t("server.failed"), "fail", bold=True)]
            for metin in gunluk.strip().splitlines()[-12:]:
                satirlar.append(line(metin, "fail", indent=2))
            self._terminal.finish("".join(satirlar))
            self._retranslate_server()
            return
        self._server = server
        adres = f"{server.url}/docs"
        self._terminal.finish(
            line(t("server.running", url=server.url), "ok", bold=True)
            + line(t("server.docs", url=adres), "dim", indent=2)
            + line(t("server.reload_note"), "dim", indent=2)
        )
        self._retranslate_server()
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices

        QDesktopServices.openUrl(QUrl(adres))

    def stop_server(self) -> None:
        """Açık sunucuyu kapatır (alıştırma değişince, düğmeyle, ekran kapanınca)."""
        if self._server is not None:
            self._server.stop()
            self._server = None
        self._retranslate_server()

    def _retranslate_server(self) -> None:
        anahtar = "server.stop" if self._server is not None else "server.start"
        self._server_button.setText("  " + self._language.t(anahtar))
        p = PALETTES.get(self._mode, PALETTES["light"])
        self._server_button.setIcon(icon("x" if self._server is not None else "globe", p["text"], 16))

    def _show_tables(self) -> None:
        """Tablolar penceresini açar; veri yoksa önce anlık görüntü alır."""
        if self._exercise is None:
            return

        if self._tables_window is None:
            self._tables_window = TablesWindow(
                self._language, self, self._mode
            )
        pencere = self._tables_window
        pencere.set_tables(self._tables, "" if self._tables else
                           self._language.t("tables.loading"))
        pencere.show()
        pencere.raise_()
        pencere.activateWindow()

        # Henüz çalıştırılmamışsa hazır verinin hâlini getiriyoruz:
        # sorguyu yazmadan önce "elimde ne var" sorusunun cevabı gerekiyor.
        if not self._tables and (
            self._snapshot is None or not self._snapshot.isRunning()
        ):
            self._snapshot = SnapshotWorker(self._exercise, self)
            self._snapshot.completed.connect(self._on_snapshot)
            self._snapshot.start()

    def _on_snapshot(self, result) -> None:
        self._tables = result.tables
        if self._tables_window is None:
            return
        if result.tables:
            self._tables_window.set_tables(result.tables)
        else:
            hata = (result.error or {}).get("message", "")
            self._tables_window.set_tables([], hata or self._language.t("tables.empty"))

    def _clear_results(self) -> None:
        """Yeni alıştırma: terminal karşılamaya döner, Çıktı sekmesi kapanır."""
        self._terminal.set_welcome(self._welcome_html())
        self._terminal.clear()
        self._set_output(False)

    # --- terminal ----------------------------------------------------------

    def _runtime_name(self) -> str:
        dil = self._exercise.language if self._exercise is not None else "python"
        return {"tsql": "SQL Server", "docker": "Docker"}.get(dil, "Python")

    def _command_name(self) -> str:
        if self._exercise is not None and self._exercise.language == "tsql":
            return "sqlcmd -i sorgu.sql"
        if self._exercise is not None and self._exercise.language == "docker":
            # Odyssey'nin denetimi; Docker'ın kendi komutları (build, run)
            # çıktının içinde ayrı satırlar olarak geliyor.
            return "odyssey check"
        if self._exercise is not None and self._exercise.is_multi_file:
            return f"python {self._exercise.entry}"
        return "python cozum.py"

    def _welcome_html(self) -> str:
        t = self._language.t
        satirlar = [line(f"Odyssey v{APP_VERSION} · {self._runtime_name()}", "accent", bold=True)]
        if self._exercise is not None:
            satirlar.append(
                line(t("terminal.ready", title=self._language.pick(self._exercise.title)), "dim")
            )
        return "".join(satirlar)

    def _prose(self, text: str, color: str, prefix: str = "", indent: int = 0) -> str:
        """Düz yazıyı terminal genişliğinde satırlara böler (satırlar kaymıyor)."""
        sarilmis = textwrap.wrap(text, PROSE_WIDTH - indent - len(prefix)) or [""]
        parcalar = []
        for index, satir in enumerate(sarilmis):
            on = prefix if index == 0 else " " * len(prefix)
            parcalar.append(line(on + satir, color, indent=indent))
        return "".join(parcalar)

    def _terminal_body(self, result: RunResult, seconds: float, has_output: bool) -> str:
        """Bir çalıştırmanın terminaldeki gövdesi: çıktı, ayraç, sonuç."""
        t = self._language.t
        parcalar = []
        if result.stdout.strip():
            parcalar.append(block(result.stdout.rstrip("\n")))
        if result.stderr.strip():
            parcalar.append(block(result.stderr.rstrip("\n"), "fail"))
        if result.truncated:
            parcalar.append(line(f"[{t('exercise.output_truncated')}]", "dim"))
        parcalar.extend(self._request_lines(result.requests))
        docker = result.docker.get("state", "")
        if docker in ("missing", "stopped"):
            parcalar.append(self._prose(t(f"terminal.docker_{docker}"), "warn", prefix="🐳 "))
        elif not (result.stdout.strip() or result.stderr.strip()):
            parcalar.append(line(t("terminal.no_output"), "dim"))

        parcalar.append(line("─" * 44, "dim"))
        gecti = result.passed
        parcalar.append(self._prose(
            summarise(result, self._language), "ok" if gecti else "fail",
            prefix="✓ " if gecti else "✕ ",
        ))

        explanation = explain(result.error)
        if explanation is not None:
            parcalar.append(self._prose(
                t(explanation.key, **explanation.values), "warn", prefix="💡 "
            ))

        for feedback in describe(result, self._language):
            if feedback.passed:
                continue
            parcalar.append(self._prose(feedback.message, "fail", prefix="✕ "))
            if feedback.has_comparison:
                parcalar.append(line(f"{t('check.stdout.expected')}:", "dim", indent=2))
                parcalar.append(block(feedback.expected or "—", "warn", indent=4))
                parcalar.append(line(f"{t('check.stdout.actual')}:", "dim", indent=2))
                parcalar.append(block(feedback.actual or "—", "text", indent=4))

        if result.artifacts:
            parcalar.append(line(
                "📊 " + t("terminal.artifacts", count=len(result.artifacts)), "accent"
            ))
        if has_output:
            parcalar.append(line("→ " + t("terminal.see_output"), "accent"))
        sure = f"{seconds:.1f}"
        if self._language.language == "tr":
            sure = sure.replace(".", ",")
        parcalar.append(line(t("terminal.took", seconds=sure), "dim"))
        return "".join(parcalar)

    def _request_lines(self, requests: list[dict]) -> list[str]:
        """API alıştırmasında sunucuya giden istekler: `→ GET /books?page=2  200`."""
        if not requests:
            return []
        from urllib.parse import urlencode

        satirlar = [line(self._language.t("terminal.requests", count=len(requests)), "dim")]
        for istek in requests[:REQUEST_LINES]:
            sorgu = urlencode(istek.get("query") or {})
            hedef = istek.get("path", "") + (f"?{sorgu}" if sorgu else "")
            durum = int(istek.get("status", 0))
            renk = "ok" if durum < 300 else "warn" if durum < 500 and durum != 404 else "fail"
            satirlar.append(line(f"→ {istek.get('method', '')} {hedef}  {durum}", renk, indent=2))
        if len(requests) > REQUEST_LINES:
            satirlar.append(line(f"… +{len(requests) - REQUEST_LINES}", "dim", indent=2))
        return satirlar

    # --- sol: Çıktı sekmesi ------------------------------------------------

    def _output_markdown(self, result: RunResult) -> str:
        """Grafikler ve tutmayan çok satırlı çıktılar; yoksa boş metin."""
        t = self._language.t
        parcalar = []
        damga = int(time.time() * 1000)
        if result.artifacts:
            parcalar.append(f"## {t('output.produced')}")
            for yol in result.artifacts:
                # Aynı adlı dosya her çalıştırmada yeniden yazılıyor; sorgu
                # eki olmadan tarayıcı eski grafiği önbellekten gösteriyordu.
                kaynak = f"{yol.as_uri()}?v={damga}"
                parcalar.append(
                    f'<figure class="fig"><img class="out" src="{html.escape(kaynak)}" alt="">'
                    f"<figcaption>{html.escape(yol.name)}</figcaption></figure>"
                )

        karsilastirmalar = [
            f for f in describe(result, self._language)
            if not f.passed and f.has_comparison
            and ("\n" in (f.expected or "") or "\n" in (f.actual or ""))
        ]
        if karsilastirmalar:
            parcalar.append(f"## {t('output.compare')}")
            parcalar.append(t("output.compare_intro"))
            for feedback in karsilastirmalar:
                beklenen = (feedback.expected or "").splitlines()
                gelen = (feedback.actual or "").splitlines()
                parcalar.append(f"**{html.escape(feedback.message)}**")
                parcalar.append(
                    f'<div class="out-label">{html.escape(t("check.stdout.expected"))}</div>'
                    + _cmp_html(beklenen, beklenen)
                )
                parcalar.append(
                    f'<div class="out-label">{html.escape(t("check.stdout.actual"))}</div>'
                    + _cmp_html(gelen, beklenen, mark=True)
                )
        if not parcalar:
            return ""
        return f"# {t('output.title')}\n\n" + "\n\n".join(parcalar)

    def _set_output(self, visible: bool, focus: bool = False) -> None:
        """Kod alıştırmasında "Yönerge | Çıktı" sekmelerini açar ya da kapatır."""
        self._has_output = visible
        self._update_tabs("output" if visible and focus else None)

    # --- çalıştırma -------------------------------------------------------

    def _fix_run_width(self) -> None:
        """Çalıştır düğmesi iki metnin (çalıştır / çalışıyor) genişini alır."""
        b = self._run_button
        eski = b.text()
        genis = 0
        for metin in ("exercise.run", "exercise.running"):
            b.setText("  " + self._language.t(metin))
            genis = max(genis, b.sizeHint().width())
        b.setText(eski)
        b.setMinimumWidth(genis)

    def run(self) -> None:
        if self._exercise is not None and self._exercise.is_problem:
            # Ctrl+Enter problemde cevabı denetliyor.
            self._problem.check()
            return
        if self._exercise is None or (self._worker and self._worker.isRunning()):
            return

        # Düğme devre dışı bırakılmıyor (gri zeminde dönen yay görünmüyordu);
        # ikinci çalıştırmayı yukarıdaki işçi denetimi engelliyor.
        self._run_button.setText("  " + self._language.t("exercise.running"))
        self._run_spinner.start()
        # Terminalde önceki çalıştırmalar yukarıda kalıyor; yenisi altına.
        self._terminal.begin(
            line(f"❯ {self._command_name()}", "prompt", bold=True),
            line(self._language.t("terminal.running"), "dim"),
        )
        self._run_started = time.monotonic()

        self._worker = RunWorker(self._code_now(), self._exercise, self)
        self._worker.completed.connect(self._on_completed)
        self._worker.start()

    def _on_completed(self, result: RunResult) -> None:
        self._run_spinner.stop()
        self._run_button.setEnabled(True)
        self._run_button.setText("  " + self._language.t("exercise.run"))
        p = PALETTES.get(self._mode, PALETTES["light"])
        self._editor_flash.flash(p["success"] if result.passed else p["danger"])
        # Hata veren satır editörde işaretleniyor (SQL'de satır bilgisi yok).
        # Çok dosyalı alıştırmada hatanın dosyası öne geliyor, sekmesinde nokta.
        hata = (result.error or {}) if result.status == "error" else {}
        satir = hata.get("line") if isinstance(hata.get("line"), int) else None
        for editor in self._editors.values():
            editor.set_error_line(None)
        if self._exercise is not None and self._exercise.is_multi_file:
            dosya = str(hata.get("file") or self._exercise.entry) if satir else ""
            self._file_tabs.set_error(dosya)
            if dosya in self._editors:
                self._show_file(dosya)
                self._editors[dosya].set_error_line(satir)
        else:
            self._editor.set_error_line(satir)

        if self._exercise is not None:
            self._store.save_exercise(
                self._chapter_id,
                self._section_id,
                self._exercise.id,
                self._code_to_save(),
                solved=result.passed,
                count_attempt=True,
            )
            self._store.add_exercise_attempt(
                self._chapter_id,
                self._section_id,
                self._exercise.id,
                self._code_to_save(),
                result.passed,
                run_detail(result),
            )
            self._load_history()
            self._session_fails = 0 if result.passed else self._session_fails + 1
            self._prompt.update_extra(self._extra_html())
        # Kart bu alıştırmada ilk kez çıktıysa yönerge öne geliyor ve terminal
        # oraya işaret ediyor; yoksa "Çıktı" sekmesinin arkasında kalıyordu.
        yeni_kart = (not result.passed and not self._stuck_announced
                     and self._failures() >= STUCK_AFTER and self._stuck_spot() is not None)
        if yeni_kart:
            self._stuck_announced = True

        # Grafikler ve tutmayan çok satırlı çıktılar sol paneldeki "Çıktı"
        # sekmesinde, tam genişlikte; terminal kısa bir işaret bırakıyor.
        cikti = self._output_markdown(result)
        if cikti:
            self._output_view.set_base_dir(self._exercise.directory if self._exercise else None)
            self._output_view.show_text(cikti)
        self._set_output(bool(cikti), focus=bool(cikti) and not yeni_kart)
        if yeni_kart:
            self._update_tabs("prompt")

        sure = time.monotonic() - self._run_started if self._run_started else 0.0
        govde = self._terminal_body(result, sure, bool(cikti))
        if yeni_kart:
            govde += self._prose(self._language.t("stuck.terminal"), "accent", prefix="💡 ")
        self._terminal.finish(govde)

        # Tablolar penceresi açıksa çalıştırmanın bıraktığı hâli gösteriyor.
        if result.tables:
            self._tables = result.tables
            if self._tables_window is not None:
                self._tables_window.set_tables(result.tables)

        if result.passed and self._exercise is not None:
            self.solved.emit(self._exercise.id)

    # --- adım adım izleme -----------------------------------------------------

    @property
    def tracing(self) -> bool:
        return self._bottom_stack.currentWidget() is self._trace

    def start_trace(self, source: str = "user") -> None:
        """Kodu izleyerek çalıştırır; bitince panel terminalin yerinde açılır.

        `source` "solution" ise alıştırmanın örnek çözümü izleniyor (onay
        `_on_trace_source` / `trace_solution`'da).
        """
        if self._exercise is None or self._exercise.is_problem or self._exercise.language != "python":
            return
        if (self._worker and self._worker.isRunning()) or (
            self._trace_worker and self._trace_worker.isRunning()
        ):
            return
        if source == "solution":
            dil = self._language.language
            kod = (self._exercise.solution_files(dil) if self._exercise.is_multi_file
                   else self._exercise.solution_code_for(dil) or "")
        else:
            kod = self._code_now()
        self._trace_source = source
        self._trace_code = kod
        self._trace_spinner.start()
        self._trace_started = time.monotonic()
        self._trace_worker = TraceWorker(kod, self._exercise, self)
        self._trace_worker.completed.connect(self._on_traced)
        self._trace_worker.start()

    def _on_trace_source(self, source: str) -> None:
        if source == "solution":
            self.trace_solution()
        else:
            self.start_trace("user")

    def trace_solution(self) -> None:
        """Örnek çözümü adım adım oynatır; çözümü gösterdiği için ilk seferde sorar.

        Son ipucu (çözümün tamamı) zaten açıldıysa ya da bu alıştırmada bir
        kez onaylandıysa sorulmuyor.
        """
        if self._exercise is None:
            return
        son_ipucu = len(self._exercise.hints)
        onayli = self._exercise.id in self._solution_confirmed or (son_ipucu and son_ipucu in self._revealed)
        if not onayli:
            if not self._confirm_solution():
                return
            self._solution_confirmed.add(self._exercise.id)
        self.start_trace("solution")

    def _confirm_solution(self) -> bool:
        from . import titlebar
        from .confirm_dialog import ConfirmDialog
        from .modal import Backdrop

        t = self._language.t
        pencere = self.window()
        perde = Backdrop(pencere)
        perde.show()
        dialog = ConfirmDialog(t("trace.solution_confirm_title"), t("trace.solution_confirm_text"),
                               t("trace.solution_confirm"), t("common.cancel"), pencere)
        titlebar.apply(dialog, self._mode)
        self.confirm_dialog = dialog
        kabul = dialog.exec() == ConfirmDialog.DialogCode.Accepted
        self.confirm_dialog = None
        perde.deleteLater()
        return kabul

    def _on_traced(self, result: RunResult) -> None:
        self._trace_spinner.stop()
        if result.status not in ("ok", "error"):
            # Zaman aşımı, bellek, çökme: izlenecek bir kayıt yok; terminal
            # sebebini normal çalıştırmadaki gibi anlatıyor.
            self.close_trace()
            self._terminal.begin(line(f"❯ {self._command_name()}", "prompt", bold=True), "")
            self._terminal.finish(
                line(self._language.t("trace.failed"), "fail")
                + line("")
                + self._terminal_body(result, time.monotonic() - self._trace_started, False)
            )
            return
        for editor in self._editors.values():
            editor.set_error_line(None)
        self._file_tabs.set_error("")
        self._trace.retranslate(self._language.t)
        # Değişkenler ve çıktı sığsın: alt alan en az %45 (örnek çözümde
        # kod sütunu da var, %58); kapanınca eski boy.
        boylar = self._work_splitter.sizes()
        if not self.tracing:
            self._sizes_before_trace = boylar
        toplam = sum(boylar)
        pay = 0.58 if self._trace_source == "solution" else 0.45
        if toplam and boylar[1] < toplam * pay:
            ust = int(toplam * (1 - pay))
            self._work_splitter.setSizes([ust, toplam - ust])
        self._bottom_stack.setCurrentWidget(self._trace)
        aciklama = explain(result.error)
        ipucu = self._language.t(aciklama.key, **aciklama.values) if aciklama is not None else ""
        self._trace.load(result.steps, result.stdout, result.error, result.steps_truncated, ipucu,
                         source=self._trace_source, code=self._trace_code)
        self._trace.setFocus()

    def _on_trace_step(self, satir, kind: str, dosya: str = "") -> None:
        # Çok dosyalı alıştırmada adımın dosyası öne geliyor; odak panelde
        # kalıyor (oklarla ilerlemeye devam edilsin).
        if dosya and dosya in self._editors and dosya != self._file_tabs.current:
            self._show_file(dosya)
        for editor in self._editors.values():
            editor.set_trace_line(satir if editor is self._editor else None, kind or "line")

    def close_trace(self) -> None:
        """Paneli kapatır, editördeki işareti kaldırır."""
        if not hasattr(self, "_bottom_stack") or not self.tracing:
            return
        self._bottom_stack.setCurrentWidget(self._terminal)
        for editor in self._editors.values():
            editor.set_trace_line(None)
        if self._sizes_before_trace:
            self._work_splitter.setSizes(self._sizes_before_trace)
            self._sizes_before_trace = None

    def _on_problem_checked(self, answers: list, passed: bool) -> None:
        """Cevap denetlendi: kaydet, gerekiyorsa çözümü aç, çözüldüyse haber ver.

        Çözüm yolları kendiliğinden iki durumda açılıyor: problem çözüldüğünde
        (kişi kendi yolunu başka yollarla karşılaştırsın) ve iki yanlış
        denemeden sonra (takılan kişi nerede ayrıldığını görsün).
        """
        if self._exercise is None:
            return
        self._save_problem_state(solved=passed, count_attempt=True)
        self._store.add_exercise_attempt(
            self._chapter_id, self._section_id, self._exercise.id,
            json.dumps([str(a) for a in answers], ensure_ascii=False), passed,
        )
        self._load_history()
        self._update_tabs()
        self._session_fails = 0 if passed else self._session_fails + 1
        self._prompt.update_extra(self._extra_html())
        attempts = self._store.attempts(self._chapter_id, self._section_id, self._exercise.id)
        if passed or attempts >= REVEAL_AFTER_ATTEMPTS:
            self._reveal_solutions(True)
        if passed:
            self.solved.emit(self._exercise.id)

    def _on_git_changed(self, code: str, passed: bool, failed: bool) -> None:
        """Terminalde bir komut çalıştı: komut listesi kayda, hata sayacına."""
        if self._exercise is None or not self._exercise.is_terminal:
            return
        self._store.save_exercise(self._chapter_id, self._section_id, self._exercise.id, code)
        if not self._git_study_marked and saved_commands(code):
            # Komut yazmak çalışma sayılıyor (seri); günde bir kez yeter.
            self._store.mark_study_day()
            self._git_study_marked = True
        if failed:
            self._session_fails += 1
            if self._session_fails == STUCK_AFTER:
                self._prompt.update_extra(self._extra_html())

    def _on_git_solved(self, exercise_id: str) -> None:
        """Hedeflerin hepsi tuttu: çözüldü olarak kaydet, deneme listesine yaz."""
        if self._exercise is None or self._exercise.id != exercise_id:
            return
        komutlar = "\n".join(c for c in self._git.commands if c.strip())
        self._store.save_exercise(self._chapter_id, self._section_id, exercise_id,
                                  self._store.exercise_code(self._chapter_id, self._section_id, exercise_id),
                                  solved=True, count_attempt=True)
        self._store.add_exercise_attempt(self._chapter_id, self._section_id, exercise_id, komutlar, True)
        self._session_fails = 0
        self._load_history()
        self._update_tabs()
        self._prompt.update_extra(self._extra_html())
        self.solved.emit(exercise_id)

    def _save_problem_state(self, solved: bool | None = None, count_attempt: bool = False) -> None:
        """Cevaplar, çalışma alanı ve çözümün açık olup olmadığı tek kayıtta.

        Kod alıştırmasının `code` sütununa JSON olarak yazılıyor; ilerleme ve
        rozet hesabı iki türü ayırt etmiyor.
        """
        if self._exercise is None or not self._exercise.is_problem:
            return
        state = {
            "answers": self._problem.answers(),
            "drawing": self._problem.drawing(),
            "revealed": self._revealed_solution,
        }
        self._store.save_exercise(
            self._chapter_id,
            self._section_id,
            self._exercise.id,
            json.dumps(state, ensure_ascii=False),
            solved=solved,
            count_attempt=count_attempt,
        )

    def _reveal_solutions(self, revealed: bool, save: bool = True, focus: bool = True) -> None:
        """Çözüm yollarını sol panelde açar (ya da kapatır).

        Yeni açıldığında doğrudan çözüm sekmesine geçiliyor; bölüme geri
        dönüşte (`focus=False`) yönerge önde kalıyor.
        """
        was_open = self._revealed_solution
        self._revealed_solution = revealed
        self._problem.set_revealed(revealed)
        if revealed:
            self._render_solutions()
        self._update_tabs("solutions" if revealed and focus and not was_open else None)
        if save:
            self._save_problem_state()

    def _render_solutions(self) -> None:
        """Çözüm yolları; birden fazlaysa hepsi, sırayla."""
        if self._exercise is None:
            return
        t = self._language.t
        language = self._language.language

        parts = [
            f"# {t('problem.solutions_title')}",
            t("problem.compare_intro"),
        ]
        solutions = self._exercise.solutions
        for index, solution in enumerate(solutions, start=1):
            title = self._language.pick(solution.get("title"))
            if len(solutions) > 1:
                heading = t("problem.path", number=index, title=title)
            else:
                heading = title or t("problem.solution")
            parts.append(f"## {heading}")
            parts.append(self._exercise.solution_text(index - 1, language))

        self._solutions.set_base_dir(self._exercise.directory)
        self._solutions.show_text("\n\n".join(parts))

    def _reset(self) -> None:
        if self._exercise is None:
            return
        # Terminal silinmiyor: önceki çalıştırmaların çıktısı yol gösterebilir.
        if self._exercise.is_multi_file:
            for item in self._exercise.files:
                if not item.readonly and item.name in self._editors:
                    self._editors[item.name].setPlainText(item.starter_for(self._language.language))
            self._file_tabs.set_error("")
            return
        self._editor.setPlainText(
            self._exercise.starter_code_for(self._language.language)
        )

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        # Simge baştan var: dönen yay onun yerine geçiyor, düğme genişlemiyor.
        p = PALETTES.get(mode, PALETTES["light"])
        if self._run_spinner._saved_icon is None:  # noqa: SLF001
            self._run_button.setIcon(icon("play", "#FFFFFF", 16))
        self._reset_button.setIcon(icon("refresh", p["text"], 16))
        if self._trace_spinner._saved_icon is None:  # noqa: SLF001
            self._trace_button.setIcon(icon("steps", p["text"], 16))
        for editor in {self._main_editor, *self._editors.values()}:
            editor.set_mode(mode)
        self._file_tabs.set_mode(mode)
        self._prompt.set_mode(mode)
        self._solutions.set_mode(mode)
        self._output_view.set_mode(mode)
        self._history_view.set_mode(mode)
        self._request_panel.set_mode(mode)
        self._retranslate_server()
        self._problem.set_mode(mode)
        self._splitter.set_mode(mode)
        self._work_splitter.set_mode(mode)
        if self._tables_window is not None:
            self._tables_window.set_mode(mode)

    def retranslate(self) -> None:
        self._run_button.setText("  " + self._language.t("exercise.run"))
        self._reset_button.setText("  " + self._language.t("exercise.reset"))
        self._trace_button.setText("  " + self._language.t("trace.button"))
        self._retranslate_server()
        self._server_button.setToolTip(self._language.t("server.tip"))
        self._request_panel.retranslate()
        self._trace_button.setToolTip(self._language.t("trace.button_tip"))
        self._trace.retranslate(self._language.t)
        self._fix_run_width()
        self._tables_button.setText(self._language.t("tables.button"))
        self._file_tabs.set_texts(self._language.t("files.readonly"), self._language.t("files.error_here"))
        if self._tables_window is not None:
            self._tables_window.retranslate()

        # Başlık, etiketler ve ipuçları belgenin içinde olduğu için dil
        # değişince yönergeyi baştan çizmek yeterli.
        self._problem.retranslate()
        self._git.retranslate()
        self._update_tabs()
        if self._attempt_count:
            self._load_history()
        self._terminal.set_title(self._language.t("terminal.title"))
        self._terminal.clear_button.setText(self._language.t("terminal.clear"))
        self._terminal.set_welcome(self._welcome_html())
        if self._exercise is not None and self._exercise.is_problem and self._revealed_solution:
            self._render_solutions()
        if self._exercise is not None:
            self._refresh_prompt()
            if not self._exercise.is_problem and not self._exercise.is_terminal:
                self._sync_starter_language()

    def _sync_starter_language(self) -> None:
        """Başlangıç kodunun yorum satırlarını şimdiki dile çevirir.

        Yalnızca kullanıcı koda dokunmadıysa yapılıyor. Yazılmış bir kod
        varsa yerinde bırakılıyor: dil değiştirmek kimsenin yazdığını
        silmemeli.
        """
        if self._exercise is None:
            return

        if self._exercise.is_multi_file:
            for item in self._exercise.files:
                editor = self._editors.get(item.name)
                if editor is None or (not item.readonly and not item.is_untouched(editor.toPlainText())):
                    continue
                wanted = item.starter_for(self._language.language)
                if wanted.strip() != editor.toPlainText().strip():
                    editor.setPlainText(wanted)
            return

        current = self._editor.toPlainText()
        if not self._exercise.is_untouched(current):
            return

        wanted = self._exercise.starter_code_for(self._language.language)
        if wanted.strip() != current.strip():
            self._editor.setPlainText(wanted)


def _cmp_html(lines: list[str], reference: list[str], mark: bool = False) -> str:
    """Çıktı satırları; `mark` ise beklenenle tutmayan satırlar işaretli.

    Satır satır karşılaştırılıyor: tablolarda hangi satırın farklı olduğu
    bir bakışta görünsün. Gelen çıktı kısaysa eksik satırlar da gösteriliyor.
    """
    parcalar = []
    for index, satir in enumerate(lines):
        farkli = mark and (index >= len(reference) or satir.rstrip() != reference[index].rstrip())
        sinif = "ln diff" if farkli else "ln"
        parcalar.append(f'<span class="{sinif}">{html.escape(satir) or " "}</span>')
    if mark and len(lines) < len(reference):
        for _ in range(len(reference) - len(lines)):
            parcalar.append('<span class="ln miss">…</span>')
    if not parcalar:
        parcalar.append('<span class="ln">—</span>')
    return '<div class="cmp">' + "".join(parcalar) + "</div>"


def problem_state(saved: str) -> dict:
    """Kaydedilmiş problem durumu; kayıt yoksa ya da bozuksa boş durum."""
    state = {"answers": [], "drawing": empty_drawing(), "revealed": False}
    if not saved:
        return state
    try:
        value = json.loads(saved)
    except ValueError:
        return state
    if not isinstance(value, dict):
        return state
    state["answers"] = [str(item) for item in value.get("answers", [])]
    state["drawing"] = clean_drawing(value.get("drawing"))
    state["revealed"] = bool(value.get("revealed", False))
    return state
