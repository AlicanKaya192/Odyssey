`trait Label { fn label(&self) -> String; }` yaz ve `Debug` sağlayan **her tür** için tek bir `impl` ile uygula: Sonuç `<{:?}>` biçiminde olsun. Örnek: `5.label()` → `<5>`.
