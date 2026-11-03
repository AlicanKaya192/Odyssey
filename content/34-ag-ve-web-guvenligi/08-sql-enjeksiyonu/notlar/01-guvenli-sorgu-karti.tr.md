## Kural

**Her** değer parametreyle gider; sorgu metnine hiçbir zaman kullanıcıdan
gelen bir şey yapıştırılmaz.

## Python kalıpları (sqlite3)

| İş | Doğru yazım |
|---|---|
| Tek değer | `conn.execute("... WHERE owner = ?", (owner,))` |
| Birden çok değer | `conn.execute("... WHERE a = ? AND b = ?", (a, b))` |
| Çok satır ekleme | `conn.executemany("INSERT ... VALUES (?, ?)", rows)` |
| `IN` listesi | `", ".join("?" * len(items))` ile yer tutucu üret, değerleri ayrı ver |
| Sütun adı | İzin listesi sözlüğüne eşle: `SORTABLE.get(sort, "name")` |
| `LIKE` araması | `\` sonra `%` ve `_` kaçılır, `... LIKE ? ESCAPE '\'` |

## Yanlış yazımlar

Hepsi aynı açıktır:

- `f"... WHERE owner = '{owner}'"`
- `"... WHERE owner = '" + owner + "'"`
- `"... WHERE owner = '%s'" % owner`
- `"... WHERE owner = '{}'".format(owner)`

## Neden ayıklama yetmez?

"Tırnakları silerim" ya da "`'` yerine `''` yazarım" yaklaşımı her
bağlamı, her veritabanının kurallarını ve her karakter kodlamasını doğru
bilmeyi ister. Parametre bu bilgiyi veritabanı sürücüsüne bırakır; değeri
koda çevirmenin hiçbir yolunu bırakmaz.

## Zararı sınırlayan katmanlar

- Uygulamanın veritabanı kullanıcısı en az yetkili (okuyan bölüm yalnızca
  okur, tablo silme yetkisi yok).
- Veritabanı hata mesajı kullanıcıya gösterilmez, kayda yazılır.
- Girdi önce beklenen türe ve biçime çevrilir (sayı, tarih, e-posta).
- Parolalar özetli saklanır; sızan bir tablo düz parola içermez.
