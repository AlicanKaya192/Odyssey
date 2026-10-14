**actions/cache**

| Ayar | Anlamı |
|---|---|
| `path` | Saklanacak klasör (pip için `~/.cache/pip`) |
| `key` | Tam anahtar; içerik değişince değişmeli |
| `restore-keys` | Yedek önekler; tam anahtar yoksa en yeni eşleşen |

**Sonuçlar**

| Durum | Ne olur |
|---|---|
| hit | Tam anahtar bulundu; klasör geri yüklenir, iş sonunda yeniden saklanmaz |
| partial | Önek tuttu; en yeni eşleşen geri yüklenir, iş sonunda yeni anahtarla saklanır |
| miss | Hiçbiri; her şey indirilir, iş sonunda saklanır |

**İyi anahtar**

```text
pip-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
```

- Araç adı (`pip`): başka önbelleklerle karışmasın.
- `runner.os`: işletim sistemleri karışmasın.
- `hashFiles(...)`: bağımlılık değişince yeni anahtar.

**Kısa yol**

```yaml
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: pip
```

**Sınırlar**

- Depo başına varsayılan 10 GB; 7 gün kullanılmayan silinir.
- Dala bağlı: dal + varsayılan dal; PR hedef dalınkini okur.
- Gizli değer önbelleğe konmaz.
- Önbellek boşken de iş doğru çalışmalı.

**concurrency**

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

| Ayar | Anlamı |
|---|---|
| `group` | Aynı gruptaki çalışmalardan biri sürer |
| `cancel-in-progress: true` | Yeni gelince eskisi iptal (test hatları) |
| `cancel-in-progress: false` | Yeni, eskisinin bitmesini bekler (dağıtım) |
