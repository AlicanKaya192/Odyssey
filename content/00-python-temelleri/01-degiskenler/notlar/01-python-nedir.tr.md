Python, 1991 yılında Guido van Rossum tarafından geliştirilen, okunabilirliği ön planda tutan yüksek seviyeli bir programlama dilidir.

## Neden Python?

Veri bilimi ve makine öğrenmesi alanında Python'un baskın olmasının birkaç sebebi var:

**Sözdizimi İngilizceye yakın.** Diğer dillerde onlarca satır tutan bir iş, Python'da birkaç satırda biter. Bu, öğrenme eğrisini ciddi şekilde düşürüyor.

**Kütüphaneleri olgun.** NumPy sayısal hesaplama, pandas veri işleme, scikit-learn makine öğrenmesi, matplotlib görselleştirme için yıllardır geliştirilen ve endüstride kullanılan araçlar.

**Topluluğu geniş.** Karşılaştığın hemen her sorunun cevabı bir yerlerde bulunuyor. Bu, tıkandığında yalnız kalmaman demek.

## Yorumlanan bir dil

Python **yorumlanan** bir dildir: yazdığın kod satır satır çalıştırılır, önceden derlenmesi gerekmez. Bu, hızlı deneme yapmayı kolaylaştırır — bir satır yazıp hemen sonucunu görebilirsin.

Karşılığında C veya Rust gibi derlenen dillere göre daha yavaştır. Ama veri biliminde ağır hesaplamayı zaten NumPy gibi kütüphaneler yapıyor ve onların çekirdeği C ile yazılmış. Yani pratikte bu yavaşlık çoğu zaman hissedilmiyor.

## Sürümler

Bugün kullanılan sürüm Python 3'tür. İnternette Python 2 ile yazılmış eski örneklere rastlayabilirsin; en belirgin farkı `print` kullanımıdır:

```python
print "merhaba"      # Python 2 — artık çalışmaz
print("merhaba")     # Python 3 — doğru kullanım
```

Bir örnek çalışmıyorsa, önce Python 2 ile yazılmış olup olmadığına bak.
