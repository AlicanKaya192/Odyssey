`money_ticks(values)` değerleri çubuk grafiğe çizsin ve y ekseni yazılarını
binlik ayraçlı, ondalıksız yazsın
(`StrMethodFormatter("{x:,.0f}")`). Şekli çizdirip (`fig.canvas.draw()`) y
ekseninin **ilk üç** işaret yazısını liste olarak döndürsün, sonra şekli
kapatsın.

**Beklenen çıktı:**

```
['0', '200,000', '400,000']
```
