"""Git patikasının terminal alıştırması (`"kind": "terminal"`).

Kod yazılmıyor: kişi terminale komut yazıyor, komut benzeticide
(`core/git_sim.World`) çalışıyor. Her komuttan sonra alıştırmanın hedefleri
(`core/git_checks.evaluate`) denetleniyor; hepsi tutunca alıştırma çözülmüş
sayılıyor. "Çalıştır" düğmesi yok, terminalin kendisi denetim.

Kayıt: `exercise_progress.code` sütununda JSON `{"commands": [...]}`. Bölüme
dönünce benzetici baştan kurulup komutlar sırayla yeniden çalıştırılıyor;
saat sabit adımla ilerlediği için commit kimlikleri de aynı çıkıyor.
"""

from __future__ import annotations

import json

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ..core.catalog import Exercise
from ..core.git_checks import build_world, evaluate
from ..core.git_sim import World
from ..core.language import LanguageManager
from ..widgets.git_terminal import GitTerminal


def saved_commands(code: str) -> list[str]:
    """Kayıttaki komut listesi; kayıt yoksa ya da bozuksa boş."""
    if not code:
        return []
    try:
        value = json.loads(code)
    except ValueError:
        return []
    if not isinstance(value, dict):
        return []
    return [str(c) for c in value.get("commands", []) if isinstance(c, str)]


def encode_commands(commands: list[str]) -> str:
    return json.dumps({"commands": commands}, ensure_ascii=False)


class GitWork(QWidget):
    """Sağ taraf: terminal + hedefler; kaydı ve çözümü dışarı bildiriyor.

    `changed(kod, hepsi_tuttu, hata)` her komuttan sonra: kod kayda yazılacak
    JSON, `hata` komut sıfırdan farklı kodla bitti mi (takıldın mı sayacı).
    `solved` hedefler bu dünyada ilk kez hepsi birden tutunca.
    """

    changed = Signal(str, bool, bool)
    solved = Signal(str)
    reset_done = Signal()

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._exercise: Exercise | None = None
        self._world: World | None = None
        self._commands: list[str] = []
        self._results: list[dict] = []
        self._all_passed = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        self.terminal = GitTerminal()
        self.terminal.command_entered.connect(self._on_command)
        self.terminal.reset_button.clicked.connect(self.reset)
        layout.addWidget(self.terminal)

    # --- dış ------------------------------------------------------------------

    @property
    def commands(self) -> list[str]:
        return list(self._commands)

    def show_exercise(self, exercise: Exercise, saved: str) -> None:
        """Dünyayı kurar, kayıttaki komutları yeniden çalıştırıp ekranı doldurur."""
        self._exercise = exercise
        self._commands = []
        self._world = build_world(exercise, self._language.language)
        self.terminal.clear_screen()
        self._welcome()
        for line in saved_commands(saved):
            self._execute(line)
        self._results = evaluate(self._world, exercise.checks)
        self._all_passed = bool(self._results) and all(r["passed"] for r in self._results)
        self.terminal.set_history(self._commands)
        self._refresh()

    def reset(self) -> None:
        """Alıştırmanın başına döner: dosyalar ve depo kurulumdaki hâline."""
        if self._exercise is None:
            return
        self._commands = []
        self._world = build_world(self._exercise, self._language.language)
        self.terminal.clear_screen()
        self._welcome()
        self.terminal.write_note(self._language.t("git.reset_done"), "warn")
        self._results = evaluate(self._world, self._exercise.checks)
        self._all_passed = False
        self.terminal.set_history([])
        self._refresh()
        self.changed.emit(encode_commands([]), False, False)
        self.reset_done.emit()
        self.terminal.focus_input()

    def retranslate(self) -> None:
        t = self._language.t
        self.terminal.set_texts(t("git.terminal"), t("git.reset"), t("terminal.clear"), t("git.placeholder"))
        if self._world is not None:
            self._world.lang = self._language.language if self._language.language in ("tr", "en") else "en"
        self._refresh()

    def focus(self) -> None:
        self.terminal.focus_input()

    # --- iç -------------------------------------------------------------------

    def _welcome(self) -> None:
        self.terminal.write_note(self._language.t("git.welcome"), "dim", bold=False)

    def _execute(self, line: str) -> int:
        """Satırı çalıştırıp ekrana yazar (yeniden oynatmada da)."""
        assert self._world is not None
        prompt = self._world.prompt()
        if line.strip() == "clear":
            self._world.run(line)
            self._commands.append(line)
            self.terminal.clear_screen()
            return 0
        self.terminal.write_command(prompt, line)
        if not line.strip():
            return 0
        out, code = self._world.run(line)
        self._commands.append(line)
        if out.lines:
            self.terminal.write_lines(out.lines)
        return code

    def _on_command(self, line: str) -> None:
        if self._world is None or self._exercise is None:
            return
        code = self._execute(line)
        if not line.strip():
            self._refresh()
            return
        self._results = evaluate(self._world, self._exercise.checks)
        passed = bool(self._results) and all(r["passed"] for r in self._results)
        newly = passed and not self._all_passed
        self._all_passed = passed
        if newly:
            self.terminal.write_note("✓ " + self._language.t("git.solved"), "ok")
        self._refresh()
        self.changed.emit(encode_commands(self._commands), passed, code != 0)
        if newly:
            self.solved.emit(self._exercise.id)

    def _refresh(self) -> None:
        if self._world is not None:
            self.terminal.set_prompt(self._world.prompt())
        goals = []
        for result in self._results:
            label = self._language.pick(result.get("label")) if result.get("label") else ""
            if label:
                goals.append((label, bool(result["passed"])))
        self.terminal.set_goals(self._language.t("git.goals"), goals)
