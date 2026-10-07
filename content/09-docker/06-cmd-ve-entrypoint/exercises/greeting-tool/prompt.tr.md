İmajı bir komut satırı aracına çevir: `docker run --rm greet Ada` yazınca
Ada'yı selamlasın, argüman verilmezse dünyayı.

**Yapman gerekenler:**

1. `ENTRYPOINT` ile her zaman `python greet.py` çalışsın.
2. `CMD` ile varsayılan argüman `World` olsun.

İkisi de köşeli parantezli biçimde. Odyssey konteyneri iki kez çalıştıracak:
argümansız ve `Ada Lovelace` ile.

**Beklenen çıktılar:**

```
Hello, World!
Hello, Ada Lovelace!
```
