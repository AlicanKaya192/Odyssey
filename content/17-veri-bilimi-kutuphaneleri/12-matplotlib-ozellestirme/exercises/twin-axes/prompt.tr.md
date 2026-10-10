`twin_axes(temp, sales)` sıcaklığı sol eksene, satışı `ax.twinx()` ile açılan
**sağ** eksene çizsin. Sol eksenin adı `"temperature"`, sağınki `"sales"`;
çizgilerin `label`'ı da aynı adlar. İki çizgiyi **tek** açıklamada göstersin
(`ax.legend(handles=[...])`). `twin.png` olarak kaydedip şekli kapatsın.
`[alan_sayısı, sol_ad, sağ_ad, açıklamadaki_adlar]` döndürsün. Başlangıç
kodu iki seriyi aynı eksene çiziyor; sıcaklık satışın yanında düz bir çizgi
gibi kalıyor.

**Beklenen çıktı:**

```
2 temperature sales
['temperature', 'sales']
```
