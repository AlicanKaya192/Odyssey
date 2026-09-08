Üç üründe `supplier_code` boş. Bu ürünlerde `NONE` yazsın, diğerlerinde
kendi kodu görünsün.

Sütunlar: `name` ve `supplier`. Ada göre sırala. **Bütün ürünler sonuca
girecek** — bu bir süzme değil.

```
name       supplier
---------  --------
Antivirus  S2      
Cable      S1      
Desktop    S3      
Headset    NONE    
Keyboard   S1      
...
```

Aradığın şey bir koşul değil, bir **değer değiştirici**: boş hücrenin
yerine ne yazılacağını söyleyen bir işlev.

Adı yanıltıcı olabilir — `IS NULL` soru sorar, aradığın işlev cevap yazar.
