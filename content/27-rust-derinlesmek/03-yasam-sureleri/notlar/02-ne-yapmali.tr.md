## Ömür hatası alınca sırayla sor

1. **Dönen şeyin sahibi kim olmalı?** Fonksiyon yeni bir değer üretiyorsa referans değil sahipli tür döndür.
2. **Dönen referans hangi girdiden geliyor?** Yalnızca onu işaretle.
3. **Struct gerçekten referans tutmalı mı?** Çoğu zaman `String` daha basit.
4. **Son çare `clone`:** Küçük veride kabul edilebilir, hata değildir.

## Sahipli mi, referans mı?

| Durum | Seçim |
|---|---|
| Girdinin bir parçasını döndürüyorsun | `&str` |
| Yeni metin üretiyorsun | `String` |
| Struct uzun yaşayacak | `String` alan |
| Çok büyük metinde kısa süreli görünüm | `&'a str` alan |

## Uygulama: Kelimeler

Girdinin parçalarını kopyasız tutan bir yapı:

```rust
#[derive(Debug)]
struct Token<'a> {
    text: &'a str,
    position: usize,
}

fn tokens(line: &str) -> Vec<Token<'_>> {
    let mut found = Vec::new();
    for (position, text) in line.split_whitespace().enumerate() {
        found.push(Token { text, position });
    }
    found
}

fn main() {
    let line = String::from("go rust");
    for t in tokens(&line) {
        println!("{} {}", t.position, t.text);
    }
}
```

```text
0 go
1 rust
```

Her `Token` özgün metne işaret ediyor, tek bayt kopyalanmadı. Bedeli: `text` silinmeden `tokens` yaşayamaz.

## Yanlış çözümler

| Görülen | Neden yanlış |
|---|---|
| Her yere `'static` | Yerel değer `'static` olmaz, hata başka yere kayar |
| `'a` ekleyip yerel referans döndürmek | İşaret değeri yaşatmaz |
| Gereksiz yere `<'a>` | Çıkarım zaten yapıyor; `cargo clippy` söyler |
