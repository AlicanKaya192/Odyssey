Üç üründe `tedarikci_kod` boş. Bu ürünlerde `YOK` yazsın, diğerlerinde
kendi kodu görünsün.

Sütunlar: `ad` ve `tedarikci`. Ada göre sırala. **Bütün ürünler sonuca
girecek** — bu bir süzme değil.

```
ad           tedarikci
-----------  ---------
Antivirus    T2
Fare         T1
Kablo        T1
Klavye       T1
Kulaklik     YOK
...
```

Aradığın şey bir koşul değil, bir **değer değiştirici**: boş hücrenin
yerine ne yazılacağını söyleyen bir işlev.

Adı yanıltıcı olabilir — `IS NULL` soru sorar, aradığın işlev cevap yazar.
