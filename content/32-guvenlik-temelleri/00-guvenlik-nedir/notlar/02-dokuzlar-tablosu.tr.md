Erişilebilirlik sözleri "dokuz" sayısıyla anılır: %99,9 "üç dokuz",
%99,99 "dört dokuz". Aşağıdaki tablo Python ile hesaplandı; bir yıl 365
gün, bir ay 30 gün sayıldı.

| Söz | Yılda (dakika) | Ayda (dakika) | Haftada (dakika) |
|---|---|---|---|
| %99 | 5256,0 | 432,0 | 100,8 |
| %99,5 | 2628,0 | 216,0 | 50,4 |
| %99,9 | 525,6 | 43,2 | 10,1 |
| %99,95 | 262,8 | 21,6 | 5,0 |
| %99,99 | 52,6 | 4,3 | 1,0 |
| %99,999 | 5,3 | 0,4 | 0,1 |

## Nasıl hesaplanır?

İzin verilen kesinti, toplam sürenin "açık olmayan" payıdır:

```python
def allowed_minutes(percent, days):
    return days * 24 * 60 * (1 - percent / 100)


print(round(allowed_minutes(99.9, 30), 1))
```

```text
43.2
```

Tersine, gerçekleşen erişilebilirlik açık kalınan sürenin toplam süreye
oranıdır:

```python
total = 30 * 24 * 60
down = 12 + 30
print(round((total - down) / total * 100, 3))
```

```text
99.903
```

Ayda 42 dakika kapalı kalan bir hizmet %99,9 sözünü kıl payı tuttu: o
ay için izin 43,2 dakikaydı ve sonuç %99,903, hedefin hemen üstünde. Bir
kesinti daha olsaydı söz bozulurdu.

## Dikkat

- Yüzdeler birbirine yakın görünür; dakikaya çevirmeden karşılaştırma.
- "Planlı bakım" sözleşmede sayılıyor mu sayılmıyor mu, baştan yazılır.
- Daha fazla dokuz, daha fazla makine, daha fazla kişi ve daha fazla para
  demek. Her hizmetin beş dokuza ihtiyacı yok.
