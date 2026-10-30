## Panik her yerden çıkabilir

`T::clone`, `T::drop`, kullanıcının verdiği kapanış: Hepsi panik yapabilir. Elle bellek yöneten kod, bu noktaların her birinde programın geçerli durumda olmasını sağlamalıdır.

| Seviye | Söz |
|---|---|
| Sızıntı olabilir | Yalnızca kaynak kaybı; tanımsız davranış yok |
| Değişmez korunur | Yapı kullanılabilir kalır |
| Tam geri alma | Hiçbir şey olmamış gibi |

Tanımsız davranış **hiçbir** seviyede kabul edilmez. Sızıntı kabul edilebilir.

## Sık yapılan hata

```rust
// Wrong order: the length grows before the value is written.
self.len += 1;
let value = make_value();
ptr::write(self.ptr.add(self.len - 1), value);
```

`make_value` panik yaparsa uzunluk artmış ama yer boştur. Yapı düşürülürken boş yeri de düşürmeye kalkar: Tanımsız davranış. Doğru sıra önce değeri üretmek, sonra yazmak, **en son** uzunluğu artırmaktır.

## Koruyucu kalıbı

Yarım işi geri almak için bir değer tut; `Drop`'u işi toparlasın. Başarılı olursa `mem::forget` ile koruyucuyu sustur:

```rust
struct Guard<'a> {
    list: &'a mut Vec<i32>,
    original_len: usize,
}

impl Drop for Guard<'_> {
    fn drop(&mut self) {
        self.list.truncate(self.original_len);
    }
}
```

## Kural

Elle bellek işinde kendine sor: "Şu satır panik yaparsa yapı düşürüldüğünde ne olur?" Cevap "bilmiyorum" ise sıra yanlıştır.
