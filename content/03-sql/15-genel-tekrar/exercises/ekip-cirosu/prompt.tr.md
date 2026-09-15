Altında en az bir çalışan olan her yönetici için ekibinin büyüklüğünü ve
ekibinin getirdiği ciroyu göster. Ekip, yöneticinin altındaki **herkes**:
doğrudan ve dolaylı, kendisi hariç. Ciro iptal edilmeyen siparişlerden;
satışı olmayan ekip `0`.

Sütunlar: `name`, `team_size`, `team_revenue`. `team_revenue` (büyükten
küçüğe), sonra `name` ile sırala.

```
name         team_size  team_revenue
-----------  ---------  ------------
Ada Kilic    5          72615.00
Bora Yilmaz  2          72615.00
Emre Sahin   1          0.00
```

Satışları yalnızca Ceren ile Deniz yapıyor; ikisi de Bora'nın ekibinde,
Bora da Ada'nınkinde — o yüzden iki ekip aynı ciroyu gösteriyor. Emre'nin
tek çalışanı Fulya'nın satışı yok. Bölümler: özyinelemeli `WITH` (12),
`LEFT JOIN` (06), gruplama (05).
