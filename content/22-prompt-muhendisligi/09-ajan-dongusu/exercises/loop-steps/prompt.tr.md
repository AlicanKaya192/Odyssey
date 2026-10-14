`loop_steps(actions, max_steps)` bir ajanın turlarını taklit etsin:
`actions` her turda modelin yaptığı (`"tool"` ya da `"answer"`). En fazla
`max_steps` tur dönülür; ilk `"answer"` turunda `[o tur, True]` döndür.
Cevap gelmeden sınır dolarsa ya da eylemler biterse
`[dönülen tur sayısı, False]`.

**Beklenen çıktı:**

```
[3, True]
[5, False]
```
