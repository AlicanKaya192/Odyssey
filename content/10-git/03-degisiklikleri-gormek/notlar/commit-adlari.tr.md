Bir commit'i Git'e anlatmanın yolları. Hepsi `git show`, `git diff`,
`git log` gibi komutlarda hash'in yerine yazılabilir.

| Ad | Anlamı |
|---|---|
| `1158a1b7fc12…` | Tam hash (40 karakter). |
| `1158a1b` | Kısa hash; tek bir commit'e uyduğu sürece yeter (genellikle 7 karakter). |
| `HEAD` | Şu an bulunduğun commit. |
| `HEAD~1` | HEAD'in bir öncesi (ebeveyni). `HEAD~` de aynı. |
| `HEAD~3` | Üç öncesi. |
| `main` | `main` dalının son commit'i. |
| `main~2` | `main`'in son commit'inden iki önce. |
| `v1.0` | Bir etiketin gösterdiği commit (bölüm 13). |

## Hash neden böyle?

Hash commit'in içeriğinden (dosyalar, yazar, tarih, mesaj, önceki commit)
hesaplanan bir **parmak izi**. İki sonucu var:

- Aynı içerik her zaman aynı hash'i verir; farklı içerik farklı hash.
  Kimse bir commit'i hash'ini değiştirmeden sessizce değiştiremez.
- Bir commit'in hash'i ondan önceki commit'in hash'ine de bağlı. Geçmişte
  bir şey değişirse ondan sonraki her commit'in hash'i değişir. (12'de
  `rebase` ve `--amend` bunu yapacak.)

Bu yüzden dersteki hash'ler senin terminalinde başka çıkar: tarih ve yazar
farklı.

## `~` ile `^` farkı

`HEAD~2` "ilk ebeveynden iki adım geri" demek. `^` ise birleştirme
commit'lerinde hangi ebeveyn olduğunu seçer: `HEAD^1` birinci ebeveyn,
`HEAD^2` ikinci ebeveyn (birleştirilen dal). Birleştirmesi olmayan geçmişte
`HEAD^` ile `HEAD~` aynı şeydir. Birleştirmeyi 07'de göreceğiz.
