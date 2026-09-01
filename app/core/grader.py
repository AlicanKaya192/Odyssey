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
            # Dogru degeri baska bir adla tutuyorsa bunu soyluyoruz. Islem
            # dogru, yalnizca ad tutmuyor; bunu ayirt etmeyen bir mesaj
            # kisiyi bastan cozmeye itiyordu.
            benzer = detail.get("lookalike")
            if benzer:
                return Feedback(
                    passed=False,
                    message=language.t(
                        "check.variable.renamed", name=name, found=benzer
                    ),
                )
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

    if check.type == "method":
        # Sinif alistirmalarinda dusme sebepleri cok cesitli: sinif hic yok,
        # kurucu patliyor, metot eksik, donus yanlis. Hepsi "sinif calismadi"
        # diye ozetlenirse kisi nereye bakacagini bilemiyor.
        cls = detail.get("cls", "")
        if detail.get("missing"):
            return Feedback(passed=False, message=language.t("check.method.missing", name=cls))
        if detail.get("not_class"):
            return Feedback(passed=False, message=language.t("check.method.not_class", name=cls))
        if detail.get("init_raised"):
            return Feedback(
                passed=False,
                message=language.t(
                    "check.method.init_raised", name=cls,
                    args=detail.get("args", ""), error=detail.get("init_raised", ""),
                ),
            )
        attribute = detail.get("attribute")
        if attribute:
            if detail.get("no_member"):
                return Feedback(
                    passed=False,
                    message=language.t("check.method.no_attribute", name=cls, attribute=attribute),
                )
            return Feedback(
                passed=False,
                message=language.t(
                    "check.method.attribute_failed", name=cls, attribute=attribute,
                    expected=detail.get("expected", ""), actual=detail.get("actual", ""),
                ),
            )
        method = detail.get("method", "")
        if detail.get("no_member"):
            return Feedback(
                passed=False,
                message=language.t("check.method.no_method", name=cls, method=method),
            )
        if detail.get("raised"):
            return Feedback(
                passed=False,
                message=language.t(
                    "check.method.raised", name=cls, method=method,
                    args=detail.get("args", ""), error=detail.get("raised", ""),
                ),
            )
        return Feedback(
            passed=False,
            message=language.t(
                "check.method.failed", name=cls, method=method,
                args=detail.get("args", ""),
                expected=detail.get("expected", ""), actual=detail.get("actual", ""),
            ),
        )

    if check.type == "annotation":
        # Belirtim kontrolu birden cok sekilde dusebiliyor; her biri farkli
        # bir seyi yanlis yapiyor ve mesajin bunu ayirt etmesi gerekiyor.
        # "Belirtim eksik" ile "yanlis tip yazmissin" ayni cumle olursa kisi
        # neye bakacagini bilemiyor.
        if detail.get("unparsed"):
            return Feedback(passed=False, message=language.t("check.annotation.unparsed"))

        variable = detail.get("variable")
        if variable:
            if detail.get("bare"):
                return Feedback(
                    passed=False,
                    message=language.t(
                        "check.annotation.variable_bare",
                        name=variable,
                        expected=detail.get("expected", ""),
                    ),
                )
            return Feedback(
                passed=False,
                message=language.t(
                    "check.annotation.variable_wrong",
                    name=variable,
                    expected=detail.get("expected", ""),
                    actual=detail.get("actual", ""),
                ),
            )

        name = detail.get("name", "")
        if detail.get("missing"):
            return Feedback(
                passed=False,
                message=language.t("check.function.missing", name=name),
            )
        if detail.get("no_param"):
            return Feedback(
                passed=False,
                message=language.t(
                    "check.annotation.no_param", name=name, param=detail.get("param", "")
                ),
            )
        if detail.get("returns"):
            key = "return_bare" if detail.get("bare") else "return_wrong"
            return Feedback(
                passed=False,
                message=language.t(
                    f"check.annotation.{key}",
                    name=name,
                    expected=detail.get("expected", ""),
                    actual=detail.get("actual", ""),
                ),
            )
        key = "param_bare" if detail.get("bare") else "param_wrong"
        return Feedback(
            passed=False,
            message=language.t(
                f"check.annotation.{key}",
                name=name,
                param=detail.get("param", ""),
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
    """Sonuç panelinde gösterilecek geri bildirimleri döndürür.

    **Yalnızca düşen kontroller listeleniyor.** Önce her kontrol için bir
    satır çiziliyordu; bir alıştırmada altıya kadar kontrol olduğu için
    geçen bir çözümde alt alta altı tane "Geçti" satırı beliriyordu. Aynı
    şeyi altı kez söylemek bilgi vermiyor, yalnızca yer kaplıyor ve asıl
    bakılacak yeri — çıktıyı — aşağı itiyor.

    Hepsi geçtiyse tek bir satır yeterli. Bir şey düştüyse yalnızca o
    satır(lar) gösteriliyor; geçenleri de listelemek, düzeltilecek yeri
    aramaya çeviriyordu.

    Zaman aşımında liste boş dönüyor: o durumu `summarise()` zaten tek
    cümleyle anlatıyor, aynı metni iki kere göstermenin anlamı yok.
    """
    # Kod hiç çalışmadıysa kontroller bilgi vermiyor, üstelik yanıltıyor:
    # söz dizimi hatası olan bir çözümde "Book adında bir sınıf
    # tanımlamamışsın" yazıyordu — oysa kişi sınıfı yazmış, yalnızca iki
    # nokta unutmuş. Asıl söylenecek şeyi (hata türü ve satır numarası)
    # `summarise()` ve `mistakes.explain()` zaten söylüyor.
    if result.status != "ok":
        return []

    failed = _unique(
        describe_check(check, language)
        for check in result.checks
        if not check.passed
    )
    if failed:
        return failed

    # Düşen kontrol yok. Tek satırı yalnızca alıştırma gerçekten geçtiyse
    # gösteriyoruz.
    if result.passed:
        return [Feedback(passed=True, message=language.t("check.passed"))]

    return []


def _unique(feedbacks) -> list[Feedback]:
    """Aynı cümleyi bir kez gösterir.

    Bir sınıfa üç ayrı `method` kontrolü yazılmışsa ve sınıf hiç yoksa,
    üçü de aynı cümleyi üretiyor. Aynı şeyi üç kez söylemek bilgi vermiyor.
    Karşılaştırmalı satırlar (beklenen/bulunan) ayrı sayılıyor; ikisinin
    metni aynı olsa da içerikleri farklı olabiliyor.
    """
    seen = set()
    result = []
    for feedback in feedbacks:
        key = (feedback.message, feedback.expected, feedback.actual)
        if key in seen:
            continue
        seen.add(key)
        result.append(feedback)
    return result


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
