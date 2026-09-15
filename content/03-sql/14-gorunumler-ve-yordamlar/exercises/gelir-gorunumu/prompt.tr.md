İptal edilmeyen siparişlerde her müşterinin cirosunu veren bir **görünüm**
kur: `dbo.customer_revenue`. Sütunlar: `id`, `name`, `revenue`.

Denetim görünümden şöyle okuyor:

```sql
SELECT id, name, revenue FROM dbo.customer_revenue ORDER BY id;
```

```
id  name           revenue
--  -------------  --------
1   Nova Retail    4155.00
2   Bright Office  34100.00
3   Delta Systems  6710.00
4   Helix Studio   49690.00
5   Orion Labs     4510.00
```

Görünümün içinde `ORDER BY` yazılamıyor; sıra, görünümü kullanan sorgunun
işi. Hesaplanan sütuna ad vermek de şart.

Kurduğun şeyi aynı kodda denemek istersen araya `GO` yaz: `CREATE`
kendi toplu işinde olmak zorunda, `GO`'suz altına yazılan bir sorgu
sözdizimi hatası veriyor. Her çalıştırma sonunda geri alındığı için bir
sonraki çalıştırmada aynı adla yeniden kurabilirsin.
