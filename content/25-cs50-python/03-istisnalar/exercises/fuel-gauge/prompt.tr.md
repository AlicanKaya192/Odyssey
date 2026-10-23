Yakıt göstergeleri depoda ne kadar yakıt kaldığını çoğu zaman kesirle gösterir: `1/4` deponun %25'i dolu, `1/2` %50'si, `3/4` %75'i.

Kullanıcıdan `X/Y` biçiminde bir kesir isteyen bir program yaz (`X` negatif olmayan, `Y` pozitif bir tam sayı). Depodaki yakıtı **en yakın tam sayıya yuvarlanmış** yüzde olarak yaz (`75%`). %1 ya da daha azı kaldıysa (depo neredeyse boş) yüzde yerine `E`, %99 ya da daha fazlası kaldıysa (neredeyse dolu) `F` yaz.

`X` ya da `Y` tam sayı değilse, `X` `Y`'den büyükse ya da `Y` sıfırsa **yeniden sor**. `ValueError` ve `ZeroDivisionError` gibi istisnaları yakala. (CS50'de dosyanın adı `fuel.py`.)

İpucu: birden çok türü tek `except` yakalayabilir: `except (ValueError, ZeroDivisionError):`. `round` en yakın tam sayıya yuvarlar.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `3/4` → çıktı `75%`
- Girdi `1/4` → çıktı `25%`
- Girdi `4/4` → çıktı `F`
- Girdi `0/4` → çıktı `E`
- Girdi `4/0`, `1/2` → çıktı `50%`
- Girdi `three/four`, `1/2` → çıktı `50%`
- Girdi `1.5/3`, `1/2` → çıktı `50%`
- Girdi `-3/4`, `1/2` → çıktı `50%`
- Girdi `5/4`, `1/2` → çıktı `50%`
- Girdi `2/3` → çıktı `67%`
- Girdi `99/100` → çıktı `F`
- Girdi `1/100` → çıktı `E`
