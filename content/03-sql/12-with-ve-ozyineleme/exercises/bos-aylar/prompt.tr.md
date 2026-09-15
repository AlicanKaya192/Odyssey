Ocak 2026'dan Haziran 2026'ya kadar **her ayın** cirosunu göster
(iptal edilenler hariç). Siparişi olmayan aylar da listede olsun, cirosu
`0`.

Sütunlar: `month` (ayın ilk günü), `revenue`. `month`'a göre sırala.

```
month       revenue
----------  --------
2026-01-01  32715.00
2026-02-01  28680.00
2026-03-01  7710.00
2026-04-01  30060.00
2026-05-01  0.00
2026-06-01  0.00
```

Mayıs ve Haziran'da sipariş yok, yani o aylar hiçbir tabloda geçmiyor —
`GROUP BY` onları kendiliğinden getiremez. Ayları önce özyinelemeli bir
`WITH` ile üret, sonra ciroyu onlara bağla.
