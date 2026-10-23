"1 ile 100 arasında bir sayı tuttum... Hangisi?"

Şu programı yaz:

- Kullanıcıdan bir seviye (`n`) ister; pozitif bir tam sayı gelmezse yeniden sorar.
- `random` modülüyle 1 ile `n` arasında (ikisi dahil) bir tam sayı tutar: `random.randint(1, n)`.
- Kullanıcıdan tahmin ister; pozitif bir tam sayı değilse yeniden sorar.
- Tahmin küçükse `Too small!`, büyükse `Too large!` yazar ve yeniden sorar; eşitse `Just right!` yazıp biter.

(CS50'de dosyanın adı `game.py`.)

Denetim her durumda rastgele sayı üretecini aynı başlangıca (tohum) getiriyor; `randint`'i bir kez, seviyeden sonra çağırırsan senin programın da aynı sayıyı tutar.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `cat`, `-1`, `1`, `1` → çıktı `Just right!`
- Girdi `10`, `cat`, `-1`, `100`, `1`, `4` → çıktı `Too large!`, `Too small!`, `Just right!`
- Girdi `10000`, `cat`, `-1`, `100000`, `1`, `4186` → çıktı `Too large!`, `Too small!`, `Just right!`
- Girdi `0`, `100`, `cat`, `-1`, `1000`, `1`, `58` → çıktı `Too large!`, `Too small!`, `Just right!`
