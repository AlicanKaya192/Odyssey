Yanına `users.json` dosyası konuldu: kullanıcıların listesi. Bazılarında
`email`, bazılarında `age` alanı **yok**.

**Yapman gerekenler:**

1. Dosyayı `users` adında bir listeye oku.
2. Her kullanıcı için adını ve e-postasını yazdır; e-postası yoksa yerine
   `-` yaz.
3. E-postası olmayan kullanıcı sayısını `no_email` değişkeninde say.
4. Yaşı **olan** kullanıcıların yaşlarının ortalamasını **tam bölme** ile
   `average_age` değişkeninde hesapla.
5. Sırayla `no_email` ve `average_age` yazdır.

**Beklenen çıktı:**

```text
Ada ada@example.com
Alan -
Grace grace@example.com
Linus linus@example.com
Margaret -
2
35
```

Köşeli parantezle olmayan alanı istersen `KeyError` alırsın. `get`'in
ikinci argümanı alan yoksa dönen değer; verilmezse `None` döner.
