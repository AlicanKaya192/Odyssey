Gradyan gerektirmeyen, en sezgisel açıklama yöntemi **örtme duyarlılığı**
(occlusion sensitivity): resmin bir bölgesini sıfırla kapat, doğru sınıfın
olasılığı ne kadar düşüyor bak. Bölgeyi resmin üstünde gezdir; olasılığı en
çok düşüren bölge, modelin en çok güvendiği yer. Bu not dersteki eğitilmiş
modeli kullanıyor.

```python
def occlusion_map(image, target, patch=6):
    steps = image.shape[-1] // patch
    drops = torch.zeros(steps, steps)
    with torch.no_grad():
        base = F.softmax(model(image[None]), dim=1)[0, target]
        for row in range(steps):
            for col in range(steps):
                r0, c0 = row * patch, col * patch
                covered = image.clone()
                covered[:, r0:r0 + patch, c0:c0 + patch] = 0
                prob = F.softmax(model(covered[None]), dim=1)[0, target]
                drops[row, col] = base - prob
    return drops


drops = occlusion_map(x_test[2], y_test[2].item())
row, col = divmod(drops.argmax().item(), 4)
print(SHAPES[y_test[2]], drops.shape, (row, col), (row * 6, col * 6))
print((drops > 0.5).sum().item())
```

```text
square torch.Size([4, 4]) (1, 2) (6, 12)
1
```

- 24 × 24'lük resim 6 × 6'lık 16 parçaya bölündü; her parça bir kez
  kapatıldı.
- Resim bir kare (dersteki üçüncü satır: kutusu x 9–17, y 2–11). En büyük
  düşüş (1, 2) parçasında: resmin 6–11. satırları ve 12–17. sütunları, karenin
  sağ alt köşesi. Olasılığı yarıdan fazla düşüren tek parça bu.
- Bedeli: parça başına bir ileri geçiş (burada 16). Büyük resimde ve küçük
  parçada binlerce geçiş eder; Grad-CAM tek ileri ve tek geri geçişle yetinir.
- Her resimde işe yaramayabilir: model çok eminse ve şekil birkaç parçaya
  yayılıyorsa tek parçayı kapatmak olasılığı hiç oynatmaz (dersteki ikinci
  resimde, dairede, hiçbir parça olasılığı 0,01 bile düşürmüyor).
- Kapatırken kullanılan değer (0, gri, bulanık) sonucu değiştirebilir: siyah
  bir parça modele "yeni bir şekil" gibi de görünebilir.
