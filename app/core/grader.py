"""Çalıştırma sonuçlarını insanın okuyabileceği geri bildirime çevirir.

`runner.py` ham veri döndürür: hangi kontrol tuttu, beklenen neydi, bulunan
neydi. Burada bunlar seçili dilde anlaşılır cümlelere dönüşür.

Hepsi şablon metin — değerlendirmede hiçbir dış servis kullanılmıyor.
Alıştırma tanımında `hint` verilmişse genel mesaj yerine o gösterilir, çünkü
göreve özel yazılmış ipucu her zaman daha yararlıdır.
"""

from __future__ import annotations

from dataclasses import dataclass

from .language import LanguageManager
from .runner import CheckResult, RunResult


@dataclass
class Feedback:
    """Kullanıcıya gösterilecek tek bir geri bildirim satırı."""

    passed: bool
    message: str
    expected: str = ""
    actual: str = ""

    @property
    def has_comparison(self) -> bool:
        return bool(self.expected or self.actual)


def _hint_or(language: LanguageManager, check: CheckResult, fallback_key: str) -> str:
    """Göreve özel ipucu varsa onu, yoksa genel mesajı döndürür."""
    hint = language.pick(check.hint)
    return hint or language.t(fallback_key)


def describe_check(check: CheckResult, language: LanguageManager) -> Feedback:
    """Tek bir kontrolü cümleye çevirir."""
    detail = check.detail

    if check.passed:
        return Feedback(passed=True, message=language.t("check.passed"))

    if check.type == "stdout":
        return Feedback(
            passed=False,
            message=language.t("check.stdout.failed"),
            expected=detail.get("expected", ""),
            actual=detail.get("actual", ""),
        )

    if check.type == "variable":
        name = detail.get("name", "")
        if detail.get("missing"):
            return Feedback(
                passed=False,
                message=language.t("check.variable.missing", name=name),
            )
        return Feedback(
            passed=False,
            message=language.t(
                "check.variable.failed",
                name=name,
                expected=detail.get("expected", ""),
                actual=detail.get("actual", ""),
            ),
        )

    if check.type == "function":
        name = detail.get("name", "")
        if detail.get("missing"):
            return Feedback(
                passed=False,
                message=language.t("check.function.missing", name=name),
            )
        if detail.get("raised"):
            return Feedback(
                passed=False,
                message=language.t(
                    "check.function.raised",
                    name=name,
                    args=detail.get("args", ""),
                    error=detail.get("raised", ""),
                ),
            )
        return Feedback(
            passed=False,
            message=language.t(
                "check.function.failed",
                name=name,
                args=detail.get("args", ""),
                expected=detail.get("expected", ""),
                actual=detail.get("actual", ""),
            ),
        )

    if check.type == "ast_require":
        return Feedback(
            passed=False,
            message=_hint_or(language, check, "check.ast_require.failed"),
        )

    if check.type == "ast_forbid":
        return Feedback(
            passed=False,
            message=_hint_or(language, check, "check.ast_forbid.failed"),
        )

    return Feedback(passed=False, message=language.t("check.failed"))


def summarise(result: RunResult, language: LanguageManager) -> str:
    """Sonucun tek cümlelik özeti."""
    if result.status == "timeout":
        return language.t("exercise.timeout", seconds=result.timeout_sec)

    if result.status == "crashed":
        return language.t("exercise.error")

    if result.status == "error":
        error = result.error or {}
        line = error.get("line")
        message = f"{error.get('type', '')}: {error.get('message', '')}".strip(": ")
        if line:
            return f"{language.t('exercise.error')}  ({message} — satır {line})"
        return f"{language.t('exercise.error')}  ({message})"

    if result.passed:
        return language.t("exercise.passed")

    return language.t("exercise.failed")


def describe(result: RunResult, language: LanguageManager) -> list[Feedback]:
    """Bütün kontrolleri sırayla geri bildirime çevirir.

    Zaman aşımında kontrol listesi boş döner: o durumu `summarise()` zaten
    tek cümleyle anlatıyor, aynı metni iki kere göstermenin anlamı yok.
    """
    if result.status == "timeout":
        return []

    return [describe_check(check, language) for check in result.checks]


def diff_lines(expected: str, actual: str) -> list[tuple[str, str, str]]:
    """Beklenen ve bulunan çıktıyı satır satır eşler.

    Her satır için (işaret, beklenen, bulunan) döndürür. İşaret "=" ise satır
    aynı, "!" ise farklı. Arayüz bunu iki sütun hâlinde gösterir.
    """
    expected_lines = expected.splitlines()
    actual_lines = actual.splitlines()
    total = max(len(expected_lines), len(actual_lines))

    rows = []
    for index in range(total):
        left = expected_lines[index] if index < len(expected_lines) else ""
        right = actual_lines[index] if index < len(actual_lines) else ""
        rows.append(("=" if left.strip() == right.strip() else "!", left, right))
    return rows
