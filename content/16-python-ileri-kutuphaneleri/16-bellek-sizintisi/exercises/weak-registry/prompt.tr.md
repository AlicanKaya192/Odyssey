`Registry` eklenen nesneleri bir kümede tutuyor; nesneler programın başka
yerinde silinse de kayıtta yaşamaya devam ediyor. Kümeyi
`weakref.WeakSet` ile değiştir: silinen nesne kayıttan kendiliğinden
düşsün. (Alttaki `del item` satırına dikkat: döngü bittikten sonra `item`
adı son nesneyi göstermeye devam eder; o da bir başvurudur.) Beklenen çıktı:

```
3
2
0
```

**Beklenen çıktı:**

```
3
2
0
```
