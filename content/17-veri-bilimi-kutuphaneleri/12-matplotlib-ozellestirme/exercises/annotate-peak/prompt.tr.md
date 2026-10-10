`annotate_peak(values)` değerleri çizgi grafiğe çizsin (x = `0, 1, 2, ...`) ve
**en büyük** değeri `"peak"` yazılı, oklu bir notla işaretlesin
(`ax.annotate("peak", xy=(x, y), xytext=(x + 1, y), arrowprops=dict(arrowstyle="->"))`).
`peak.png` olarak kaydedip şekli kapatsın.
`[not_metni, [x, y]]` döndürsün: notun `xy` noktası (`int`). Başlangıç kodu
son noktayı işaretliyor.

**Beklenen çıktı:**

```
['peak', [3, 310]]
```
