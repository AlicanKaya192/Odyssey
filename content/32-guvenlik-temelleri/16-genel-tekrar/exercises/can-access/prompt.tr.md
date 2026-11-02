Yetkilendirme ve Erişim Denetimi Modelleri bölümlerini birleştir.

`can_access(user, action, doc, user_roles, role_perms)`:

1. Kullanıcının rollerinden biri eylemi içeriyorsa `True`.
2. Değilse, kullanıcı belgenin sahibiyse (`doc["owner"]`) ve eylem
   `"read"` ya da `"edit"` ise `True`.
3. Geri kalan her şey `False`: bilinmeyen kullanıcı ve bilinmeyen rol
   dahil.

**Beklenen çıktı:**

```
ada edit True
bora edit False
ceren edit True
ceren delete False
zeynep read False
```
