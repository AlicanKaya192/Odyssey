"""Sık yapılan hataları açıklayan katman.

Python'un hata mesajları doğru ama öğretmiyor. `can only concatenate str
(not "int") to str` cümlesi yeni başlayan birine hiçbir şey anlatmıyor.

Burada hata tipi ve mesajına bakıp "bu ne demek, neden oldu, nasıl
düzeltilir" açıklaması üretiliyor. Hepsi önceden yazılmış eşleştirmeler;
hiçbir dış servis kullanılmıyor.

Yeni bir kalıp eklemek için `RULES` listesine bir satır yazmak yeterli.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Explanation:
    """Bir hataya karşılık gelen açıklama."""

    key: str          # i18n anahtarı
    values: dict      # metindeki yer tutucular


@dataclass(frozen=True)
class Rule:
    """Hata tipi ve mesaj kalıbından açıklamaya eşleme."""

    error_type: str
    pattern: str
    key: str

    def match(self, error_type: str, message: str) -> re.Match | None:
        if self.error_type and self.error_type != error_type:
            return None
        return re.search(self.pattern, message, re.IGNORECASE)


# Sıra önemli: ilk eşleşen kural kazanır, özel kalıplar genel olanlardan önce.
RULES: list[Rule] = [
    # --- TypeError -------------------------------------------------------
    Rule("TypeError", r"can only concatenate str.*to str", "mistake.str_plus_int"),
    Rule("TypeError", r"unsupported operand type\(s\) for \+: 'int' and 'str'", "mistake.int_plus_str"),
    Rule("TypeError", r"can't multiply sequence by non-int", "mistake.str_times_str"),
    Rule("TypeError", r"'(\w+)' object is not callable", "mistake.not_callable"),
    Rule("TypeError", r"object is not subscriptable", "mistake.not_subscriptable"),
    Rule("TypeError", r"missing \d+ required positional argument", "mistake.missing_argument"),
    Rule("TypeError", r"takes \d+ positional arguments? but \d+ (was|were) given", "mistake.too_many_arguments"),

    # --- NameError -------------------------------------------------------
    Rule("NameError", r"name '(\w+)' is not defined", "mistake.undefined_name"),

    # --- SyntaxError -----------------------------------------------------
    Rule("SyntaxError", r"unterminated string literal", "mistake.unterminated_string"),
    Rule("SyntaxError", r"EOL while scanning string literal", "mistake.unterminated_string"),
    Rule("SyntaxError", r"expected ':'", "mistake.missing_colon"),
    Rule("SyntaxError", r"invalid syntax", "mistake.invalid_syntax"),
    Rule("SyntaxError", r"'\(' was never closed", "mistake.unclosed_bracket"),
    Rule("SyntaxError", r"cannot assign to literal", "mistake.assign_to_literal"),

    # --- Girinti ---------------------------------------------------------
    Rule("IndentationError", r"expected an indented block", "mistake.expected_indent"),
    Rule("IndentationError", r"unexpected indent", "mistake.unexpected_indent"),
    Rule("IndentationError", r"", "mistake.indentation"),
    Rule("TabError", r"", "mistake.tabs_and_spaces"),

    # --- Değer ve dönüşüm ------------------------------------------------
    Rule("ValueError", r"invalid literal for int\(\) with base 10: '(.*)'", "mistake.int_conversion"),
    Rule("ZeroDivisionError", r"", "mistake.division_by_zero"),

    # --- Dizin ve anahtar ------------------------------------------------
    Rule("IndexError", r"list index out of range", "mistake.index_out_of_range"),
    Rule("KeyError", r"", "mistake.missing_key"),
    Rule("AttributeError", r"'(\w+)' object has no attribute '(\w+)'", "mistake.no_attribute"),

    # --- Giriş bekleyen kod ----------------------------------------------
    Rule("EOFError", r"", "mistake.input_used"),

    # --- İçe aktarma -----------------------------------------------------
    Rule("ModuleNotFoundError", r"No module named '(\w+)'", "mistake.module_missing"),
]


def explain(error: dict | None) -> Explanation | None:
    """Hata bilgisine karşılık gelen açıklamayı bulur.

    `error`, `runner.RunResult.error` sözlüğüdür. Eşleşme bulunamazsa None
    döner ve arayüz yalnızca ham hata mesajını gösterir — uydurma bir
    açıklama üretmektense hiçbir şey söylememek daha dürüst.
    """
    if not error:
        return None

    error_type = error.get("type", "")
    message = error.get("message", "")

    for rule in RULES:
        found = rule.match(error_type, message)
        if found is None:
            continue

        values: dict[str, str] = {}
        # Kalıptaki yakalama grupları name1, name2... olarak aktarılıyor.
        for index, group in enumerate(found.groups(), start=1):
            values[f"name{index}"] = group or ""

        return Explanation(key=rule.key, values=values)

    return None
