Bu haftanın programlarında en sık karşılaşılan hatalar ve mesajları
(Python 3.14'te ölçüldü). Hata mesajının **son satırı** önce okunur: türü ve
sebebi orada yazar.

## Kapanmamış parantez ya da tırnak

```python
print("hello, world"
```

```text
SyntaxError: '(' was never closed
```

Python dosyayı çalıştırmadan önce baştan sona okur; sözdizimi hatası varsa
hiçbir satır çalışmaz. Parantezleri ve tırnakları çift çift say.

## Tırnak içinde tırnak

```python
print("hello,"friend"")
```

```text
SyntaxError: invalid syntax. Is this intended to be part of the string?
```

Dışarıda tek tırnak kullan (`'hello, "friend"'`) ya da içteki tırnağı kaçır
(`"hello, \"friend\""`).

## Metinle sayıyı toplamak

```python
x = input("What's x? ")
print(x + 1)
```

```text
TypeError: can only concatenate str (not "int") to str
```

`input` metin döndürür. Hesap yapacaksan önce çevir: `int(input(...))`.
Hata vermeyen ama yanlış olan kardeşi: iki metni toplamak (`"1" + "2"` →
`"12"`).

## Tam sayı beklerken ondalıklı yazmak

```python
int("1.5")
```

```text
ValueError: invalid literal for int() with base 10: '1.5'
```

`int` yalnızca tam sayı metnini çevirir; ondalıklı sayı için `float`.

## Tanımlanmamış ad

```python
hello()
```

```text
NameError: name 'hello' is not defined. Did you mean: 'help'?
```

Fonksiyon ya hiç tanımlanmadı, ya adı farklı yazıldı (büyük/küçük harf de
fark eder), ya da tanımından **önce** çağrıldı.

## Gövdesi girintisiz fonksiyon

```python
def f():
print(1)
```

```text
IndentationError: expected an indented block after function definition on line 1
```

`def` satırından sonraki gövde içeri itilir (genellikle 4 boşluk).

## Hata vermeyen yanlışlar

Bunlar mesaj üretmez; program çalışır ama istediğini yapmaz.

| Yazdığın | Ne oluyor | Doğrusu |
|---|---|---|
| `print("hello, name")` | ekrana `name` kelimesi yazılır | `print(f"hello, {name}")` |
| `name.strip()` (tek başına) | `name` değişmez | `name = name.strip()` |
| `print("hello,", end="")` + `print(name)` | `hello,David` bitişik | `print("hello, ", end="")` |
| `def main(): ...` ve çağrı yok | program hiçbir şey yapmaz | dosyanın sonuna `main()` |
| fonksiyonda `print(n * n)` | değer geri dönmez (`None`) | `return n * n` |
