Birleştirme ile rebase arasında doğru ya da yanlış yok; ekip bir düzen seçer
ve ona uyar. Karar verirken bu sorular yardımcı olur.

| Soru | Merge | Rebase |
|---|---|---|
| Geçmiş nasıl görünür? | Gerçekte olduğu gibi: dallar ve birleşme noktaları | Düz bir çizgi, sanki her şey sırayla yapılmış |
| Commit'ler değişir mi? | Hayır | Evet, yeni hash'ler |
| Paylaşılmış dalda güvenli mi? | Evet | Hayır |
| Çakışma kaç kez çözülür? | Bir kez, birleştirmede | Her commit için ayrı ayrı olabilir |
| `git log` okuması | Birleştirme commit'leri kalabalık edebilir | Kolay |

## Sık görülen düzen

1. Özellik dalında çalış.
2. `main` ilerlediyse dalını güncel tut: `git fetch` + `git rebase origin/main`
   (dal yalnızca senindeyse) ya da `git merge origin/main`.
3. PR aç; GitHub'da birleştir (ekibin seçtiği yöntemle).
4. Kendi `main`'ini `git pull` ile güncelle (`pull.rebase true` ayarlıysa
   yerel commit'in yoksa fark etmez).

## Ne zaman kesinlikle merge?

- Dal başkalarıyla paylaşılıyorsa.
- `main`, `develop` gibi uzun ömürlü dalları birbirine katarken.
- Geçmişin "gerçekte ne oldu" bilgisini korumak önemliyse.

## Ne zaman rebase rahat?

- Henüz push etmediğin yerel commit'lerin varken `git pull --rebase`.
- Yalnızca senin çalıştığın bir dalı PR'dan önce temizlerken.
