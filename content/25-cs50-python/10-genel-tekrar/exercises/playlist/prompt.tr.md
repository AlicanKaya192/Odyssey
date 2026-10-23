`Playlist` adında bir sınıf yaz:

- `Playlist(name)`: ad boşsa `ValueError`; şarkılar boş bir listeyle başlar.
- `add(*songs)`: istenen sayıda şarkı ekler. Şarkılardan biri listede zaten varsa ya da aynı çağrıda iki kez geçiyorsa `ValueError` ve **hiçbiri** eklenmez.
- `len(playlist)` şarkı sayısını verir (`__len__`).
- `songs`: şarkıların listesini veren, **ayarlayıcısı olmayan** bir özellik; `playlist.songs = [...]` `AttributeError` vermeli. Dönen liste bir kopya olsun.
- `__str__`: `Road Trip: 2 songs`.

Odyssey sınıfını gerçekten kurup metotlarını çağırarak denetliyor; dosyanın sonunda deneme kodu yazabilirsin.
