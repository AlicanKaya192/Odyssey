Bir makine şişe kolayı 50 sente satıyor ve yalnızca 25, 10 ve 5 sentlik bozuk para kabul ediyor.

Kullanıcıdan paraları **birer birer** isteyen bir program yaz. Her paradan önce kalan tutarı `Amount Due: 50` biçiminde yaz. En az 50 sent atıldığında kullanıcıya ne kadar para üstü verileceğini `Change Owed: 10` biçiminde yaz ve dur. Kullanıcının yalnızca tam sayı gireceğini varsay; kabul edilmeyen bir değer (`30` gibi) yok sayılır ve tutar değişmez. (CS50'de dosyanın adı `coke.py`.)

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `25`, `25` → çıktı `Amount Due: 50`, `Amount Due: 25`, `Change Owed: 0`
- Girdi `25`, `10`, `25` → çıktı `Amount Due: 50`, `Amount Due: 25`, `Amount Due: 15`, `Change Owed: 10`
- Girdi `10`, `5`, `30`, `25`, `10` → çıktı:

```text
Amount Due: 50
Amount Due: 40
Amount Due: 35
Amount Due: 35
Amount Due: 10
Change Owed: 0
```

- Girdi `5`, `5`, `5`, `5`, `5`, `5`, `5`, `5`, `5`, `5` → çıktı:

```text
Amount Due: 50
Amount Due: 45
Amount Due: 40
Amount Due: 35
Amount Due: 30
Amount Due: 25
Amount Due: 20
Amount Due: 15
Amount Due: 10
Amount Due: 5
Change Owed: 0
```

