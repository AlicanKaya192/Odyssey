Gringotts kasası: `Vault(galleons=0, sickles=0, knuts=0)` üç sikke sayısını aynı adlı örnek değişkenlerinde saklar; `__str__` `100 Galleons, 50 Sickles, 25 Knuts` döndürür. `__add__` yaz ki iki kasa `+` ile toplanabilsin: sonuç, sayıları ayrı ayrı toplanmış **yeni** bir `Vault`; iki kasa da değişmez.

Odyssey sınıfını gerçekten kurup metotlarını çağırarak denetliyor; dosyanın sonunda deneme kodu yazabilirsin.
