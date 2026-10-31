"""Paketli Rust alıştırmalarının derleme önbelleği: boyutu ve temizliği.

serde, clap ve tokio ilk alıştırmada derleniyor ve sonuçları bu klasörde
kalıyor (~150 MB, ölçüldü). Silmek ilerlemeyi etkilemez, yalnızca sonraki
alıştırma paketleri yeniden derler.
"""

from __future__ import annotations

import shutil

from ..paths import rust_build_dir


def size_mb() -> float:
    folder = rust_build_dir()
    if not folder.is_dir():
        return 0.0
    return sum(f.stat().st_size for f in folder.rglob("*") if f.is_file()) / (1024 * 1024)


def clear() -> None:
    shutil.rmtree(rust_build_dir(), ignore_errors=True)
