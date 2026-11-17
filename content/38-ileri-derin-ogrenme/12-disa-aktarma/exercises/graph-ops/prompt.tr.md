`graph_ops(activation)` hazır modeli `torch.ones(2, 3)` örneğiyle dışa
aktarsın ve grafiğin `call_function` düğümlerinin hedeflerini
(`str(n.target)`), başlarındaki `aten.` öneki atılmış olarak, sırayla
listelesin.

**Beklenen çıktı:**

```
['linear.default', 'relu.default', 'linear.default']
```
