`git log --oneline --graph --all` dalların nasıl ayrıldığını ve
birleştiğini metin çizgileriyle gösterir. İlk bakışta karışık; dört işareti
bilmek yeter.

| İşaret | Anlamı |
|---|---|
| `*` | Bir commit. Satırın geri kalanı hash'i ve mesajı. |
| <code>&#124;</code> | Bir dalın çizgisi; yukarıdan aşağı geçmişe doğru akar. |
| `/` | Bir dal buradan ayrıldı (aşağıdaki commit'ten çatallandı). |
| `\` | Bir dal buraya katıldı (birleştirme, 07). |

## Bir örnek

```text
* 4c1a2f0 (login) Add login form
| * 9e8d7c6 (HEAD -> main) Fix typo
|/
* 2b3c4d5 Add home page
```

Aşağıdan yukarı oku (eskiden yeniye):

1. `Add home page` iki dalın ortak noktası.
2. Oradan iki çizgi çıkıyor (`|/`): biri `main`, biri `login`.
3. `main` dalında `Fix typo`, `login` dalında `Add login form` var; iki dal
   birbirinin commit'ini görmüyor.
4. Parantez içindeki adlar dalların şu an nerede olduğunu söylüyor. `HEAD ->
   main` bulunduğun dal.

## İpuçları

- `--all` olmadan yalnızca bulunduğun dalın geçmişi görünür; öbür dallar
  çizilmez.
- Uzun geçmişte `-10` gibi bir sınır koy.
- Bu komutu sık yazacaksan kısaltma tanımlayabilirsin (15'te):
  `git config --global alias.lg "log --oneline --graph --all"`, sonra
  `git lg`.
