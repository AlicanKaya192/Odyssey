Bütünlüğü izlemenin bir yolu, dosyaların parmak izlerini (özetlerini)
saklayıp sonra yeniden karşılaştırmaktır. `old` ve `new`, dosya adından
özete giden iki sözlük.

`integrity_changes(old, new)` fonksiyonunu yaz ve şu sözlüğü döndür:

- `"added"`: yalnızca `new`'de olan dosyalar,
- `"removed"`: yalnızca `old`'da olan dosyalar,
- `"changed"`: ikisinde de olup özeti farklı olan dosyalar.

Her liste `sorted` ile abece sırasında olsun.

**Beklenen çıktı:**

```
added ['run.sh']
removed ['notes.txt']
changed ['config.ini']
```
