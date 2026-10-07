`ARG` yalnızca derlemede geçerli; çalışırken de gerekiyorsa `ENV`'e
aktarılıyor.

**Yapman gerekenler:**

1. `VERSION` adında, varsayılanı `1.0` olan bir `ARG` tanımla.
2. Değerini `ENV APP_VERSION=$VERSION` ile çalışma zamanına aktar.

Odyssey imajı iki kez kuracak: argümansız ve `--build-arg VERSION=2.4` ile.

**Beklenen çıktılar:**

```
version 1.0
version 2.4
```
