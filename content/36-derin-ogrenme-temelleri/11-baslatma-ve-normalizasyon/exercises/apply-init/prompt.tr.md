`init_weights(module)` `model.apply` ile her alt modüle çağrılıyor. Yalnızca
`nn.Linear` katmanlarında ağırlığı Kaiming (ReLU) ile başlat, sabiti sıfırla ve
katmanı `visited` listesine ekle. `init_report` `[başlatılan katman sayısı,
sabitlerin mutlak toplamı]` döndürür.

**Beklenen çıktı:**

```
[3, 0.0]
```
