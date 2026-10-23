Dersteki Seçmen Şapka'yı yaz, ama `sort` yazdırmak yerine bir dize **döndürsün**. `Hat` sınıfında dört Hogwarts binasının listesi `houses` adında bir **sınıf değişkeni** olsun; `sort(cls, name)` bir **sınıf metodu** (`@classmethod`) olsun ve `Harry is in Ravenclaw` gibi bir dize döndürsün; binayı `random.choice(cls.houses)` seçsin. Program hiç `Hat` nesnesi oluşturmadan adı sorup `print(Hat.sort(name))` yazar. Odyssey rastgele sayı üretecini her denemede aynı tohumla başlatıyor; o yüzden `random.choice`'u tam bir kez çağır.

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir):

```text
$ python cozum.py
Name: Harry
Harry is in Ravenclaw
```
