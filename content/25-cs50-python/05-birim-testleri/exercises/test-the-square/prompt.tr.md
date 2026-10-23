`calculator.py` hazır ve salt okunur; içindeki `square(n)` bir sayının karesini döndürüyor. `test_calculator.py` dosyasındaki `test_square` fonksiyonuna `assert` satırları yaz: pozitif sayılar, negatif sayılar ve sıfır.

Odyssey testini önce doğru `calculator.py` ile çalıştırır (geçmeli), sonra `square`'in **bilerek bozulmuş** sürümleriyle (her birinde testin düşmeli). Yalnızca `square(2)`'yi denersen `n + n` yazılmış bir `square`'i kaçırırsın.
