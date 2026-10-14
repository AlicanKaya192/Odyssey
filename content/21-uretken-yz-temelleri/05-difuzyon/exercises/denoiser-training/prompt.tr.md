`train(steps, seed)` dersteki gürültü tahmincisini eğitiyor, ama döngüde iki
satır eksik. `xt`'yi tek formülle kur:
`xt = np.sqrt(a) * x0 + np.sqrt(1 - a) * eps`; ağı çalıştırdıktan sonra
kaybın türevini ver: `backward(acts, 2 * (acts[-1] - eps) / eps.size, net)`.
Fonksiyon eğitimden sonra ayrı bir denetim grubunda tahmin hatasını
döndürüyor. Ağ parçaları salt okunur `diffusion_base.py`'de.

**Beklenen çıktı:**

```
0.386
```
