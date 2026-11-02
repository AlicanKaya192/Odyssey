grep'in en çok kullanılan biçimleri, bir bakışta.

## Temel

| Yazım | Ne yapar |
|---|---|
| `grep 'desen' f` | f'de deseni taşıyan satırlar |
| `grep 'desen' f1 f2` | Birden çok dosya; satırın başında dosya adı |
| <code>komut &#124; grep 'desen'</code> | Komutun çıktısını süzer |
| `grep -r 'desen' klasör` | Klasör ve alt klasörlerinde |

## Seçenekler

| Seçenek | Ne yapar |
|---|---|
| `-i` | Büyük/küçük harf farkı yok |
| `-n` | Satır numarası (`3:...`) |
| `-c` | Eşleşen satır sayısı |
| `-v` | Eşleşmeyen satırlar |
| `-w` | Yalnızca tam kelime |
| `-x` | Yalnızca tam satır |
| `-o` | Yalnızca eşleşen parça |
| `-l` | Yalnızca dosya adları |
| `-E` | Genişletilmiş ifade |
| `-r` | Alt klasörlere in |

Birleştirilebilir: `-in`, `-ic`, `-rl`, `-vi`.

## Çıkış kodu

| Kod | Anlamı |
|---|---|
| 0 | En az bir satır bulundu |
| 1 | Hiç bulunamadı |
| 2 | Hata (dosya yok, desen bozuk) |

## Sık kalıplar

- Kaç hata var: `grep -ic error app.log`
- Hata ve uyarılar: `grep -E 'ERROR|WARN' app.log`
- Bilgi dışındakiler: `grep -vi info app.log`
- Hangi dosyalarda: `grep -rl 'TODO' .`
