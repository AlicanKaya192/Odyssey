# Dönüşümler ve Veri Artırma

Gerçek projelerde etiketli resim azdır: her resmi birinin tek tek
işaretlemesi gerekir. Az resimle eğitilen ağ eğitim resimlerini
**ezberler**: onlarda kusursuz, yeni resimlerde kötüdür. Bu bölümde
torchvision'ın **dönüşümlerini** (transforms) ve onlarla yapılan **veri
artırmayı** (data augmentation) öğreneceğiz: her turda eğitim resimlerinin
biraz değiştirilmiş kopyalarını göstermek. Ağ aynı resmi hiç iki kez aynı
görmediği için ezberleyemiyor, şeklin kendisini öğrenmek zorunda kalıyor.

## Tek bir dönüşüm

torchvision'ın `v2` dönüşümleri tensörü alıp yeni bir tensör döndüren
fonksiyonlar gibi çalışır. Yatay çevirme ve dolgulu rastgele kırpma:

```python
import torch
from torchvision.transforms import v2
from dl_data import make_shapes, SHAPES

images, labels = make_shapes(300)
img = torch.from_numpy(images[0])
flip = v2.RandomHorizontalFlip(p=1.0)
print(torch.equal(flip(img), img.flip(-1)))

crop = v2.RandomCrop(16, padding=3)
print(img.shape, crop(img).shape)
```

```text
True
torch.Size([1, 16, 16]) torch.Size([1, 16, 16])
```

- `RandomHorizontalFlip(p=1.0)` resmi her seferinde aynalıyor; varsayılan
  `p=0.5` ile yarı yarıya. Sonuç, sütunları ters çeviren `img.flip(-1)` ile
  aynı.
- `RandomCrop(16, padding=3)` resmin çevresine 3 piksellik sıfır çerçevesi
  ekleyip içinden rastgele bir yerde 16 × 16'lık bir parça kesiyor. Etkisi:
  şekil birkaç piksel rastgele kayıyor. Boy değişmiyor.

## Dönüşüm zinciri

Dönüşümler `v2.Compose` ile art arda dizilir. Bir dosyadan okunan `uint8`
resmi ağa hazır hâle getiren tipik zincir:

```python
raw = (img * 255).to(torch.uint8)
prepare = v2.Compose([
    v2.RandomHorizontalFlip(),
    v2.RandomCrop(16, padding=3),
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize([0.5], [0.5]),
])
out = prepare(raw)
print(raw.dtype, out.dtype, tuple(out.shape))
print(out.min().item() >= -1, out.max().item() <= 1)
```

```text
torch.uint8 torch.float32 (1, 16, 16)
True True
```

Sıra önemli: geometrik dönüşümler (çevirme, kırpma) önce, tür dönüşümü ve
normalleştirme en sonda. `Normalize([0.5], [0.5])` [0, 1] aralığını
[−1, 1]'e taşıyor.

## Rastgelelik ve tohum

"Rastgele" dönüşümler PyTorch'un rastgele sayı üretecini kullanır. Tohumu
sabitlersen aynı değişiklik tekrar eder; sabitlemezsen her çağrıda başka bir
sonuç çıkar.

```python
augment = v2.Compose([v2.RandomHorizontalFlip(), v2.RandomCrop(16, padding=3)])
torch.manual_seed(0)
a = augment(img)
torch.manual_seed(0)
b = augment(img)
c = augment(img)
print(torch.equal(a, b), torch.equal(a, c))
```

```text
True False
```

Aynı resmin sekiz farklı artırılmış hâli:

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="371.52pt" height="52.391489pt" viewBox="0 0 371.52 52.391489" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 52.391489 
L 371.52 52.391489 
L 371.52 0 
L 0 0 
L 0 52.391489 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g clip-path="url(#pa9d1cf8dbd)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAADUAAAA1CAYAAADh5qNwAAADDElEQVR4nO1aTU8iQRCt7owogmBwRDTERAxojDcTr/4B/6k/w4sXr0YM0QtGRSAIfgI6G3Y3ta873ZPRZLPZwnd6kym6J9THvK4aFYZhRL/RbrcJMTMzwzwMQ+Y3NzfkQxAEzFOpFPPn52fDbm1tjfn9/T3z0WjkXTuEZ3h5eWH+9PRk2GkSCE0CoYiIwy8ptP7zX3x8fBj3yuUy8yjyL319fc18YWGB+WAw+OzjTIenNAmEJoEI8vk8X/T7feMm5kQ6nXaWUxtvb2/M39/fmXe7Xe9v4vJocXGR+fb2NvPT01Pva0CkpzQJhFJKcYxtbm4aNx8fH5nf3t4mWrDVajnDKpPJeF8LDw8PzGdnZw07VCWlUol5Npt1PufPtUkgNAlEgBWu0Wh4Defm5pi/vr567fb395kfHR0x39jYMOyUmoiZX8BnwH0mODg4cO5jh5x4T2mSLmg1VCSXWHWhWCx6qx9WtVwuZ9hhqGM445lpgtXVVee+WE2/z1P/KzRJzykFZXaCarXqVBS28PUBBejJyYlxD9UGCuRarZYof1uQu1PhKU0CEeCF3VPAUjscDp0LbG1tGdf1ep35+fk58+PjY8Pu8PCQ+Xg8Zr6ysmLY4b5taOFh++77PCWi+pWhvTVBs9n89IK7u7vO8LXFMnZsl5aWvK0CPE8NIRTj2nQiC4UmgdAkvaQ3rRyqVCrMr66uErWTe72eU4XYagUnHZhHtkrHPIpg37jpiEhPaRKIYG9vz9n1tPsAcSHnC2Es1Z1Ox7CzexauTrBrEDi1ntIkEOorQzcEdkrtkJ2fn/fOfJPCJ1zTMQMLkZ7SJBCaBEJls9nIlQP2tw6YExcXF94FURHElePl5WWnurCBKn0EORX3ihHpKU0CodbX1yPf7BUPeb45Lw7CbKCgxW8l7OEail279X13d8cc22dxKSDSU5qkK4qMNZe1pwlJgGewy8tL7ywXP02IA35y0IOz2tR5SpNAqK8I2p2dHeZnZ2deO5zf2u23uPmyD4VCIdEXNCI9pUkg9L9+gL+BH3R0NWqmPElZAAAAAElFTkSuQmCC" id="image6bf5d9b6bb" transform="scale(1 -1) translate(0 -38.16)" x="7.2" y="-7.031489" width="38.16" height="38.16"/>
   </g>
  </g>
  <g id="axes_2">
   <g clip-path="url(#pbfdb0c2977)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAADUAAAA1CAYAAADh5qNwAAACwElEQVR4nO2aTU/yQBDHp5NWqCAhglINFz0UYjh44soX4JvyMbh48WrEELxABHyJiihvvqSXeWY3u30a85gnmfo7/Ytsi5nZ6X9n1/E87xMY5XKZ9M3NDdhwXZf01tYW6dfXV9KHh4fKmNvbW9Lr9dp6b/4b3t7eSM/nc0gCgkAQBOIAgJJ+HMQ///PHx4fyt2q1Svrz03yL0WikXO/s7JCezWbwUyAIBEEgCAJx9Q983zeWU53lckn6/f2d9MPDg3WMbR4Vi0Xlul6vkz4/Pycd9xoQHykEgThBECj1eDweJxo4nU6NaZXL5YyvhIinpyfSmUzG6EgigiAgnc/nSb+8vKQ3UggCcfV0y2azpBeLhXVgs9kk3el0SB8dHZF2nMiwgNF58Oe0Wi3rc5KmnPhIIaTN0HL29/et1Y9XtUKhQLrf7ytjeDrzNdPBwQHY4NV0/rueEgaCQJwwDK2O4vn5OdFNuAE9OzuzGlhukMMwTDR/+dxNdaQQBOLqrmG1Whm/WKvVlOter0f68vKSdLfbJd1ut5Uxm82GdKVSsT7z7u6OtOd5pH/XU6l1FDqNRoM0T2HuIni3NqJUKhkrob6e4ukY16ZLVaFAEAiCQNzj42Plg+vr67+2kyMeHx+NLoQvDPkuhz6PuEvXSzp/btIyLj5SCAJx9R5AXMpxhsOhsVTf398b+xVxnWDuIP4FCAJBSLOjyLNOaQRP2+3tbauLSAI3rXrFS7phIT5SCAJBEIhzenqqzCk+J66urqwDuSOwleS9vT3lWncYNpfO51TSV4z4SCEIxPF9X4mvrWzyjTAdbmj5WQm+saabXb74m0wmyvd4+yxuCqQqUggCcb7bo+DrsMFgYEw5fiwhDv3IAV+rfQcEgSCkLf1OTk5IX1xcWG/C92/56TJ90y0pu7u7iU7QpCpSCALB//0DfoIvMukO6E1iyKoAAAAASUVORK5CYII=" id="image536d93dadc" transform="scale(1 -1) translate(0 -38.16)" x="52.56" y="-7.031489" width="38.16" height="38.16"/>
   </g>
  </g>
  <g id="axes_3">
   <g clip-path="url(#p28b6cc6174)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAADQAAAA1CAYAAAAOJMhOAAACaklEQVR4nO1ay6riQBCtlDfiW3wr4kIQ3Qpu/BH/1B/wA9y5UFeCouIDxPcLHWSgrA6dIJk7DFO5Z3VCOunCqpw+Xa0BAE8QBARhQBAGBGFAEAYEYUAQhq9PB4bDYeLBYJD4arWyfcY0TeKZTIb4dDpVxoVCIeLX65X4/X63fXehUNDGIC5DCMJg/E2nEI1Gie92O+LFYtE+IOMV0m9MJhPlHuL79388Ht7IEIJXS85kitVoNIj3+33im83GVRDJZJK4z+cjvlwubZ/hSns6neRmCMGrJReJRIjv93vi8/lcuyi+cLlciMfjcVuFOhwOWmXMZrOfhAb5fF5uhhCEAUEYjD91CvV6nXin01Hunc9n7ffwfKpTdrtd4q1Wi/hoNLKdNxAIaOcRlyEEr5ZcmO2HuMxyzGYz5ZrvU3iJVCoVZdx2u9XKe9Yi24vFwnsZQhAGw43K8VJwKoPhcKg1k9wNvNBsNrVm1wmxWIz4j1P4n4Dg1TaWyTZ4XI4TiQRxv9+vPFMul98Tfb2narfbyji776ZWqynXg8FA6+x/nIJI2UabFhIvM+sGj0v1er3WdkqtzoE7il6v90loapwgDAheVbkHKzOueLxE+OptVUPekuLdUeu+h6/6TuDv4GoqLkMIwoAgDMZ3nj6USiXlejwef3RykEqltPLuxv2LyxCCV0suaNPt5xJ+u91cBcGdw/F41LafrS1oz2QIQRgMNyrHV2leclZzysGP9Z0OstLp9Ed/GahWq9qSFZchBGEw3JQcTzdvVeVyOWUcX0B5g54fhFmP/J3M6ZwdrtkpsLgMIQgD/usAvhu/APL7xzFrF/zZAAAAAElFTkSuQmCC" id="image5bf11f8270" transform="scale(1 -1) translate(0 -38.16)" x="98.64" y="-7.031489" width="37.44" height="38.16"/>
   </g>
  </g>
  <g id="axes_4">
   <g clip-path="url(#pc429367808)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAADUAAAA1CAYAAADh5qNwAAACg0lEQVR4nOVayYoqMRS9dVWcFcQRXaiIfoAb9/6yv+FCUHBAkUJUHDbOE1bTm3gTKnb1e93vwa2zOiFJJXpvJScnZQCABcyAwBAIDOGlBZ/PJ1WmUinB5/O54KFQSPDb7Sb1eTwetgPlcjmpvNlsBL/f74Ink0ltO1dHCoEhEBjCoEt6NBqVKvf7veD5fN7+AcbnI16YzWaCI77+s+fzCf8KCAyBwD39nCKRSAju8XikuvV6bdsnGAxK5fP5bJvCsVhMalcsFgXvdDrujRQCQximaYr0u16vUmU8HrddvY7HI+hWzHQ67WjgbDYreCQSEXw8HkvtLOv7ehuBIRAYwktT7HK5aAUtTYN2uy14s9l0NFAgEJDKy+XSUb96vW47rusihcAQCAxhLBYLS3cgo+9BpVIRfLfbCU7fSXVJX61Wjibx08IXgSEQuAva4XCoFaFUOTQaDcH7/b6jgVShShXFaDT6KwXhikghMIQ3k8mIQqlUkiu9Lwet1Wo5SrlarSb4YDDQWmlUvfxEyrGPFAJDIHBf0oOKj7Ddbm2tZqouVPXd7Xa/PYlCoWBrsalbyZ5Ydq6LFAJDeOktgypoqd1FbazpdGqrDN5BdXLp9jGZTLT9nKYc+0ghMIRXXfF0KUJ3fXqGUlcrHVTVcDgcvvQkPtHr9QRXPRRXRQqBIRAYwviTWw+qLk6nk1RHLWTde/PbQGAIBLelX4rYzrrLNKffPVSrVW0K02801HSm7VZOLTdgCASGMDKZjKVzR6kKoBdyVGS+E7TvbjaokqFnMvUSzzTNr36DOyKF4ObN1+/326ZiuVyW2r07G+kQDodt75PVc5jl0EpjGSkEhsD/PYHfwAct89yNGFS58QAAAABJRU5ErkJggg==" id="image59fe02df1f" transform="scale(1 -1) translate(0 -38.16)" x="144" y="-7.031489" width="38.16" height="38.16"/>
   </g>
  </g>
  <g id="axes_5">
   <g clip-path="url(#pfee087fddc)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAADUAAAA1CAYAAADh5qNwAAACqklEQVR4nO1ay2oqQRCtKaLxjeAjGkRQUQMRXAhu/QH/1M9w48a9BiEuFN/iI/g2hnChrGmmxXu54ULNPaszdI/VWGdqTlePAQAXEAYEgUAQCASBQBAIBIFAEIiHW4PhcJj4dDol7nA4tPMGg4E+2MM1nNPpJL7ZbEzznp+fiU8mE+LH4/GutYrMFIJAGH/bUSBe/6fPz0/TWCKRIH656MP2+33ifr+f+Hq9vm8NIBAIdqh+xWKReLfbJb5arbTScbvdxLfbrTbYfr8nfj6fic/nc+09OskFg0HT9cvLi+xMIdit+hnG9/AvZDIZ4h8fH6Z5w+HwrmDj8dhSVl6vV1tBl8sl8cfHR8uX9zdisdj1fhAIBIFAsENJL5VKxJvNJvFOp6P9EZfLRXy322nnlctl4rVajXgqldI+y/z14WJxKpWKvTKFYGdDizeMqg7RaFRb0nmpDgQCpnlc6lzOYbZnisfj+rWCQCDYWX4Gq0jZbFbrKLjxvQVuQBuNhmmMuw1ukHO53F1SF5kpBIFAsFuLjIO/2VXXcDgcwAr5fN503W63ibdaLeL1et00r1qtEj+dTsSfnp60MXkLT2SmEOxQ0v2alhRvb/V6vT8KVigULCWsmmXesQ2FQsR5eVc3iVyOIjOFYIfqt9a0pLjk0um0aez9/f2uzutisbB0IdytqIcCXHJhZmjV6sfjiswUgkAg2OGZcrE+wOvrq2W/Qu373XqOdM8lL9Wz2cw0T+1ZWLW3uYOwRaYQBML4yc94fD6f6ZrL1uPxaM9874FDOXfm58EiM4VgB/lF2V6fy4LLhX8SoM57e3v77U8YVEQiEUt3waEa2v/yE1f9ksmkpdFVt/O6c15+EKaCG1q+h1MP17jZRdYlHo1Gpnt4+0xkoUAQCPzXC/gJfAECwAIaq0Uv2QAAAABJRU5ErkJggg==" id="imageec0daaab54" transform="scale(1 -1) translate(0 -38.16)" x="189.36" y="-7.031489" width="38.16" height="38.16"/>
   </g>
  </g>
  <g id="axes_6">
   <g clip-path="url(#p989574d582)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAADQAAAA1CAYAAAAOJMhOAAACpUlEQVR4nOWay4rqQBCGK2UixkRFUVFUUBDdCm58Ed/UF/AB3Cl4QXEhKl5AvN8wgxzoqYTunJnhwIGab/U33ek0VqW6uloNABxgBAIzEJiBwAwEZiAwA4EZCMxAYAYCM3TLskTDNE2hN5uN8iHDMIROpVJCz+dz17hwOCz0/X4X+vl8KufOZrPSNTweD9e4ZDIpHcfOQgjM0H6SnEYiEaEPh4PQuVxO/SLt/ao/zGYzVx/i5+/6er2+uxzeFkJghmYYhnC5er0uOvr9vtC73e5HkycSCaEDgYDQ6/Va+QyNtJfLReqyb6LRqNDFYpGvhRCYgcAMzbZt8Q0dj0fRsVwupbv8m9vtJnQsFlOG3NPpJA316XT6S4vLZDJC27bt6huPx0I7jsPXQgi/JVOo1WpCt9ttV9/1epW6DzX9m06nI3Sz2RR6Op0qFxQKhaTv8YNuN+wshMAMzbIsRxaVKIvFwtWm5w/qIuVy2TVuv99Lo6E3yq1Wq78uFEkC65fEsrMQAjMQOIftNPFtP78eDofS7JhmA28ajYY0e/eDZtEZkimMRiPXOO8WwdZCCMzQaUmKhuN4PC50MBh0PVQqlT4n0HWhW62Wa5zKzarVqqs9GAykifCVZAoqF2NvIQRmaIjoyHZf6mbe8xCNbNvtVlop9WYONKPodrvfXmg+n3e1aSmMRld2FkJgBgIzdPrd0BBOfZ7u3t7wTmts3toZPcjRXd8POkeJbA+TyUT5DC1Hs7MQAjN02qCXSlQXCgXlBNQtvLs5PdR5bxxU0DmOpKzmV0fo9Xp8LYTADM00TUdW7acRz3u/+VVo5nA+n5VVUD/Xgt9uIQTOR3CNbGrU5bzJKYVe6/tdZKmu4b1UKhWpy849fxmgLkzHsbMQAjPwfy/gX/MBZP3l443sOuYAAAAASUVORK5CYII=" id="image5de7e8f54f" transform="scale(1 -1) translate(0 -38.16)" x="235.44" y="-7.031489" width="37.44" height="38.16"/>
   </g>
  </g>
  <g id="axes_7">
   <g clip-path="url(#p402f68d6b6)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAADUAAAA1CAYAAADh5qNwAAAC2UlEQVR4nOWay04qQRCGayrcFDEEEJAYEzUCARIWJG59Ad/Ux3DDxq0BY9SFC28QLipyEU4wJ+Xfk24i55JzUnyrf9I9M8SqrvmrW69arc7oJ7e3t4T0ej3Rs5lMo7W1NdGDwYBcbG1tif74+DDG2u02LUs8HhddLBZFn5+fG/OYFMKkEG+eWXLhzS+/ODg4EP3y8iL6/v7+Ww9/fHwU3e/3jbFoNCqa+etv2+12RYfDYeOeUCgkOpvNit7Y2NAfKSaFMCkkUKvVnKXx6urKelMkEhH9/v7ufPjR0ZHo09NTY2xvb49saxk/HfieOcfHx2QD17vaSDFpL+l+sNROp1P6Dul02lrSsVTP2dzctKY5pnMqlTLu2d7etr4TPw+fv5sUwrRq6edBVTo8PLQ6CjS9i0ADOqder1vdBhrkfD6/dJqrjRSTQgKLBvFDiFVpNBo57ykUCqKbzaboRqNhzDs7OxN9cnIiejKZiM5kMsY9I3jv8/Oz6GAwqD9STAphUogXi8VmrkZuZ2dH9N3d3dIPr1QqTuOLLuLt7U10Mpl07n+EoEnE9YXO5/OaFMKkkIA/5RBMuf39fdE3NzfWsu+n0+k49zXQrTw9PVlTzm9oR5By+N7xeKw/UkwKCWDLXC6XjUFs77FlXpRyrvTFqjan1WpZW3sEd4L9LmLlIsWkEKZVaxJ/BdwCxnW4vr5uzEMX8V2C4MaxjPvXnspIMSnES6fTM1dKYMrkcjmyzbu8vHQ+HB3BonKMh3PoLvyEwNBi+vk/MSojxaS9+u3u7hqDaHaxH1p0zouHYYjf0MZiMevhGhpdf5/08PBg3T7zLwGVkWJSCJNCPM/zZq7SiKcJr6+vSz8cG8vr62tjDNfRcDhc+v8oOtCArkSkmBTi/a6hLZVKxvXFxYV1nv/8FrffXGfLi0gkEs5/CVIZKSaFeH+6n/ofYFIIk0KYFMKkECaF8L/+AX+DH7hmDEPCvZ5ZAAAAAElFTkSuQmCC" id="imagea93d69bd8b" transform="scale(1 -1) translate(0 -38.16)" x="280.8" y="-7.031489" width="38.16" height="38.16"/>
   </g>
  </g>
  <g id="axes_8">
   <g clip-path="url(#pd30d7b3d18)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAADUAAAA1CAYAAADh5qNwAAACiElEQVR4nOWa2ariQBCGK2XEXUFc0QsV0Qfwxntf2dfwQlBwQZEgKi437ht6kIE+1SFx+pyZMwPV39WfmO6OVqXzd7UGADyBGQgMQWCIaT/h9XqFTiaTQs9mM6GDwaDU5nq9Cn2/310Hy2azQq/Xa6Fvt5t0XSKRcLxO60ghMASBIYZ9So9EIkLvdjuhc7mceyfGq5tfTKdToRHl3+zxeMC/AIEhCDqknwrxeFw69ng8Qq9WK9d2gUBA6NPp5Ji+L6LRqNCFQkHodrutb6QQGGJYliWl3+VyEToWiznOXIfDAdxmzFQqpTRwJpMROhwOS5+NRiOhn8+v+20EhiAwxKQp9uJ8PjsaWpoGrVZLatNoNJQG8/v9Qi8WC6U2tVrNdVytIoXAEASGGPP5XJoz6aKMPgPlclno7XYrdUKfSzqlL5dLpZv428YXgSEIOhjawWDgaECpa6jX61InvV5PaTBqVKmjGA6H0nXfcRHsI4XAEDOdTksnisXi54fmZwWt2WwqpVu1WhW63++7ltKoc/nTdNMiUggMQdBhSg+QaXyz2TiWmqm7sDuPTqfz5ZvI5/PSMS2zuZXstIsUAkNMusNgN7S03EXLWJPJRGpD3cE7aB/01TEej13bqKYc+0ghMMSks50dmiL0rW+va9DZ6h20j/1+r1SX6Ha7QlMXol2kEBiCwBDjO7se9o3s4/HoWEJ+99z8JAgMQdAt/ZKk7PxuM031fw+VSsUxhel/NOzpTK9bqpbcgCEIDDHS6fTTrTpKHQDdjLObTDdD+25ngzoZuh6zr6Esy/rdd9AjUgg6v3x9Pp9jKr4olUpKayM3QqGQdEz3lOka7KlYSmMZKQSG4P++gZ/gA0Eg3I0W9gDlAAAAAElFTkSuQmCC" id="imageaf24139dfc" transform="scale(1 -1) translate(0 -38.16)" x="326.16" y="-7.031489" width="38.16" height="38.16"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pa9d1cf8dbd">
   <rect x="7.2" y="7.2" width="37.991489" height="37.991489"/>
  </clipPath>
  <clipPath id="pbfdb0c2977">
   <rect x="52.789787" y="7.2" width="37.991489" height="37.991489"/>
  </clipPath>
  <clipPath id="p28b6cc6174">
   <rect x="98.379574" y="7.2" width="37.991489" height="37.991489"/>
  </clipPath>
  <clipPath id="pc429367808">
   <rect x="143.969362" y="7.2" width="37.991489" height="37.991489"/>
  </clipPath>
  <clipPath id="pfee087fddc">
   <rect x="189.559149" y="7.2" width="37.991489" height="37.991489"/>
  </clipPath>
  <clipPath id="p989574d582">
   <rect x="235.148936" y="7.2" width="37.991489" height="37.991489"/>
  </clipPath>
  <clipPath id="p402f68d6b6">
   <rect x="280.738723" y="7.2" width="37.991489" height="37.991489"/>
  </clipPath>
  <clipPath id="pd30d7b3d18">
   <rect x="326.328511" y="7.2" width="37.991489" height="37.991489"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Aynı üçgenin sekiz artırılmış hâli: aynalanmış ve rastgele kaydırılmış.</figcaption>
</figure>

## Artırmayı veri setine bağlamak

Artırma, `Dataset`'in `__getitem__` metodunda, resim **istendiği anda**
uygulanır. Böylece aynı resim her turda başka bir hâliyle gelir.
`Dataset`, `__len__` (kaç örnek var) ve `__getitem__` (i'inci örneği ver)
metotlarını yazdığımız bir sınıf; Derin Öğrenmenin Temelleri modülünden
tanıyorsun.

```python
from torch.utils.data import Dataset


class Shapes(Dataset):
    def __init__(self, x, y, transform=None):
        self.x = torch.from_numpy(x)
        self.y = torch.from_numpy(y)
        self.transform = transform

    def __len__(self):
        return len(self.y)

    def __getitem__(self, i):
        image = self.x[i]
        if self.transform is not None:
            image = self.transform(image)
        return image, self.y[i]


x_small, y_small = make_shapes(90, seed=1)
train_aug = Shapes(x_small, y_small, augment)
train_plain = Shapes(x_small, y_small)
print(len(train_aug))
print(torch.equal(train_plain[0][0], train_plain[0][0]))
print(torch.equal(train_aug[0][0], train_aug[0][0]))
```

```text
90
True
False
```

- Artırmasız veri setinde aynı resim hep aynı geliyor; artırmalıda iki
  istek iki farklı resim veriyor.
- Test verisine artırma **uygulanmaz**: test, ağın gerçek resimlerdeki
  başarısını ölçmeli.

## Az veriyle: artırma işe yarıyor mu?

Yalnızca 90 eğitim resmiyle aynı ağı iki kez eğitelim: artırmasız ve
artırmalı. Her ikisi de 25 tur, aynı tohum.

```python
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader

x_test, y_test = make_shapes(300, seed=2)
x_test, y_test = torch.from_numpy(x_test), torch.from_numpy(y_test)


def fit(dataset):
    torch.manual_seed(0)
    model = nn.Sequential(
        nn.Conv2d(1, 8, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(8, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Flatten(), nn.Linear(256, 3),
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
    loader = DataLoader(dataset, batch_size=16, shuffle=True,
                        generator=torch.Generator().manual_seed(0))
    for epoch in range(25):
        model.train()
        for xb, yb in loader:
            optimizer.zero_grad()
            F.cross_entropy(model(xb), yb).backward()
            optimizer.step()
    model.eval()
    with torch.no_grad():
        train_acc = (model(train_plain.x).argmax(1) == train_plain.y).float().mean().item()
        test_acc = (model(x_test).argmax(1) == y_test).float().mean().item()
    return round(train_acc, 2), round(test_acc, 2)


print("plain", fit(train_plain))
print("augmented", fit(train_aug))
```

```text
plain (0.99, 0.82)
augmented (0.97, 0.97)
```

- Artırmasız ağ eğitim resimlerinin neredeyse hepsini doğru biliyor ama
  test resimlerinde belirgin biçimde geride: **ezberlemiş**.
- Artırmalı ağ eğitimde biraz daha az kusursuz, testte ise çok daha iyi.
  Eğitim ile test arasındaki açık kapandı.
- Ölçerken eğitim doğruluğunu artırmasız resimlerle (`train_plain`)
  hesapladık: artırma yalnızca eğitim adımlarında kullanılıyor.

Artırma her zaman bu kadar fark yaratmaz; ama veri azken çoğu zaman
yapılabilecek en ucuz iyileştirmedir. Hangi artırmaların **etiketi
bozmadığını** düşünmek gerekir; notlarda bunun örnekleri var.

## Özet

- `v2` dönüşümleri tensör alıp tensör verir; `v2.Compose` ile zincirlenir.
- Rastgele dönüşümler `torch.manual_seed` ile tekrarlanabilir olur.
- Artırma `Dataset.__getitem__` içinde, yalnızca eğitim verisine uygulanır.
- Az veride artırma ezberlemeyi azaltıp test başarısını artırabilir.
