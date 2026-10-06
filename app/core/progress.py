"""İlerleme, profil, notlar ve ayarların saklandığı yer.

Her şey kullanıcının kendi bilgisayarında, `%APPDATA%\\Odyssey\\progress.db`
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

# Programın en son açıldığı gün (ayar tablosunda). Çalışma günü değil.
SEEN_KEY = "last_seen_day"

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
    # 2 — günlük etkinlik günlüğü
    #
    # `study_days` yalnızca "o gün çalışıldı" diyor, ne kadar çalışıldığını
    # söylemiyor. `updated_at` alanları da her dokunuşta üzerine yazıldığı
    # için geçmiş tutmuyor: bir alıştırmayı iki kez açarsan ilk çözüm tarihi
    # kayboluyor.
    #
    # Bu tablo **olay ekliyor, güncellemiyor** — profildeki etkinlik grafiği
    # ve rozet koşulları ("bir günde beş alıştırma", "yedi gün üst üste")
    # ancak böyle hesaplanabiliyor.
    """
    CREATE TABLE IF NOT EXISTS activity (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        day         TEXT NOT NULL,
        kind        TEXT NOT NULL,
        chapter_id  TEXT NOT NULL DEFAULT '',
        section_id  TEXT NOT NULL DEFAULT '',
        ref_id      TEXT NOT NULL DEFAULT '',
        created_at  TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS activity_day ON activity (day);

    -- Bu güncellemeden önce ilerlemiş kullanıcıların grafiği boş
    -- açılmasın diye eldeki kayıtlardan geriye dolduruluyor. `updated_at`
    -- son dokunuşu gösterdiği için tarihler yaklaşık; yine de gerçek veri.
    INSERT INTO activity (day, kind, chapter_id, section_id, ref_id, created_at)
    SELECT substr(updated_at, 1, 10), 'exercise', chapter_id, section_id,
           exercise_id, updated_at
    FROM exercise_progress WHERE solved = 1;

    INSERT INTO activity (day, kind, chapter_id, section_id, ref_id, created_at)
    SELECT substr(updated_at, 1, 10), 'lesson', chapter_id, section_id, '',
           updated_at
    FROM section_progress WHERE lesson_read = 1;

    INSERT INTO activity (day, kind, chapter_id, section_id, ref_id, created_at)
    SELECT substr(updated_at, 1, 10), 'quiz', chapter_id, section_id, '',
           updated_at
    FROM section_progress WHERE quiz_score IS NOT NULL;
    """,
    # 3 — bildirimler. `title_key` metnin kendisi değil **kimliği** tutuyor
    # (rozet bildiriminde rozetin id'si): metin gösterildiği anda seçili
    # dilde üretiliyor, yoksa dil değişince bildirim eski dilde kalıyordu.
    """
    CREATE TABLE IF NOT EXISTS notifications (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        kind        TEXT NOT NULL,
        title_key   TEXT NOT NULL,
        icon        TEXT NOT NULL DEFAULT '',
        is_read     INTEGER NOT NULL DEFAULT 0,
        created_at  TEXT NOT NULL
    );
    """,
    # 4 — Notlarım. İlk şemadaki `notes` tablosu bölüm başına tek, adsız bir
    # not tutuyordu ve arayüzü hiç yazılmadı. Notlar artık adlı ve bir
    # bölümde birden fazla olabiliyor. Klasör patikanın kendisi
    # (`chapter_id`); `section_id` boşsa not bir derse bağlı değil.
    #
    # `notes` tablosu silinmiyor: içinde bir şey varsa buraya kopyalanıyor,
    # kullanıcının verisi hiçbir göçte yok edilmiyor.
    """
    CREATE TABLE IF NOT EXISTS notebook_entries (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_id  TEXT NOT NULL,
        section_id  TEXT NOT NULL DEFAULT '',
        title       TEXT NOT NULL,
        body        TEXT NOT NULL DEFAULT '',
        created_at  TEXT NOT NULL,
        updated_at  TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS notebook_entries_chapter
        ON notebook_entries (chapter_id);

    INSERT INTO notebook_entries
        (chapter_id, section_id, title, body, created_at, updated_at)
    SELECT chapter_id, section_id, section_id, body, updated_at, updated_at
    FROM notes WHERE trim(body) <> '';
    """,
    # 5 — Notlarım'da kullanıcının kendi klasörleri. Not patikasını
    # (`chapter_id`) ve dersini taşımaya devam ediyor; `folder_id` doluysa
    # ağaçta o klasörde duruyor ve ders bağlantısı ("Derse git", dersteki
    # panel) korunuyor. Klasör silinince not silinmiyor: sütun boşalıyor,
    # not patikasının klasörüne dönüyor.
    #
    # Ayrı bir göç, 4'e eklenmedi: 4 Alican'ın veritabanında zaten
    # uygulandı, değiştirilse onda hiç çalışmazdı.
    """
    CREATE TABLE IF NOT EXISTS notebook_folders (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT NOT NULL,
        created_at  TEXT NOT NULL
    );

    ALTER TABLE notebook_entries ADD COLUMN folder_id INTEGER
        REFERENCES notebook_folders (id) ON DELETE SET NULL;
    """,
    # 6 — bildirim zili kalktı (Alican, 25 Eylül). Bölüm bitirme ve rozet
    # artık sağ altta o an beliren bir kartla duyuruluyor; saklanacak,
    # okundu sayılacak bir liste kalmadı. Rozetlerin kendisi `badges`
    # tablosunda duruyor, burada yalnızca duyuruların kopyası vardı.
    """
    DROP TABLE IF EXISTS notifications;
    """,
    # 7 — ders notlarının okunması (Alican, 29 Eylül: notları bitirince
    # sekmede tik çıkmıyordu). Bir not sonuna kadar kaydırılınca okunmuş
    # sayılıyor; bölümdeki notların hepsi okununca "Ders Notu" sekmesine tik.
    # Bölümün tamamlanma şartı değil, yalnızca gösterge.
    """
    CREATE TABLE IF NOT EXISTS notes_read (
        chapter_id  TEXT NOT NULL,
        section_id  TEXT NOT NULL,
        document_id TEXT NOT NULL,
        read_at     TEXT NOT NULL,
        PRIMARY KEY (chapter_id, section_id, document_id)
    );
    """,
    # 8 — çalışma zamanlayıcısı (Alican, 30 Eylül). Tamamlanan (ya da en az
    # iki dakika süren) her odak evresi bir satır: günün toplam odak süresi
    # buradan. Etkinlik takvimine ayrıca `activity` tablosunda "focus" olayı
    # düşüyor.
    """
    CREATE TABLE IF NOT EXISTS focus_sessions (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        day         TEXT NOT NULL,
        minutes     INTEGER NOT NULL,
        created_at  TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_focus_day ON focus_sessions (day);
    """,
    # 9 — geçmiş denemeler (Alican, 30 Eylül: "geçmişte yaptıkları yanlışları
    # görebilmeleri lazım"). Alıştırmada her çalıştırma (problemde her cevap
    # denetimi) ve sınavda her deneme ayrı satır. `exercise_progress.code`
    # yalnızca son hâli tutuyordu; yanlış denemeler üzerine yazılıp
    # kayboluyordu.
    """
    CREATE TABLE IF NOT EXISTS exercise_attempts (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_id  TEXT NOT NULL,
        section_id  TEXT NOT NULL,
        exercise_id TEXT NOT NULL,
        code        TEXT NOT NULL,
        passed      INTEGER NOT NULL,
        detail      TEXT NOT NULL DEFAULT '',
        created_at  TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_exercise_attempts
        ON exercise_attempts (chapter_id, section_id, exercise_id);
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_id  TEXT NOT NULL,
        section_id  TEXT NOT NULL,
        score       INTEGER NOT NULL,
        passed      INTEGER NOT NULL,
        answers     TEXT NOT NULL,
        created_at  TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_quiz_attempts ON quiz_attempts (chapter_id, section_id);
    """,
    # 10 — yarıda bırakılan sınav denemesi (0.9.2). Sınavdan çıkan kişinin
    # o ana kadarki cevapları ve yanlışları kayboluyordu (Alican'ın arkadaşı);
    # artık puansız, "yarıda bırakıldı" olarak saklanıyor.
    """
    ALTER TABLE quiz_attempts ADD COLUMN abandoned INTEGER NOT NULL DEFAULT 0;
    """,
    # 11 — bölümün ilk tamamlandığı an (0.9.2). Bölüme sonradan alıştırma
    # eklenince bitirmiş olan "yarım kaldı"ya düşmesin (`core/completion.py`).
    """
    ALTER TABLE section_progress ADD COLUMN completed_at TEXT;
    """,
]

# Bir alıştırma için saklanan en fazla deneme; eskiler siliniyor.
MAX_EXERCISE_ATTEMPTS = 40
# Bir sınav için saklanan en fazla deneme.
MAX_QUIZ_ATTEMPTS = 20


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
    # İlk tamamlandığı an; doluysa bölüm hep tamamlanmış sayılıyor.
    completed_at: str | None = None

    @property
    def has_activity(self) -> bool:
        return self.lesson_read or self.quiz_score is not None or self.exercises_solved > 0

    def status(self, requires_quiz: bool, requires_exercises: bool) -> str:
        """Yol ekranında gösterilecek durum.

        Kilit yok: her bölüm her zaman açılabilir, bu yüzden yalnızca
        "tamamlandı / yarım kaldı / başlanmadı" ayrımı var.
        """
        if self.completed_at:
            return "completed"
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

    def mark_seen(self) -> None:
        """Program bugün açıldı (hatırlatmaların "N gündür yoksun" hesabı).

        Çalışma günü değil: seri yalnızca çalışılan günlerle sürüyor. Ama
        programı sabah açıp konulara bakan birine akşam "3 gündür yoksun"
        demek yanlıştı (Alican'a gelen bildirim, 29 Eylül).
        """
        bugun = date.today().isoformat()
        if self.setting(SEEN_KEY, "") != bugun:
            self.set_setting(SEEN_KEY, bugun)

    def last_seen_day(self) -> date | None:
        """Programın en son açıldığı ya da çalışıldığı gün (hangisi sonraysa)."""
        gunler = [self.last_study_day()]
        try:
            gunler.append(date.fromisoformat(self.setting(SEEN_KEY, "")))
        except ValueError:
            pass
        gunler = [g for g in gunler if g is not None]
        return max(gunler) if gunler else None

    def mark_study_day(self) -> None:
        """Bugün çalışıldı olarak işaretlenir (gün serisi için)."""
        with self._write() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO study_days (day) VALUES (?)",
                (date.today().isoformat(),),
            )

    def add_focus_session(self, minutes: int) -> None:
        """Bir odak evresini kaydeder (çalışma zamanlayıcısı)."""
        with self._write() as connection:
            connection.execute(
                "INSERT INTO focus_sessions (day, minutes, created_at) VALUES (?, ?, ?)",
                (date.today().isoformat(), int(minutes), _now()),
            )

    def focus_today(self) -> tuple[int, int]:
        """Bugünkü odak: (toplam dakika, evre sayısı)."""
        row = self._connection.execute(
            "SELECT COALESCE(SUM(minutes), 0) AS m, COUNT(*) AS n FROM focus_sessions WHERE day = ?",
            (date.today().isoformat(),),
        ).fetchone()
        return int(row["m"]), int(row["n"])

    def record_activity(
        self,
        kind: str,
        chapter_id: str = "",
        section_id: str = "",
        ref_id: str = "",
    ) -> None:
        """Etkinlik günlüğüne bir olay ekler.

        Bu tablo **yalnızca eklenir**, güncellenmez: profildeki grafik ve
        rozet koşulları geçmişe bakıyor, son duruma değil.
        """
        with self._write() as connection:
            connection.execute(
                "INSERT INTO activity (day, kind, chapter_id, section_id, ref_id, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (date.today().isoformat(), kind, chapter_id, section_id, ref_id, _now()),
            )

    def activity_by_day(self, days: int = 182) -> dict[str, int]:
        """Son `days` gün için gün başına olay sayısı.

        Olayı olmayan günler sözlükte yok; çağıran taraf sıfır sayıyor.
        """
        basla = date.fromordinal(date.today().toordinal() - days + 1).isoformat()
        rows = self._connection.execute(
            "SELECT day, COUNT(*) AS n FROM activity WHERE day >= ? GROUP BY day",
            (basla,),
        ).fetchall()
        return {row["day"]: row["n"] for row in rows}

    def activity_years(self) -> list[int]:
        """Etkinlik bulunan yıllar, yeniden eskiye.

        İçinde bulunulan yıl her zaman listede — hiç kayıt yokken de bir
        ızgara gösterilebilsin diye.
        """
        rows = self._connection.execute(
            "SELECT DISTINCT substr(day, 1, 4) AS y FROM activity"
        ).fetchall()
        yillar = {int(row["y"]) for row in rows if row["y"]}
        yillar.add(date.today().year)
        return sorted(yillar, reverse=True)

    def activity_for_year(self, year: int) -> dict[str, int]:
        """Bir yılın gün başına olay sayısı."""
        rows = self._connection.execute(
            "SELECT day, COUNT(*) AS n FROM activity WHERE day LIKE ? GROUP BY day",
            (f"{year}-%",),
        ).fetchall()
        return {row["day"]: row["n"] for row in rows}

    def busiest_day_count(self) -> int:
        """En yoğun günde kaç çalışma yapılmış?"""
        row = self._connection.execute(
            "SELECT COUNT(*) AS n FROM activity GROUP BY day ORDER BY n DESC LIMIT 1"
        ).fetchone()
        return row["n"] if row else 0

    def best_quiz_score(self) -> int | None:
        """En yüksek sınav puanı; hiç sınav yoksa `None`."""
        row = self._connection.execute(
            "SELECT MAX(quiz_score) AS s FROM section_progress"
        ).fetchone()
        return row["s"] if row and row["s"] is not None else None

    def passed_quiz_count(self) -> int:
        """Geçilen sınav sayısı."""
        row = self._connection.execute(
            "SELECT COUNT(*) AS n FROM section_progress WHERE quiz_passed = 1"
        ).fetchone()
        return row["n"] if row else 0

    # --- rozetler ---------------------------------------------------------

    def earned_badges(self) -> dict[str, str]:
        """Kazanılmış rozetler: `id -> kazanıldığı tarih`."""
        rows = self._connection.execute(
            "SELECT badge_id, earned_at FROM badges"
        ).fetchall()
        return {row["badge_id"]: row["earned_at"] for row in rows}

    def award_badge(self, badge_id: str) -> None:
        """Rozeti kazanılmış olarak kaydeder.

        `INSERT OR IGNORE`: koşul sonradan tekrar sağlansa bile ilk
        kazanım tarihi korunuyor.
        """
        with self._write() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO badges (badge_id, earned_at) VALUES (?, ?)",
                (badge_id, _now()),
            )

    def activity_totals(self) -> dict[str, int]:
        """Tür başına toplam olay sayısı."""
        rows = self._connection.execute(
            "SELECT kind, COUNT(*) AS n FROM activity GROUP BY kind"
        ).fetchall()
        return {row["kind"]: row["n"] for row in rows}

    def active_day_count(self) -> int:
        """Kaç ayrı günde çalışılmış?"""
        row = self._connection.execute(
            "SELECT COUNT(*) AS n FROM study_days"
        ).fetchone()
        return row["n"] if row else 0

    def last_study_day(self) -> date | None:
        """En son çalışılan gün; hiç çalışılmadıysa None (hatırlatmalar için)."""
        row = self._connection.execute("SELECT MAX(day) AS day FROM study_days").fetchone()
        return date.fromisoformat(row["day"]) if row and row["day"] else None

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

    def section_state(self, chapter_id: str, section_id: str, exercises=()) -> SectionState:
        """Bölümün ilerlemesi.

        `exercises` bölümdeki **güncel** alıştırmalar (nesne ya da id).
        Çözülen sayısı yalnızca onların arasından sayılıyor. Önce bölümdeki
        bütün `solved = 1` satırları sayılıyordu; id'si değişen bir
        alıştırmanın eski kaydı da sayıma giriyor ve yenisi çözülmemişken
        bölüm "tamamlandı" görünüyordu.
        """
        row = self._connection.execute(
            "SELECT * FROM section_progress WHERE chapter_id = ? AND section_id = ?",
            (chapter_id, section_id),
        ).fetchone()

        ids = {getattr(item, "id", item) for item in exercises}
        exercises_total = len(ids)
        solved = 0
        if ids:
            cozulenler = self._connection.execute(
                "SELECT exercise_id FROM exercise_progress "
                "WHERE chapter_id = ? AND section_id = ? AND solved = 1",
                (chapter_id, section_id),
            ).fetchall()
            solved = sum(1 for satir in cozulenler if satir["exercise_id"] in ids)

        if row is None:
            return SectionState(exercises_total=exercises_total, exercises_solved=solved)

        return SectionState(
            lesson_read=bool(row["lesson_read"]),
            quiz_score=row["quiz_score"],
            quiz_passed=bool(row["quiz_passed"]),
            exercises_total=exercises_total,
            exercises_solved=solved,
            completed_at=row["completed_at"],
        )

    def mark_section_completed(self, chapter_id: str, section_id: str) -> None:
        """Bölümün ilk tamamlandığı anı yazar (bir kez; sonra değişmez)."""
        with self._write() as connection:
            connection.execute(
                "UPDATE section_progress SET completed_at = ? "
                "WHERE chapter_id = ? AND section_id = ? AND completed_at IS NULL",
                (_now(), chapter_id, section_id),
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

        # Olay yalnızca **ilk** okumada yazılıyor. Aynı dersi beş kez açmak
        # grafikte beş olay göstermemeli; orada "ne yaptım" duruyor,
        # "kaç kez baktım" değil.
        row = self._connection.execute(
            "SELECT lesson_read FROM section_progress "
            "WHERE chapter_id = ? AND section_id = ?",
            (chapter_id, section_id),
        ).fetchone()
        ilk_kez = not (row and row["lesson_read"])

        with self._write() as connection:
            connection.execute(
                "UPDATE section_progress SET lesson_read = 1, updated_at = ? "
                "WHERE chapter_id = ? AND section_id = ?",
                (_now(), chapter_id, section_id),
            )
        if ilk_kez:
            self.record_activity("lesson", chapter_id, section_id)
        self.mark_study_day()

    def mark_note_read(self, chapter_id: str, section_id: str, document_id: str) -> bool:
        """Ders notu sonuna kadar okundu. İlk kez okunduysa `True`."""
        with self._write() as connection:
            imlec = connection.execute(
                "INSERT OR IGNORE INTO notes_read (chapter_id, section_id, document_id, read_at) "
                "VALUES (?, ?, ?, ?)",
                (chapter_id, section_id, document_id, _now()),
            )
            ilk_kez = imlec.rowcount > 0
        # Notu sonuna kadar okumak da çalışmak: ders gibi günü sayıyor.
        self.mark_study_day()
        return ilk_kez

    def notes_read(self, chapter_id: str, section_id: str) -> set[str]:
        """Bölümde sonuna kadar okunmuş notların id'leri."""
        rows = self._connection.execute(
            "SELECT document_id FROM notes_read WHERE chapter_id = ? AND section_id = ?",
            (chapter_id, section_id),
        ).fetchall()
        return {row["document_id"] for row in rows}

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
        # Sınav farklı: her deneme ayrı bir olay. Tekrar girmek gerçekten
        # o gün yapılmış bir iş.
        self.record_activity("quiz", chapter_id, section_id)
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
        # Olay yalnızca **ilk çözümde** yazılıyor: aynı alıştırmayı tekrar
        # çalıştırmak grafiğe yeni bir olay eklememeli.
        ilk_cozum = bool(solved) and not self.exercise_solved(
            chapter_id, section_id, exercise_id
        )

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
        if ilk_cozum:
            self.record_activity("exercise", chapter_id, section_id, exercise_id)
        if count_attempt:
            self.mark_study_day()

    # --- geçmiş denemeler ------------------------------------------------------

    def add_exercise_attempt(
        self,
        chapter_id: str,
        section_id: str,
        exercise_id: str,
        code: str,
        passed: bool,
        detail: str = "",
    ) -> bool:
        """Bir denemeyi kaydeder; kaydettiyse True.

        Bir öncekiyle aynı kod ve aynı sonuçsa yazılmıyor: aynı kodu üst
        üste çalıştırmak listeyi aynı satırla doldurmasın. En eski kayıtlar
        `MAX_EXERCISE_ATTEMPTS`'i geçince siliniyor.
        """
        anahtar = (chapter_id, section_id, exercise_id)
        son = self._connection.execute(
            "SELECT code, passed FROM exercise_attempts WHERE chapter_id = ? AND section_id = ? "
            "AND exercise_id = ? ORDER BY id DESC LIMIT 1",
            anahtar,
        ).fetchone()
        if son is not None and son["code"] == code and bool(son["passed"]) == bool(passed):
            return False
        with self._write() as connection:
            connection.execute(
                "INSERT INTO exercise_attempts (chapter_id, section_id, exercise_id, code, passed, "
                "detail, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (*anahtar, code, int(bool(passed)), detail, _now()),
            )
            connection.execute(
                "DELETE FROM exercise_attempts WHERE chapter_id = ? AND section_id = ? "
                "AND exercise_id = ? AND id NOT IN (SELECT id FROM exercise_attempts "
                "WHERE chapter_id = ? AND section_id = ? AND exercise_id = ? "
                "ORDER BY id DESC LIMIT ?)",
                (*anahtar, *anahtar, MAX_EXERCISE_ATTEMPTS),
            )
        return True

    def exercise_attempts(self, chapter_id: str, section_id: str, exercise_id: str) -> list[dict]:
        """Denemeler, en yenisi başta."""
        rows = self._connection.execute(
            "SELECT id, code, passed, detail, created_at FROM exercise_attempts "
            "WHERE chapter_id = ? AND section_id = ? AND exercise_id = ? ORDER BY id DESC",
            (chapter_id, section_id, exercise_id),
        ).fetchall()
        return [dict(row) | {"passed": bool(row["passed"])} for row in rows]

    def add_quiz_attempt(
        self, chapter_id: str, section_id: str, score: int, passed: bool, answers: str,
        abandoned: bool = False,
    ) -> None:
        """Bir sınav denemesini cevaplarıyla kaydeder (`answers` JSON).

        `abandoned`: sınav bitirilmeden çıkıldı; yalnızca cevaplanan sorular
        var, puan sayılmıyor (bölümün sınav notuna yazılmıyor).
        """
        with self._write() as connection:
            connection.execute(
                "INSERT INTO quiz_attempts (chapter_id, section_id, score, passed, answers, "
                "created_at, abandoned) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (chapter_id, section_id, int(score), int(bool(passed)), answers, _now(),
                 int(bool(abandoned))),
            )
            connection.execute(
                "DELETE FROM quiz_attempts WHERE chapter_id = ? AND section_id = ? AND id NOT IN "
                "(SELECT id FROM quiz_attempts WHERE chapter_id = ? AND section_id = ? "
                "ORDER BY id DESC LIMIT ?)",
                (chapter_id, section_id, chapter_id, section_id, MAX_QUIZ_ATTEMPTS),
            )

    def quiz_attempts(self, chapter_id: str, section_id: str) -> list[dict]:
        """Sınav denemeleri, en yenisi başta."""
        rows = self._connection.execute(
            "SELECT id, score, passed, answers, created_at, abandoned FROM quiz_attempts "
            "WHERE chapter_id = ? AND section_id = ? ORDER BY id DESC",
            (chapter_id, section_id),
        ).fetchall()
        return [dict(row) | {"passed": bool(row["passed"]), "abandoned": bool(row["abandoned"])}
                for row in rows]

    def attempts(self, chapter_id: str, section_id: str, exercise_id: str) -> int:
        row = self._connection.execute(
            "SELECT attempts FROM exercise_progress "
            "WHERE chapter_id = ? AND section_id = ? AND exercise_id = ?",
            (chapter_id, section_id, exercise_id),
        ).fetchone()
        return row["attempts"] if row else 0

    # --- Notlarım ---------------------------------------------------------
    #
    # Aynı klasörde iki not aynı adı taşımıyor: ağaçta ikisi ayırt
    # edilemiyor, dışa aktarınca da dosya adları çakışıyor. Çakışan ada
    # sonuna " (2)" ekleniyor; hiçbir notun üstüne yazılmıyor.

    def notebook_entries(self) -> list[dict]:
        """Bütün notlar, gövdeleri olmadan, eklenme sırasıyla.

        Sıra değişiklik tarihine göre değil: yazdıkça en üste zıplayan bir
        not ağaçta yerini kaybettiriyordu.
        """
        rows = self._connection.execute(
            "SELECT id, chapter_id, section_id, folder_id, title, created_at, updated_at "
            "FROM notebook_entries ORDER BY created_at, id"
        ).fetchall()
        return [dict(row) for row in rows]

    def notebook_entries_with_body(self) -> list[dict]:
        """Bütün notlar gövdeleriyle (genel arama için)."""
        rows = self._connection.execute(
            "SELECT id, chapter_id, section_id, folder_id, title, body "
            "FROM notebook_entries ORDER BY created_at, id"
        ).fetchall()
        return [dict(row) for row in rows]

    def notebook_entry(self, entry_id: int) -> dict | None:
        row = self._connection.execute(
            "SELECT * FROM notebook_entries WHERE id = ?", (entry_id,)
        ).fetchone()
        return dict(row) if row else None

    def notebook_entry_count(self) -> int:
        return self._connection.execute(
            "SELECT COUNT(*) AS c FROM notebook_entries"
        ).fetchone()["c"]

    def written_note_count(self) -> int:
        """İçinde bir şey yazılı notların sayısı (rozet için).

        Notlarım'da açılan not önce boş oluşuyor; adı konmuş ama boş bir not
        "not aldım" sayılmıyor.
        """
        return self._connection.execute(
            "SELECT COUNT(*) AS c FROM notebook_entries WHERE trim(body) <> ''"
        ).fetchone()["c"]

    def add_notebook_entry(
        self,
        chapter_id: str,
        section_id: str,
        title: str,
        body: str = "",
        folder_id: int | None = None,
    ) -> int:
        """Yeni not ekler, id'sini döndürür."""
        title = self._free_title(chapter_id, title, folder_id=folder_id)
        now = _now()
        with self._write() as connection:
            cursor = connection.execute(
                "INSERT INTO notebook_entries "
                "(chapter_id, section_id, folder_id, title, body, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (chapter_id, section_id, folder_id, title, body, now, now),
            )
        return int(cursor.lastrowid)

    def move_notebook_entry(
        self, entry_id: int, *, chapter_id: str | None = None, folder_id: int | None = None
    ) -> str | None:
        """Notu taşır; dönen değer notun son adı (hedefte çakışırsa sayılı).

        `folder_id` verilirse not kullanıcının klasörüne gidiyor, patikası
        ve dersi yerinde kalıyor. Verilmezse `chapter_id` patikasının
        klasörüne dönüyor; başka bir patikaya gidiyorsa ders bağlantısı
        kalkıyor, çünkü o ders o patikada yok.
        """
        entry = self.notebook_entry(entry_id)
        if entry is None:
            return None
        if folder_id is not None:
            yeni_patika, yeni_ders = entry["chapter_id"], entry["section_id"]
        else:
            yeni_patika = entry["chapter_id"] if chapter_id is None else chapter_id
            yeni_ders = entry["section_id"] if yeni_patika == entry["chapter_id"] else ""
        ad = self._free_title(yeni_patika, entry["title"], exclude_id=entry_id, folder_id=folder_id)
        with self._write() as connection:
            connection.execute(
                "UPDATE notebook_entries SET chapter_id = ?, section_id = ?, folder_id = ?, "
                "title = ? WHERE id = ?",
                (yeni_patika, yeni_ders, folder_id, ad, entry_id),
            )
        return ad

    def update_notebook_entry(
        self, entry_id: int, *, title: str | None = None, body: str | None = None
    ) -> str | None:
        """Notun adını ve/veya gövdesini değiştirir.

        Dönen değer notun **son** adı: istenen ad klasörde başka bir notta
        varsa sonuna sayı eklenmiş hâli. Not yoksa `None`.
        """
        entry = self.notebook_entry(entry_id)
        if entry is None:
            return None

        yeni_ad = entry["title"]
        if title is not None and title.strip() and title.strip() != entry["title"]:
            yeni_ad = self._free_title(
                entry["chapter_id"], title, exclude_id=entry_id, folder_id=entry["folder_id"]
            )
        yeni_govde = entry["body"] if body is None else body

        if yeni_ad == entry["title"] and yeni_govde == entry["body"]:
            return yeni_ad

        with self._write() as connection:
            connection.execute(
                "UPDATE notebook_entries SET title = ?, body = ?, updated_at = ? "
                "WHERE id = ?",
                (yeni_ad, yeni_govde, _now(), entry_id),
            )
        return yeni_ad

    def delete_notebook_entry(self, entry_id: int) -> None:
        with self._write() as connection:
            connection.execute("DELETE FROM notebook_entries WHERE id = ?", (entry_id,))

    def _free_title(
        self,
        chapter_id: str,
        title: str,
        exclude_id: int | None = None,
        folder_id: int | None = None,
    ) -> str:
        """Notun duracağı klasörde boşta olan ad: "Ad", "Ad (2)", "Ad (3)"...

        Klasör, kullanıcının klasörü (`folder_id`) ya da yoksa patikanın
        klasörü.
        """
        from .user_notes import name_key, unique_title

        if folder_id is not None:
            rows = self._connection.execute(
                "SELECT title FROM notebook_entries WHERE folder_id = ? AND id IS NOT ?",
                (folder_id, exclude_id),
            ).fetchall()
        else:
            rows = self._connection.execute(
                "SELECT title FROM notebook_entries "
                "WHERE folder_id IS NULL AND chapter_id = ? AND id IS NOT ?",
                (chapter_id, exclude_id),
            ).fetchall()
        return unique_title(title, {name_key(row["title"]) for row in rows})

    # --- Notlarım: kullanıcının klasörleri ---------------------------------

    def notebook_folders(self) -> list[dict]:
        rows = self._connection.execute(
            "SELECT id, name, created_at FROM notebook_folders ORDER BY created_at, id"
        ).fetchall()
        return [dict(row) for row in rows]

    def add_notebook_folder(self, name: str) -> int:
        name = self._free_folder_name(name)
        with self._write() as connection:
            cursor = connection.execute(
                "INSERT INTO notebook_folders (name, created_at) VALUES (?, ?)", (name, _now())
            )
        return int(cursor.lastrowid)

    def rename_notebook_folder(self, folder_id: int, name: str) -> str | None:
        """Klasörün son adını döndürür; ad çakışırsa sayılı hâli."""
        row = self._connection.execute(
            "SELECT name FROM notebook_folders WHERE id = ?", (folder_id,)
        ).fetchone()
        if row is None:
            return None
        if not name.strip() or name.strip() == row["name"]:
            return row["name"]
        yeni = self._free_folder_name(name, exclude_id=folder_id)
        with self._write() as connection:
            connection.execute("UPDATE notebook_folders SET name = ? WHERE id = ?", (yeni, folder_id))
        return yeni

    def find_or_add_notebook_folder(self, name: str) -> int:
        """Aynı adda (büyük/küçük harf farkı gözetmeden) klasör varsa o, yoksa yenisi.

        Yüklenen notun klasörü için: arkadaşının "Sınav öncesi" klasörü,
        sende aynı adda klasör varsa oraya giriyor.
        """
        from .user_notes import name_key

        for folder in self.notebook_folders():
            if name_key(folder["name"]) == name_key(name.strip()):
                return folder["id"]
        return self.add_notebook_folder(name)

    def delete_notebook_folder(self, folder_id: int) -> None:
        """Klasörü siler; içindeki notlar patikalarının klasörüne döner.

        Dönen notun adı orada başka bir notta varsa sayılı hâlini alıyor:
        bir klasörde aynı adda iki not durmuyor.
        """
        with self._write() as connection:
            rows = connection.execute(
                "SELECT id, chapter_id, title FROM notebook_entries WHERE folder_id = ? "
                "ORDER BY created_at, id",
                (folder_id,),
            ).fetchall()
            for row in rows:
                ad = self._free_title(row["chapter_id"], row["title"], exclude_id=row["id"])
                connection.execute(
                    "UPDATE notebook_entries SET folder_id = NULL, title = ? WHERE id = ?",
                    (ad, row["id"]),
                )
            connection.execute("DELETE FROM notebook_folders WHERE id = ?", (folder_id,))

    def _free_folder_name(self, name: str, exclude_id: int | None = None) -> str:
        from .user_notes import FOLDER_MAX_LENGTH, name_key, unique_title

        rows = self._connection.execute(
            "SELECT name FROM notebook_folders WHERE id IS NOT ?", (exclude_id,)
        ).fetchall()
        return unique_title(name, {name_key(row["name"]) for row in rows}, FOLDER_MAX_LENGTH)

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
