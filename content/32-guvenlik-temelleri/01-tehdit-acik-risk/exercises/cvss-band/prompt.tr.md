`cvss_band(score)` bir CVSS puanını şiddet adına çevirmeli:

- `0.0` → `"None"`, `0.1`–`3.9` → `"Low"`, `4.0`–`6.9` → `"Medium"`,
- `7.0`–`8.9` → `"High"`, `9.0`–`10.0` → `"Critical"`.

Başlangıç kodu neredeyse doğru ama sınırlarda yanılıyor. Çıktıdaki `4.0`,
`7.0` ve `9.0` satırlarına bak ve düzelt.

**Beklenen çıktı:**

```
0.0 None
2.5 Low
4.0 Medium
6.9 Medium
7.0 High
9.0 Critical
10.0 Critical
```
