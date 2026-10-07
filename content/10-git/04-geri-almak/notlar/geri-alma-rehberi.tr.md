"Bir şeyi bozdum" anında sırayla sor. ⚠ işaretli komutlar commit'lenmemiş
işi kalıcı olarak siler.

## Değişiklik henüz commit'lenmedi

| Ne istiyorsun? | Komut |
|---|---|
| Bir dosyadaki değişikliği atmak | ⚠ `git restore dosya` |
| Bütün dosyalardaki değişiklikleri atmak | ⚠ `git restore .` |
| `git add`'i geri almak (değişiklik kalsın) | `git restore --staged dosya` |
| Yeni dosyayı hazırlık alanından çıkarmak | `git rm --cached dosya` |
| İzlenmeyen dosyaları silmek | `git clean -n` → ⚠ `git clean -f` (`-d` klasörler) |
| Her şeyi son commit'e döndürmek | ⚠ `git reset --hard` |

## Son commit'te sorun var (henüz paylaşılmadı)

| Ne istiyorsun? | Komut |
|---|---|
| Mesajı düzeltmek | `git commit --amend -m "Doğru mesaj"` |
| Unutulan dosyayı eklemek | `git add dosya` + `git commit --amend --no-edit` |
| Commit'i geri almak, değişiklik hazırlıkta kalsın | `git reset --soft HEAD~1` |
| Commit'i geri almak, değişiklik dosyada kalsın | `git reset HEAD~1` |
| Commit'i tamamen atmak | ⚠ `git reset --hard HEAD~1` |

## Commit paylaşıldı (GitHub'da, başkalarında)

| Ne istiyorsun? | Komut |
|---|---|
| Bir commit'in etkisini geri almak | `git revert <commit>` |
| Son commit'i geri almak | `git revert HEAD` |

Paylaşılmış commit'te `--amend` ve `reset` kullanma: başkalarının geçmişiyle
seninki ayrışır.

## Bir dosyanın eski hâli

| Ne istiyorsun? | Komut |
|---|---|
| Yalnızca bakmak | `git show HEAD~2:dosya` |
| Dosyayı o hâle getirmek | `git restore --source=HEAD~2 dosya` |

## `reset`'in üç kipi tek tabloda

| Kip | Dal | Hazırlık alanı | Dosyalar |
|---|---|---|---|
| `--soft` | geri gider | değişiklik orada | değişmez |
| `--mixed` (varsayılan) | geri gider | temizlenir | değişiklik orada |
| ⚠ `--hard` | geri gider | temizlenir | commit'e döner, değişiklik gider |
