Etiket geçmişi bir liste: her eleman `[etiket, sürüm]`, eskiden yeniye. `previous_version(history, alias)` fonksiyonunu yaz: geri dönüş için o etiketin **şu anki sürümünden önce** gösterdiği son **farklı** sürümü döndür.

- Yalnızca o etiketin satırlarına bak.
- Şu anki sürüm, o etiketin son satırındaki sürüm.
- Geriye doğru giderek şu ankinden farklı ilk sürümü bul.
- Böyle bir sürüm yoksa `None`.

**Beklenen çıktı:**

```
1
2
None
```
