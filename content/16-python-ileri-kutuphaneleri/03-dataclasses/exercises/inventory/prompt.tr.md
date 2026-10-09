`Inventory` dataclass'ı: `owner: str` ve `items: dict[str, int]`. Her
nesnenin **kendi** sözlüğü olmalı (`field(default_factory=dict)`). `add(name,
count)` metodu adedi eklesin (yoksa 0'dan başlasın). Başlangıç kodu sözlüğü
paylaştırıyor; çıktıya bak.

**Beklenen çıktı:**

```
Inventory(owner='ada', items={'pen': 5})
Inventory(owner='alan', items={})
```
