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
    # --- Rust: derleyici hatalari (kod) ve panik mesajlari ------------------
    Rule("rustc", r"E0382", "mistake.rust_e0382"),
    Rule("rustc", r"E0499", "mistake.rust_e0499"),
    Rule("rustc", r"E0502", "mistake.rust_e0502"),
    Rule("rustc", r"E0505", "mistake.rust_e0505"),
    Rule("rustc", r"E0506", "mistake.rust_e0506"),
    Rule("rustc", r"E0384", "mistake.rust_e0384"),
    Rule("rustc", r"E0596", "mistake.rust_e0596"),
    Rule("rustc", r"E0308", "mistake.rust_e0308"),
    Rule("rustc", r"E0106", "mistake.rust_e0106"),
    Rule("rustc", r"E0597", "mistake.rust_e0597"),
    Rule("rustc", r"E0515", "mistake.rust_e0515"),
    Rule("rustc", r"E0373", "mistake.rust_e0373"),
    Rule("rustc", r"E0277", "mistake.rust_e0277"),
    Rule("rustc", r"E0599", "mistake.rust_e0599"),
    Rule("rustc", r"E0425", "mistake.rust_e0425"),
    Rule("rustc", r"E0433", "mistake.rust_e0433"),
    Rule("rustc", r"E0432", "mistake.rust_e0433"),
    Rule("rustc", r"E0004", "mistake.rust_e0004"),
    Rule("rustc", r"E0369", "mistake.rust_e0369"),
    Rule("rustc", r"E0061", "mistake.rust_e0061"),
    Rule("rustc", r"E0133", "mistake.rust_e0133"),
    Rule("rustc", r"E0282", "mistake.rust_e0282"),
    Rule("rustc", r"E0381", "mistake.rust_e0381"),
    Rule("rustc", r"E0601", "mistake.rust_e0601"),
    Rule("panic", r"index out of bounds", "mistake.rust_index"),
    Rule("panic", r"called `Option::unwrap\(\)` on a `None`", "mistake.rust_unwrap"),
    Rule("panic", r"called `Result::unwrap\(\)` on an `Err`", "mistake.rust_unwrap_err"),
    Rule("panic", r"divide by zero", "mistake.rust_divide"),
    Rule("panic", r"attempt to .* with overflow", "mistake.rust_overflow"),
    Rule("crash", r"C00000FD", "mistake.rust_stack"),
    Rule("crash", r"C0000005", "mistake.rust_access"),

    # --- None ile işlem (fonksiyon bir şey döndürmedi) ----------------------
    Rule("AttributeError", r"'NoneType' object has no attribute '(\w+)'", "mistake.none_attribute"),
    Rule("TypeError", r"'NoneType' object is not (subscriptable|iterable)", "mistake.none_value"),
    Rule("TypeError", r"object of type 'NoneType' has no len", "mistake.none_value"),

    # --- TypeError -------------------------------------------------------
    Rule("TypeError", r"can only concatenate str.*to str", "mistake.str_plus_int"),
    Rule("TypeError", r"unsupported operand type\(s\) for \+: 'int' and 'str'", "mistake.int_plus_str"),
    Rule("TypeError", r"can't multiply sequence by non-int", "mistake.str_times_str"),
    Rule("TypeError", r"'(\w+)' object is not callable", "mistake.not_callable"),
    Rule("TypeError", r"object is not subscriptable", "mistake.not_subscriptable"),
    Rule("TypeError", r"missing \d+ required positional argument", "mistake.missing_argument"),
    Rule("TypeError", r"takes \d+ positional arguments? but \d+ (was|were) given", "mistake.too_many_arguments"),
    Rule("TypeError", r"unsupported operand type\(s\) for (\S+): '(\w+)' and '(\w+)'", "mistake.unsupported_operand"),
    Rule("TypeError", r"'(\w+)' object is not iterable", "mistake.not_iterable"),
    Rule("TypeError", r"'(\w+)' object does not support item assignment", "mistake.immutable"),
    Rule("TypeError", r"got an unexpected keyword argument '(\w+)'", "mistake.unexpected_keyword"),

    # --- NameError -------------------------------------------------------
    Rule("NameError", r"name '(\w+)' is not defined", "mistake.undefined_name"),
    Rule("UnboundLocalError", r"local variable '(\w+)'", "mistake.unbound_local"),

    # --- SyntaxError -----------------------------------------------------
    Rule("SyntaxError", r"unterminated string literal", "mistake.unterminated_string"),
    Rule("SyntaxError", r"EOL while scanning string literal", "mistake.unterminated_string"),
    Rule("SyntaxError", r"expected ':'", "mistake.missing_colon"),
    Rule("SyntaxError", r"Maybe you meant '==' or ':=' instead of '='", "mistake.assign_in_condition"),
    Rule("SyntaxError", r"invalid syntax", "mistake.invalid_syntax"),
    Rule("SyntaxError", r"'\(' was never closed", "mistake.unclosed_bracket"),
    Rule("SyntaxError", r"'([\[{])' was never closed", "mistake.unclosed_other"),
    Rule("SyntaxError", r"unmatched '([)\]}])'", "mistake.unmatched_bracket"),
    Rule("SyntaxError", r"invalid decimal literal", "mistake.name_starts_with_digit"),
    Rule("SyntaxError", r"f-string: expecting '}'", "mistake.fstring_brace"),
    Rule("SyntaxError", r"cannot assign to literal", "mistake.assign_to_literal"),

    # --- Girinti ---------------------------------------------------------
    Rule("IndentationError", r"expected an indented block", "mistake.expected_indent"),
    Rule("IndentationError", r"unexpected indent", "mistake.unexpected_indent"),
    Rule("IndentationError", r"", "mistake.indentation"),
    Rule("TabError", r"", "mistake.tabs_and_spaces"),

    # --- Değer ve dönüşüm ------------------------------------------------
    Rule("ValueError", r"invalid literal for int\(\) with base 10: '(.*)'", "mistake.int_conversion"),
    Rule("ValueError", r"could not convert string to float: '(.*)'", "mistake.float_conversion"),
    Rule("ValueError", r"too many values to unpack \(expected (\d+), got (\d+)\)", "mistake.unpack_many"),
    Rule("ValueError", r"not enough values to unpack \(expected (\d+), got (\d+)\)", "mistake.unpack_few"),
    Rule("ZeroDivisionError", r"", "mistake.division_by_zero"),

    # --- Yineleme ve tükenen yineleyici ------------------------------------
    Rule("RecursionError", r"", "mistake.recursion"),
    Rule("StopIteration", r"", "mistake.stop_iteration"),

    # --- Dosyalar --------------------------------------------------------
    Rule("FileNotFoundError", r"No such file or directory: '(.*)'", "mistake.file_not_found"),
    Rule("PermissionError", r"Permission denied: '(.*)'", "mistake.permission"),

    # --- pandas ve scikit-learn ------------------------------------------
    Rule("ValueError", r"Length of values \((\d+)\) does not match length of index \((\d+)\)", "mistake.length_mismatch"),
    Rule("ValueError", r"Input( X| y)? contains NaN", "mistake.nan_input"),
    Rule("ValueError", r"inconsistent numbers of samples: \[(\d+), (\d+)\]", "mistake.sample_mismatch"),
    Rule("ValueError", r"Expected (2D array|a 2-dimensional)", "mistake.expected_2d"),

    # --- Dizin ve anahtar ------------------------------------------------
    Rule("IndexError", r"list index out of range", "mistake.index_out_of_range"),
    Rule("IndexError", r"(string|tuple) index out of range", "mistake.sequence_index"),
    Rule("KeyError", r"'(.*)'", "mistake.missing_key_named"),
    Rule("KeyError", r"", "mistake.missing_key"),
    Rule("AttributeError", r"'(\w+)' object has no attribute '(\w+)'", "mistake.no_attribute"),

    # --- Giriş bekleyen kod ----------------------------------------------
    Rule("EOFError", r"", "mistake.input_used"),

    # --- İçe aktarma -----------------------------------------------------
    Rule("ModuleNotFoundError", r"No module named '(\w+)'", "mistake.module_missing"),
    Rule("ImportError", r"cannot import name '(\w+)' from '([\w.]+)'", "mistake.cannot_import"),
    # Windows'un Akıllı Uygulama Denetimi imzasız bir kütüphane dosyasını
    # engelledi (mesaj Windows'un dilinde geliyor).
    Rule("ImportError", r"DLL load failed.*(Application Control|Uygulama Denetimi)", "mistake.blocked_by_windows"),

    # --- SQL: sunucuya ulaşılamıyor --------------------------------------
    #
    # Bu ikisi öğrencinin kodundan kaynaklanmıyor: makinede MSSQL ya da
    # ODBC sürücüsü yok. Ham mesaj ("driver_missing") hiçbir şey
    # anlatmıyor, o yüzden ne yapılacağı yazılıyor.
    Rule("SqlUnavailable", r"driver_missing", "mistake.sql_driver_missing"),
    Rule("SqlUnavailable", r"server_missing", "mistake.sql_server_missing"),

    # --- SQL: sorgunun kendisi -------------------------------------------
    Rule("SqlError", r"Invalid object name '([^']+)'", "mistake.sql_no_table"),
    Rule("SqlError", r"Invalid column name '([^']+)'", "mistake.sql_no_column"),
    Rule("SqlError", r"is invalid in the select list because it is not contained in either an aggregate function or the GROUP BY", "mistake.sql_group_by"),
    Rule("SqlError", r"An aggregate may not appear in the WHERE clause",
         "mistake.sql_aggregate_in_where"),
    Rule("SqlError", r"Incorrect syntax near '([^']+)'", "mistake.sql_syntax"),
    Rule("SqlError", r"Ambiguous column name '([^']+)'", "mistake.sql_ambiguous"),
    Rule("SqlError", r"Conversion failed when converting", "mistake.sql_conversion"),
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
