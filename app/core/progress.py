"""İlerleme, profil, notlar ve ayarların saklandığı yer.

Her şey kullanıcının kendi bilgisayarında, `%APPDATA%\\ProjeA\\progress.db`
dosyasında duruyor. Sunucu yok, hesap yok, internete hiçbir veri gitmiyor.

Veritabanı ilk günden sürümlü: `schema_version` tablosu hangi göçlerin
uygulandığını tutuyor. Yeni bir sürümde şema değişirse `MIGRATIONS` listesine
bir adım eklenir, açılışta eksik olanlar sırayla çalışır ve kullanıcının
mevcut verisi korunur.

Kayıtlar bölüm ve alıştırma **id'leriyle** eşleşiyor. Bu yüzden bir id bir kez
verildikten sonra asla değiştirilmez; başlık ve dosya adı değişebilir.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from ..paths import database_path

# Şema göçleri. Sıra önemlidir, listeye yalnızca sona ekleme yapılır.
MIGRATIONS: list[str] = [
    # 1 — ilk şema
    """
    CREATE TABLE IF NOT EXISTS profile (
        id          INTEGER PRIMARY KEY CHECK (id = 1),
        first_name  TEXT NOT NULL DEFAULT '',
        last_name   TEXT NOT NULL DEFAULT '',
        avatar      TEXT NOT NULL DEFAULT 'default',
        started_at  TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS settings (
        key    TEXT PRIMARY KEY,
        value  TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS section_progress (
        chapter_id   TEXT NOT NULL,
        section_id   TEXT NOT NULL,
        lesson_read  INTEGER NOT NULL DEFAULT 0,
        quiz_score   INTEGER,
        quiz_passed  INTEGER NOT NULL DEFAULT 0,
        updated_at   TEXT NOT NULL,
        PRIMARY KEY (chapter_id, section_id)
    );

    CREATE TABLE IF NOT EXISTS exercise_progress (
        chapter_id   TEXT NOT NULL,
        section_id   TEXT NOT NULL,
        exercise_id  TEXT NOT NULL,
        solved       INTEGER NOT NULL DEFAULT 0,
        attempts     INTEGER NOT NULL DEFAULT 0,
        code         TEXT NOT NULL DEFAULT '',
        updated_at   TEXT NOT NULL,
        PRIMARY KEY (chapter_id, section_id, exercise_id)
    );

    CREATE TABLE IF NOT EXISTS notes (
        chapter_id  TEXT NOT NULL,
        section_id  TEXT NOT NULL,
        body        TEXT NOT NULL DEFAULT '',
        updated_at  TEXT NOT NULL,
        PRIMARY KEY (chapter_id, section_id)
    );

    CREATE TABLE IF NOT EXISTS badges (
        badge_id   TEXT PRIMARY KEY,
        earned_at  TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS study_days (
        day  TEXT PRIMARY KEY
    );
    """,
]


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class SectionState:
    """Bir alt bölümün ilerleme durumu."""

    lesson_read: bool = False
    quiz_score: int | None = None
    quiz_passed: bool = False
    exercises_total: int = 0
    exercises_solved: int = 0

    @property
    def has_activity(self) -> bool:
        return self.lesson_read or self.quiz_score is not None or self.exercises_solved > 0

    def status(self, requires_quiz: bool, requires_exercises: bool) -> str:
        """Yol ekranında gösterilecek durum.

        Kilit yok: her bölüm her zaman açılabilir, bu yüzden yalnızca
        "tamamlandı / yarım kaldı / başlanmadı" ayrımı var.
        """
        quiz_ok = self.quiz_passed or not requires_quiz
        exercises_ok = (
            self.exercises_total > 0 and self.exercises_solved >= self.exercises_total
        ) or not requires_exercises

        if quiz_ok and exercises_ok and self.has_activity:
            return "completed"
        if self.has_activity:
            return "in_progress"
        return "not_started"


class ProgressStore:
    """Veritabanı erişimi."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or database_path()
        self._connection = sqlite3.connect(self._path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._migrate()
        self._ensure_profile()

    # --- kurulum ----------------------------------------------------------

    @contextmanager
    def _write(self):
        with self._connection:
            yield self._connection

    def _migrate(self) -> None:
        cursor = self._connection.execute(
            "CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL)"
        )
        row = self._connection.execute("SELECT MAX(version) AS v FROM schema_version").fetchone()
        current = row["v"] or 0

        for index, script in enumerate(MIGRATIONS, start=1):
            if index <= current:
                continue
            with self._write() as connection:
                connection.executescript(script)
                connection.execute(
                    "INSERT INTO schema_version (version) VALUES (?)", (index,)
                )
        cursor.close()

    @property
    def schema_version(self) -> int:
        row = self._connection.execute("SELECT MAX(version) AS v FROM schema_version").fetchone()
        return row["v"] or 0

    def _ensure_profile(self) -> None:
        row = self._connection.execute("SELECT id FROM profile WHERE id = 1").fetchone()
        if row is None:
            with self._write() as connection:
                connection.execute(
                    "INSERT INTO profile (id, started_at) VALUES (1, ?)", (_now(),)
                )

    def close(self) -> None:
        self._connection.close()

    # --- ayarlar ----------------------------------------------------------

    def setting(self, key: str, default: str = "") -> str:
        row = self._connection.execute(
            "SELECT value FROM settings WHERE key = ?", (key,)
        ).fetchone()
        return row["value"] if row else default

    def set_setting(self, key: str, value: str) -> None:
        with self._write() as connection:
            connection.execute(
                "INSERT INTO settings (key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, value),
            )

    # --- profil -----------------------------------------------------------

    def profile(self) -> dict:
        row = self._connection.execute("SELECT * FROM profile WHERE id = 1").fetchone()
        return dict(row) if row else {}

    def set_profile(self, first_name: str, last_name: str, avatar: str = "") -> None:
        with self._write() as connection:
            if avatar:
                connection.execute(
                    "UPDATE profile SET first_name = ?, last_name = ?, avatar = ? WHERE id = 1",
                    (first_name, last_name, avatar),
                )
            else:
                connection.execute(
                    "UPDATE profile SET first_name = ?, last_name = ? WHERE id = 1",
                    (first_name, last_name),
                )

    # --- çalışma günleri --------------------------------------------------

    def mark_study_day(self) -> None:
        """Bugün çalışıldı olarak işaretlenir (gün serisi için)."""
        with self._write() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO study_days (day) VALUES (?)",
                (date.today().isoformat(),),
            )

    def streak(self) -> int:
        """Bugünden geriye doğru kesintisiz çalışılan gün sayısı."""
        rows = self._connection.execute(
            "SELECT day FROM study_days ORDER BY day DESC"
        ).fetchall()
        if not rows:
            return 0

        days = [date.fromisoformat(row["day"]) for row in rows]
        today = date.today()

        # Bugün henüz çalışılmadıysa seri dünden başlayabilir.
        start = today if days[0] == today else None
        if start is None:
            if (today - days[0]).days > 1:
                return 0
            start = days[0]

        streak = 0
        expected = start
        for day in days:
            if day == expected:
                streak += 1
                expected = date.fromordinal(expected.toordinal() - 1)
            elif day < expected:
                break
        return streak

    # --- alt bölüm --------------------------------------------------------

    def section_state(self, chapter_id: str, section_id: str, exercises_total: int = 0) -> SectionState:
        row = self._connection.execute(
            "SELECT * FROM section_progress WHERE chapter_id = ? AND section_id = ?",
            (chapter_id, section_id),
        ).fetchone()

        solved = self._connection.execute(
            "SELECT COUNT(*) AS c FROM exercise_progress "
            "WHERE chapter_id = ? AND section_id = ? AND solved = 1",
            (chapter_id, section_id),
        ).fetchone()["c"]

        if row is None:
            return SectionState(exercises_total=exercises_total, exercises_solved=solved)

        return SectionState(
            lesson_read=bool(row["lesson_read"]),
            quiz_score=row["quiz_score"],
            quiz_passed=bool(row["quiz_passed"]),
            exercises_total=exercises_total,
            exercises_solved=solved,
        )

    def _touch_section(self, chapter_id: str, section_id: str) -> None:
        with self._write() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO section_progress "
                "(chapter_id, section_id, updated_at) VALUES (?, ?, ?)",
                (chapter_id, section_id, _now()),
            )

    def mark_lesson_read(self, chapter_id: str, section_id: str) -> None:
        self._touch_section(chapter_id, section_id)
        with self._write() as connection:
            connection.execute(
                "UPDATE section_progress SET lesson_read = 1, updated_at = ? "
                "WHERE chapter_id = ? AND section_id = ?",
                (_now(), chapter_id, section_id),
            )
        self.mark_study_day()

    def record_quiz(self, chapter_id: str, section_id: str, score: int, passed: bool) -> None:
        """Sınav sonucunu kaydeder.

        Daha düşük bir puan öncekinin üzerine yazılmaz — bölüm tekrar
        çözülebildiği için kullanıcının en iyi sonucu korunur.
        """
        self._touch_section(chapter_id, section_id)
        with self._write() as connection:
            connection.execute(
                "UPDATE section_progress SET "
                "quiz_score = MAX(COALESCE(quiz_score, 0), ?), "
                "quiz_passed = MAX(quiz_passed, ?), updated_at = ? "
                "WHERE chapter_id = ? AND section_id = ?",
                (score, int(passed), _now(), chapter_id, section_id),
            )
        self.mark_study_day()

    # --- alıştırma --------------------------------------------------------

    def exercise_code(self, chapter_id: str, section_id: str, exercise_id: str) -> str:
        row = self._connection.execute(
            "SELECT code FROM exercise_progress "
            "WHERE chapter_id = ? AND section_id = ? AND exercise_id = ?",
            (chapter_id, section_id, exercise_id),
        ).fetchone()
        return row["code"] if row else ""

    def exercise_solved(self, chapter_id: str, section_id: str, exercise_id: str) -> bool:
        row = self._connection.execute(
            "SELECT solved FROM exercise_progress "
            "WHERE chapter_id = ? AND section_id = ? AND exercise_id = ?",
            (chapter_id, section_id, exercise_id),
        ).fetchone()
        return bool(row["solved"]) if row else False

    def save_exercise(
        self,
        chapter_id: str,
        section_id: str,
        exercise_id: str,
        code: str,
        solved: bool | None = None,
        count_attempt: bool = False,
    ) -> None:
        """Yazılan kodu ve varsa sonucu kaydeder.

        `solved` bir kez True olduysa sonradan False'a düşürülmez: kullanıcı
        çözdükten sonra kodu kurcalarsa ilerlemesini kaybetmesin.
        """
        with self._write() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO exercise_progress "
                "(chapter_id, section_id, exercise_id, updated_at) VALUES (?, ?, ?, ?)",
                (chapter_id, section_id, exercise_id, _now()),
            )
            connection.execute(
                "UPDATE exercise_progress SET code = ?, updated_at = ?"
                + (", attempts = attempts + 1" if count_attempt else "")
                + (", solved = MAX(solved, ?)" if solved is not None else "")
                + " WHERE chapter_id = ? AND section_id = ? AND exercise_id = ?",
                (
                    (code, _now())
                    + ((int(solved),) if solved is not None else ())
                    + (chapter_id, section_id, exercise_id)
                ),
            )
        if count_attempt:
            self.mark_study_day()

    def attempts(self, chapter_id: str, section_id: str, exercise_id: str) -> int:
        row = self._connection.execute(
            "SELECT attempts FROM exercise_progress "
            "WHERE chapter_id = ? AND section_id = ? AND exercise_id = ?",
            (chapter_id, section_id, exercise_id),
        ).fetchone()
        return row["attempts"] if row else 0

    # --- notlar -----------------------------------------------------------

    def note(self, chapter_id: str, section_id: str) -> str:
        row = self._connection.execute(
            "SELECT body FROM notes WHERE chapter_id = ? AND section_id = ?",
            (chapter_id, section_id),
        ).fetchone()
        return row["body"] if row else ""

    def save_note(self, chapter_id: str, section_id: str, body: str) -> None:
        with self._write() as connection:
            connection.execute(
                "INSERT INTO notes (chapter_id, section_id, body, updated_at) "
                "VALUES (?, ?, ?, ?) "
                "ON CONFLICT(chapter_id, section_id) DO UPDATE SET "
                "body = excluded.body, updated_at = excluded.updated_at",
                (chapter_id, section_id, body, _now()),
            )

    # --- toplu sayılar ----------------------------------------------------

    def solved_exercise_count(self) -> int:
        return self._connection.execute(
            "SELECT COUNT(*) AS c FROM exercise_progress WHERE solved = 1"
        ).fetchone()["c"]

    def quiz_average(self) -> int | None:
        row = self._connection.execute(
            "SELECT AVG(quiz_score) AS a FROM section_progress WHERE quiz_score IS NOT NULL"
        ).fetchone()
        return round(row["a"]) if row["a"] is not None else None

    def last_visited(self) -> tuple[str, str] | None:
        """En son işlem yapılan alt bölüm — "kaldığın yerden devam" için."""
        row = self._connection.execute(
            "SELECT chapter_id, section_id FROM section_progress "
            "ORDER BY updated_at DESC LIMIT 1"
        ).fetchone()
        return (row["chapter_id"], row["section_id"]) if row else None
