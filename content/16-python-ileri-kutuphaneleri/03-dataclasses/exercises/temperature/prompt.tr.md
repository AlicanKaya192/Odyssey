`Temperature` dataclass'ı: `celsius: float` ve `__init__`'te istenmeyen
`fahrenheit: float` (`field(init=False)`). `__post_init__` celsius
-273.15'in altındaysa `ValueError("below absolute zero")` versin, değilse
`fahrenheit = celsius * 9 / 5 + 32` hesaplasın.

**Beklenen çıktı:**

```
Temperature(celsius=100, fahrenheit=212.0)
ValueError: below absolute zero
```
