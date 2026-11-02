İlkeler kodda çoğu zaman tek bir satırın farkıdır. Aşağıdaki her çiftte
üstteki ilkeyi çiğniyor, alttaki uyguluyor.

## Bilinmeyen kullanıcı

```python
allowed = rules.get(user, ["read", "write"])
allowed = rules.get(user, [])
```

İlk satır listede olmayan kullanıcıya varsayılan olarak yetki veriyor.
İkincisi boş liste veriyor: söylenmeyen her şey yasak.

## Hata durumunda

```python
try:
    ok = check_permission(user, item)
except Exception:
    ok = True
```

```python
try:
    ok = check_permission(user, item)
except Exception:
    ok = False
```

Hata yakalanınca ne döndürüldüğüne bak. Emin olamıyorsan reddet ve hatayı
kayda geçir.

## Biçim denetimi

```python
if not name.endswith(".exe"):
    save(name)
```

```python
if name.rsplit(".", 1)[-1].lower() in {"pdf", "png", "jpg"}:
    save(name)
```

İlki engel listesi, ikincisi izin listesi. İkincide `lower()` var:
`PHOTO.PNG` da kabul edilsin, `.PNG` ile `.png` farklı sayılmasın.

## Ayarların varsayılanı

```python
debug = settings.get("debug", True)
debug = settings.get("debug", False)
```

Ayar dosyasında satır yoksa sistemin güvenli tarafta kalması gerekir.
Hata ayıklama kipi çoğu zaman iç bilgileri (yollar, sürümler, sorgular)
ekrana döker.

## Basitlik

Bir izin kuralı birçok iç içe `if` ile büyüyorsa onu bir tabloya çevir:
kimin neye izni olduğu bir sözlükte yazsın, kod yalnızca tabloya baksın.
Tabloyu okumak koddaki dallanmaları izlemekten kolaydır.
