## optimize

| Yazım | Soru |
|---|---|
| `minimize_scalar(f, bounds=(a, b), method="bounded")` | tek değişkenin en küçüğü |
| `minimize(f, x0=[...])` | çok değişkenin en küçüğü |
| `minimize(..., method="Nelder-Mead")` | türevsiz yöntem |
| `minimize(..., bounds=[(0, 1)] * n)` | her değişkene sınır |
| `minimize(..., constraints=[{"type": "eq", "fun": g}])` | `g(x) = 0` kısıtı |
| `curve_fit(model, x, y, p0=[...])` | model parametreleri + `cov` |
| `root_scalar(f, bracket=[a, b])` | `f(x) = 0` (uçlarda zıt işaret) |
| `linprog(c, A_ub=, b_ub=, bounds=)` | doğrusal kısıtlı en küçükleme |

## Sonuç nesnesi

| Alan | Ne |
|---|---|
| `res.x` | çözüm |
| `res.fun` | çözümdeki değer |
| `res.success` / `res.status` | başarılı mı |
| `res.message` | açıklama |
| `res.nit`, `res.nfev` | adım ve fonksiyon çağrısı sayısı |

## interpolate

| Yazım | Özellik |
|---|---|
| `np.interp(x, xs, ys)` | doğrusal; aralık dışında uç değeri tekrarlar |
| `CubicSpline(xs, ys)` | yumuşak; aşabilir, dışarıda eğriyi uzatır |
| `PchipInterpolator(xs, ys)` | yumuşak ve aşmaz |
| `make_interp_spline(xs, ys, k=3)` | genel spline |

## Tuzaklar

| Belirti | Sebep |
|---|---|
| "En büyük" yerine en küçüğü buldu | scipy en küçükler; eksisini ver |
| Farklı başlangıç, farklı cevap | yerel en küçük; çok başlangıç dene |
| Hepsi sıfır çıktı | kısıt unutuldu |
| `f(a) and f(b) must have different signs` | `bracket` içinde kök yok |
| `curve_fit` saçma değer verdi | kötü `p0` |
| Ölçülmemiş bir tepe / çukur | spline aştı; `Pchip` |
