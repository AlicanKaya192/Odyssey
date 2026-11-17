Otomatik kodlayıcı yalnızca **gördüğü türden** veriyi iyi kurar. Bu bir
zayıflık değil, bir araç: yeniden kurma hatası büyük olan örnek "alışılmışın
dışında"dır. Etiketsiz **anomali algılama** böyle yapılır. Aşağıdaki kod
dersteki eğitilmiş `ae`'yi kullanıyor; test rakamlarını rastgele gürültü
görüntüleriyle karşılaştırıyor.

```python
def errors(model, data):
    with torch.no_grad():
        return ((model(data) - data) ** 2).mean(dim=1)


noise = torch.rand(100, 64, generator=torch.Generator().manual_seed(2))
train_err = errors(ae, x_train)
limit = torch.quantile(train_err, 0.99)
print(errors(ae, noise).mean().item() > errors(ae, x_test).mean().item())
print((errors(ae, noise) > limit).float().mean().item() > 0.9)
```

```text
True
True
```

- Gürültünün ortalama hatası rakamlarınkinden büyük.
- Eşik eğitim hatalarının %99'luk dilimi (`torch.quantile`): eğitim
  rakamlarının yalnızca %1'i bunun üstünde. Gürültü görüntülerinin %90'ından
  fazlası eşiği aşıyor, yani "anomali" diye işaretleniyor.

Bu modülün bitirme projesindeki sensör arıza algılayıcısı etiketli veriyle
çalışıyor. Gerçekte arıza örneği çoğu zaman azdır ya da hiç yoktur; o zaman
yalnızca sağlam kayıtlarla bir otomatik kodlayıcı eğitip yeniden kurma
hatasına eşik koymak yaygın bir başlangıçtır. Eşik, doğrulama verisiyle ve
yanlış alarmın bedeline göre seçilir.
