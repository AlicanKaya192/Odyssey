Test doğruluğu modelin **ne kadar iyi** olduğunu söyler, **doğru çalışıp
çalışmadığını** söylemez. Teslim etmeden önce birkaç kısa sınama, yazılımdaki
birim testleri gibi, sessiz hataları yakalar. Aşağıdaki kod dersteki
eğitilmiş `model`'i kullanıyor.

```python
with torch.no_grad():
    probs = torch.softmax(model(x[test][:5]), dim=1)
    longer = model(torch.randn(3, 1, 128))
    alone = model(x[test][:1])
    together = model(x[test][:5])[:1]
    twice = torch.equal(model(x[test][:5]), model(x[test][:5]))
print(torch.allclose(probs.sum(dim=1), torch.ones(5)), tuple(longer.shape))
print(torch.allclose(alone, together, atol=1e-5), twice)
noise = 0.05 * torch.randn(x[test].shape, generator=torch.Generator().manual_seed(0))
stable = (predict(model, x[test] + noise) == predict(model, x[test])).float().mean()
print(stable.item() > 0.95)
```

```text
True (3, 2)
True True
True
```

Beş sınama, beş soru:

- **Olasılıklar toplamı 1 mi?** Softmax'ı unutmak ya da yanlış boyutta
  almak (`dim=0`) burada yakalanır.
- **Başka uzunlukta çalışıyor mu?** 128 ölçümlük pencere de `(3, 2)` çıktı
  verdi: `AdaptiveMaxPool1d` sayesinde. Sabit uzunluk bekleyen bir model
  burada şekil hatası verirdi.
- **Tek başına ile grup içinde aynı mı?** Bir örneğin cevabı yanındaki
  örneklere bağlı olmamalı. `BatchNorm` eğitim kipinde unutulursa bu sınama
  düşer.
- **İki çağrı aynı mı?** `eval()` unutulursa dropout her çağrıda farklı
  sonuç verir.
- **Küçük gürültüye dayanıklı mı?** Ölçüm gürültüsü kadar bir sarsıntı
  tahminlerin çoğunu değiştirmemeli. Değiştiriyorsa model sınırda kararlar
  veriyor demektir.

Bu sınamalar birkaç satır ve her eğitimden sonra yeniden çalıştırılabilir;
Python Kütüphaneleri: İleri modülündeki pytest ile bir test dosyasına koymak
doğal bir sonraki adım.
