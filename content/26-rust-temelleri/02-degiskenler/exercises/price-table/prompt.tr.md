Dosyanın başında `const VAT_PERCENT: u32 = 20;` tanımla. `base` değişkeni 250. KDV'yi `base * VAT_PERCENT / 100` ile hesaplat. Sütunlar sağa yaslı ve 6 karakter geniş olsun (`{:>6}`).

**Beklenen çıktı:**

```text
base     250
tax       50
total    300
```
