`count_params(d, layers, vocab, ffn=4)` bir modelin parametre sayısını
hesaplasın: her blokta dikkat `4d²`, ileri beslemeli ağ `2 · ffn · d²`, iki
katman normu `4d`; buna gömme tablosu `vocab · d` eklensin.

**Beklenen çıktı:**

```
3232
123371520
95059968
```
