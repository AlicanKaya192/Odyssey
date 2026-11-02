Bir çalışan ayrılıyor. `accounts` sistem → kullanıcılar, `secrets` ortak
sır → onu bilen kullanıcılar.

`leaver_checklist(user, accounts, secrets)` yapılacak işleri bir liste
olarak döndürsün: önce hesabı olan her sistem için `"disable <sistem>"`,
sonra bildiği her sır için `"rotate <sir>"`. İki grup da kendi içinde
abece sırasında. Hiçbir şey yoksa boş liste.

**Beklenen çıktı:**

```
disable mail
disable wiki
rotate deploy-key
rotate shared-printer
[]
```
