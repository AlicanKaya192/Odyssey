Bir değişkenin nereden görülebildiğine **kapsam** deniyor. Fonksiyonlarla
çalışmaya başlayınca bu konu birden önem kazanıyor.

## Yerel değişkenler

Fonksiyonun içinde oluşturduğun her değişken **yerel**dir. Fonksiyon bitince yok
olur:

```python
def calculate():
    total = 10
    print(total)

calculate()     # 10
print(total)    # NameError: name 'total' is not defined
```

Bu bir kısıtlama değil, işine yarayan bir şey. İki farklı fonksiyonda aynı adı
kullanabiliyorsun ve birbirlerini bozmuyorlar.

## Global değişkenler

Fonksiyonların dışında tanımlanan değişkenler **global**dir. İçeriden
okunabilirler:

```python
rate = 18

def add_tax(price):
    return price + price * rate / 100

print(add_tax(100))     # 118.0
```

## Okumak serbest, yazmak değil

Global bir değişkeni fonksiyon içinde okuyabilirsin. Ama ona **atama yaparsan**
Python yeni bir yerel değişken oluşturur; dışarıdaki değişmez:

```python
counter = 0

def increase():
    counter = counter + 1     # UnboundLocalError

increase()
```

Bu hata kafa karıştırıcı görünüyor ama mantığı şu: Python fonksiyonun içinde
`counter`'a atama yaptığını görüyor ve onu baştan yerel sayıyor. Sonra sağ
taraftaki `counter`'ı okumaya çalışırken henüz değer verilmemiş oluyor.

## global anahtar sözcüğü

Gerçekten dışarıdakini değiştirmek istiyorsan:

```python
counter = 0

def increase():
    global counter
    counter = counter + 1

increase()
increase()
print(counter)     # 2
```

**Ama bunu kullanma.** Ciddi anlamda gerekmedikçe. Sebebi şu: `global` kullanan
bir fonksiyon, çağrıldığı yerden görünmeyen bir yan etki bırakıyor. Program
büyüdükçe "bu değişken nerede değişti" sorusunun cevabı bulunamaz hâle geliyor.

Neredeyse her durumda daha iyi olan yol, değeri **parametre olarak alıp
sonucu döndürmek**:

```python
def increase(counter):
    return counter + 1

counter = 0
counter = increase(counter)
counter = increase(counter)
print(counter)     # 2
```

Bu sürümde fonksiyonun ne aldığı ve ne verdiği çağrı satırına bakınca belli
oluyor. Gizli hiçbir şey yok.
