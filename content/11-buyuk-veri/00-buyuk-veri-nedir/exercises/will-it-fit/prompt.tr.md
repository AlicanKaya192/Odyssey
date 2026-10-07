Bir bilgisayarın belleğine en fazla kaç satır sığacağını hesaplayan bir
fonksiyon yaz.

Belleğin tamamını tabloya veremezsin: işletim sistemi ve açık programlar da
yer tutuyor, pandas da hesap yaparken ara kopyalar açıyor. Bu alıştırmada
güvenli pay olarak tabloya **belleğin yarısını** ayırıyoruz.

**Yapman gerekenler:**

`max_rows(ram_gb, columns)` adında bir fonksiyon yaz:

1. Belleğin baytını bul: `ram_gb * 1024**3`.
2. Yarısını tabloya ayır.
3. Bir satırın baytını bul: her sütun 8 bayt.
4. Sığan satır sayısını **tam sayı** olarak döndür (`//`).

Örnekler:

- `max_rows(16, 10)` → `107374182`
- `max_rows(8, 4)` → `134217728`

16 GB'lık bir bilgisayara 10 sayı sütunlu yaklaşık 107 milyon satır
sığıyor. Metin sütunları işin içine girince bu sayı hızla düşer.
