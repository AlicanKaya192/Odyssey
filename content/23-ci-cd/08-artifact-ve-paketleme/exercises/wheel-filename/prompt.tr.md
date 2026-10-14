`wheel_filename(name, version)` fonksiyonunu yaz. Saf Python bir paketin tekerlek dosyasının adını döndürsün:

- Biçim: `ad-sürüm-py3-none-any.whl`
- Ad önce küçük harfe çevrilir.
- Addaki `-`, `_` ve `.` karakterleri `_` olur; art arda gelenler **tek** `_` olur (`a__b--c` → `a_b_c`).

`"My-Package"`, `"1.0"` → `"my_package-1.0-py3-none-any.whl"`

**Beklenen çıktı:**

```
greeter-0.1.0-py3-none-any.whl
my_package-1.0-py3-none-any.whl
data_tools-2.3.1-py3-none-any.whl
a_b_c-0.0.1-py3-none-any.whl
```
