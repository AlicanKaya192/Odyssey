Write a class named `Playlist`:

- `Playlist(name)`: `ValueError` if the name is empty; the songs start as an empty list.
- `add(*songs)`: adds any number of songs. If one of the songs is already in the list, or appears twice in the same call, `ValueError` and **none** are added.
- `len(playlist)` gives the number of songs (`__len__`).
- `songs`: a property giving the list of songs, **with no setter**; `playlist.songs = [...]` should give an `AttributeError`. The returned list should be a copy.
- `__str__`: `Road Trip: 2 songs`.

Odyssey checks your class by really creating it and calling its methods; you may write test code at the end of the file.
