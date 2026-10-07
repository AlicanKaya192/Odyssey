Ekiplerin çoğu dalları ve birleştirmeyi aynı düzenle kullanır. Adı
**özellik dalı akışı** (*feature branch workflow*); GitHub'daki pull request
(10) de bunun üstüne kurulu.

## Kurallar

1. `main` her zaman çalışır. Doğrudan ona commit atılmaz.
2. Her iş için `main`'den yeni bir dal açılır: `git switch -c contact-form`.
3. İş o dalda, küçük ve anlamlı commit'lerle yapılır.
4. İş uzun sürerse `main` ara sıra dala birleştirilir; dal güncel kalır.
5. İş bitince dal `main`'e birleştirilir (ekiplerde bir pull request ile, biri
   gözden geçirdikten sonra).
6. Birleştirilen dal silinir.

## Bir günün akışı

```text
git switch main                  ana dala dön
git switch -c contact-form       yeni iş için dal
... düzenle, git add, git commit (birkaç kez) ...
git switch main                  ana dala dön
git merge contact-form --no-edit işi al
git branch -d contact-form       dalı temizle
```

## Neden bu kadar dal?

- **Yarım iş `main`'i bozmaz.** Bir şey ters giderse dalı silip baştan
  başlarsın.
- **Aynı anda birden fazla iş yürür.** Acil bir hata gelince yarım dalı
  bırakıp `main`'den yeni bir dal açarsın.
- **Gözden geçirme kolaylaşır.** Bir dal bir işi anlatır; ekip arkadaşın
  yalnızca onu inceler.

## Uzun yaşayan dallar

Bazı ekipler `main`'in yanında `develop` gibi uzun ömürlü bir dal daha
tutar (*Git Flow*). Küçük projelerde gerek yok; tek `main` ve kısa ömürlü
özellik dalları çoğu zaman yeterli. Dallar ne kadar kısa yaşarsa birleştirmek
o kadar kolay olur.
