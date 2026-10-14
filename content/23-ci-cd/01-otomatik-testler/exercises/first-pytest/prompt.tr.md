`shipping.py` (yan sekmede, salt okunur) bir kargo ücretini hesaplıyor:

- 1 kg'a kadar: `5`
- 5 kg'a kadar: `9`
- Sonrası: `9` + fazla her kg için `2`

`main.py`'ye en az **üç** test yaz:

- `shipping_cost(1)` → `5`
- `shipping_cost(5)` → `9`
- `shipping_cost(7)` → `13`

Her test `test_` ile başlayan bir fonksiyon. Odyssey testlerini doğru kodda ve bilerek bozulmuş sürümlerde çalıştıracak.
