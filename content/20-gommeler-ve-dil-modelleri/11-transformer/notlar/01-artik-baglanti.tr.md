Bloğu artık bağlantı ve katman normu olmadan, yalnızca dikkat ve ileri
beslemeli ağı arka arkaya koyarak dizseydik ne olurdu? Dersteki ağırlıklarla
16 katman deneyelim; `Z` çıplak dizi, `R` dersteki blok:

```python
Z = R = X + Pe
for layer in range(1, 17):
    Z = np.maximum(multi_head(Z, mask) @ W1, 0) @ W2
    R = block(R, mask)
    if layer in [1, 2, 4, 8, 16]:
        sizes = [np.linalg.norm(M) for M in [Z, R, layer_norm(R)]]
        print(layer, " ".join(f"{s:.3f}" for s in sizes))
```

```text
1 5.191 16.942 8.944
2 2.703 25.603 8.944
4 0.835 46.354 8.944
8 0.037 89.631 8.944
16 0.000 171.878 8.944
```

Sütunlar: katman, çıplak dizinin büyüklüğü, bloğun büyüklüğü ve bloğun
normlanmış hâlinin büyüklüğü.

- Artık bağlantı olmadan sinyal her katmanda küçülüyor ve 16 katmanda
  sıfıra iniyor: en üstteki katman girdiden hiçbir şey göremez. Geri
  yayılımda türev de aynı yoldan geçtiği için alt katmanlar öğrenemez.
- Artık bağlantıda her katman girdisine bir şey **ekliyor**; girdi her
  zaman yerinde kalıyor ve türev toplamanın üzerinden doğrudan alta iniyor.
  Bu, 2015'te görüntü ağlarında (ResNet) bulunan ve yüzlerce katmanlı
  ağları eğitilebilir yapan fikir.
- Toplama yüzünden bloğun büyüklüğü katmanlar boyunca artıyor. Katman normu
  her alt katmanın girdisini aynı ölçeğe getiriyor (son sütun hep aynı); bu
  yüzden normu girişe koyan düzen derin modellerde kararlı çalışıyor.
