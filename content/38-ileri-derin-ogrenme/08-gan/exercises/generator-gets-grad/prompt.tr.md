`generator_gets_grad(use_detach)` hazır kurulan iki küçük ağla ayırt
edicinin kaybını (sahteye hedef 0, `BCEWithLogitsLoss`) geri yaysın.
`use_detach` doğruysa sahte örneği önce `detach()` ile koparsın. Üreticinin
ağırlığına türev yazılıp yazılmadığını (`G.weight.grad is not None`)
döndürsün.

**Beklenen çıktı:**

```
False
True
```
