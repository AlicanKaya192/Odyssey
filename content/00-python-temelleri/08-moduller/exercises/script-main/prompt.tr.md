Bir Python dosyası iki şekilde kullanılabiliyor: doğrudan çalıştırılabiliyor
ya da başka bir dosyadan `import` edilebiliyor. `if __name__ == "__main__":`
satırı bu ikisini ayırıyor.

**Yapman gerekenler:**

1. `math` modülünü al.
2. `area` adında bir fonksiyon yaz: yarıçap alsın, dairenin alanını
   **iki basamağa yuvarlayarak** döndürsün. Alan formülü: `pi * r * r`
3. `main` adında bir fonksiyon yaz: `[1, 2, 3]` listesindeki her yarıçap
   için `area` sonucunu yazdırsın.
4. En alta koruma satırını koy ve `main()` çağır:

```python
if __name__ == "__main__":
    main()
```

**Beklenen çıktı:**

```
3.14
12.57
28.27
```

Koruma satırının anlamı: "bu dosya doğrudan çalıştırıldıysa `main()` çalışsın;
başka bir dosya bunu import ettiyse çalışmasın." Böylece dosyandaki
fonksiyonlar başkası tarafından kullanılabilir ama yan etki oluşmaz.

> `math.pi` sayıyı veriyor, `round(value, 2)` iki basamağa yuvarlıyor.
