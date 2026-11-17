`restore_matches` bir modeli `weights.pt`'ye kaydediyor ve başka tohumla ikinci
bir model kuruyor; ama ikinci modele kaydedilen sayıları hiç yüklemiyor.
`after` satırından önce dosyayı `weights_only=True` ile oku ve
`load_state_dict` ile yükle. Sonuç `[False, True]` olmalı.

**Beklenen çıktı:**

```
[False, True]
```
