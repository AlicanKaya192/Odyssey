Başlangıç kodu bir LSTM ve sonu sıfırla dolgulanmış bir girdi kuruyor.
`compare_final_states(lengths)` iki liste döndürsün:

- LSTM'i girdiyle **paketlemeden** çalıştırınca her dizinin son durumu
  (`h[0, i]`) o dizinin son gerçek adımının çıktısıyla (`out[i, n - 1]`)
  `torch.allclose` ile aynı mı;
- aynı soru `pack_padded_sequence(..., enforce_sorted=False)` ile paketli
  çalıştırmanın son durumu için.

**Beklenen çıktı:**

```
[[True, True, False], [True, True, True]]
[[True, False], [True, True]]
```
