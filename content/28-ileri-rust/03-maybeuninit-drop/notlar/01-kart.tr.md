## Üç araç

| Araç | İçi geçerli mi | Kapsam sonunda düşer mi |
|---|---|---|
| `T` | Evet | Evet |
| `MaybeUninit<T>` | Söz yok | Hayır |
| `ManuallyDrop<T>` | Evet | Hayır |

## Çağrılar

| Çağrı | İş | `unsafe` mi |
|---|---|---|
| `MaybeUninit::uninit()` | Boş yer | Hayır |
| `MaybeUninit::new(v)` | Dolu yer | Hayır |
| `m.write(v)` | Yaz, eskiyi düşürme | Hayır |
| `m.assume_init()` | `T`'ye çevir | Evet |
| `m.assume_init_ref()` | `&T` | Evet |
| `m.assume_init_drop()` | Yerinde düşür | Evet |
| `ManuallyDrop::new(v)` | Sar | Hayır |
| `ManuallyDrop::drop(&mut m)` | Şimdi düşür | Evet |
| `ManuallyDrop::into_inner(m)` | Geri al | Hayır |
| `mem::forget(v)` | Hiç düşürme | Hayır |

`mem::forget` güvenlidir, çünkü sızıntı Rust'ta tanımsız davranış değildir. Yalnızca kötüdür.

## Eski yol

`mem::uninitialized()` ve `mem::zeroed()` eski kodda görülür. Birincisi kullanımdan kalktı. İkincisi `T` için sıfır geçerli değilse tanımsız davranıştır: `&T`, `Box<T>`, `NonNull<T>` gibi.

## Elle işlerken kontrol

| Soru | Yanlış olursa |
|---|---|
| Her dolu yer tam bir kez düşüyor mu? | Sızıntı ya da iki kez silme |
| Okumadan önce yazıldı mı? | Tanımsız davranış |
| Panikte durum geçerli mi? | İki kez silme olabilir |
