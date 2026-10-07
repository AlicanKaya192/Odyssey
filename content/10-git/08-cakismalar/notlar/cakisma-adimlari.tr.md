Çakışma çıktığında sırayla.

## 1. Sakin ol, bak

```text
git status
```

`Unmerged paths` altındaki her dosya çözülmeyi bekliyor. İstemde
`MERGING` yazıyor. Ne olduğunu anlamadıysan:

```text
git merge --abort
```

her şeyi birleştirmeden önceki hâline döndürür. Hiçbir şey kaybolmaz.

## 2. Her dosyayı çöz

Dosyayı aç, işaretleri bul:

```text
<<<<<<< HEAD
bizim dalımızdaki satır
=======
getirdiğimiz daldaki satır
>>>>>>> summer
```

Doğru hâli bırak, üç işaret satırını sil. Dosyada `<<<<<<<` kalmadığından
emin ol.

Bir tarafı olduğu gibi almak istersen:

| Ne istiyorsun? | Komut |
|---|---|
| Bizim dalın hâli | `git checkout --ours dosya` |
| Gelen dalın hâli | `git checkout --theirs dosya` |

## 3. İşaretle

```text
git add dosya
```

Her çakışan dosya için. `git status` artık `All conflicts fixed but you are
still merging` diyor.

## 4. Bitir

```text
git commit --no-edit
```

ya da `git merge --continue`. Gerçek terminalde `--no-edit` yazmazsan Git
mesaj için düzenleyici açar; hazır mesajı kaydedip kapatman yeter.

## Sık hatalar

| Belirti | Sebep | Çözüm |
|---|---|---|
| `Committing is not possible because you have unmerged files` | Çakışan dosyayı `git add` ile işaretlemedin. | `git add dosya` |
| Kod çalışmıyor, dosyada `<<<<<<<` var | İşaretleri silmeden `git add` yaptın. | Dosyayı düzelt, yeniden `git add`, `git commit --amend --no-edit`. |
| `You have not concluded your merge` | Bitmemiş birleştirme varken yeni bir `git merge`. | Önce bitir ya da `--abort`. |
| `There is no merge to abort` | Ortada birleştirme yok. | `git status` ile bak. |
