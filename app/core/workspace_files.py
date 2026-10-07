"""Çok dosyalı alıştırmanın dosyaları: dil, ad denetimi ve kayıt biçimi.

Tek dosyalı alıştırmada kişinin kodu `exercise_progress.code` sütununda düz
metin olarak duruyor. Çok dosyalı alıştırmada (API, Docker) bütün dosyalar
tek kayıtta, JSON olarak: ``{"files": {"main.py": "...", "models.py": "..."}}``.
Problemin cevapları da aynı sütunda JSON; ilerleme ve rozet hesabı türleri
ayırt etmiyor.
"""

from __future__ import annotations

import json
from pathlib import PurePosixPath

# Dosya adından editör dili. Tanınmayan uzantı düz metin (renk yok).
SUFFIX_LANGUAGES = {
    ".py": "python",
    ".sql": "tsql",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".sh": "shell",
    ".json": "json",
    ".toml": "toml",
    ".ini": "toml",
    ".cfg": "toml",
}
# Uzantısız ya da uzantısı dili söylemeyen adlar.
NAME_LANGUAGES = {
    "dockerfile": "dockerfile",
    ".dockerignore": "toml",
    ".env": "toml",
}

# Çalışma klasöründe denetleyicinin kendi dosyaları; alıştırma dosyası bu
# adları alamaz (`api_routes.py` API alıştırmasının sunucusu).
RESERVED_NAMES = {"job.json", "result.json", "seed.sql", "api_routes.py"}


def file_language(name: str) -> str:
    """Dosyanın editör dili: `python`, `yaml`, `dockerfile`, ... ya da `text`."""
    path = PurePosixPath(name)
    lower = path.name.lower()
    if lower in NAME_LANGUAGES:
        return NAME_LANGUAGES[lower]
    # `Dockerfile.dev`, `api.Dockerfile` gibi adlar da Dockerfile.
    if lower.startswith("dockerfile") or lower.endswith(".dockerfile"):
        return "dockerfile"
    return SUFFIX_LANGUAGES.get(path.suffix.lower(), "text")


def safe_name(name: str) -> bool:
    """Ad çalışma klasörünün içinde kalan, göreli bir dosya yolu mu.

    Alt klasör olabilir (`app/models.py`); `..`, mutlak yol, sürücü harfi
    ve ters bölü olamaz: dosya geçici klasörün dışına yazılmasın.
    """
    if not name or "\\" in name or ":" in name or name.startswith("/"):
        return False
    parts = PurePosixPath(name).parts
    if any(part in ("", ".", "..") for part in parts):
        return False
    return name not in RESERVED_NAMES


def encode(files: dict[str, str]) -> str:
    """Dosyaları tek kayda çevirir (sıra korunuyor)."""
    return json.dumps({"files": files}, ensure_ascii=False)


def decode(saved: str) -> dict[str, str] | None:
    """Kayıttaki dosyalar; kayıt bu biçimde değilse `None`.

    `None` dönmesi "kayıt yok" demek değil: alıştırma sonradan çok dosyalı
    olduysa eski kayıt düz kod olabilir, çağıran onu giriş dosyasına koyar.
    """
    if not saved or not saved.lstrip().startswith("{"):
        return None
    try:
        value = json.loads(saved)
    except ValueError:
        return None
    files = value.get("files") if isinstance(value, dict) else None
    if not isinstance(files, dict):
        return None
    return {str(name): str(text) for name, text in files.items()}
