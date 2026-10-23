class Playlist:
    def __init__(self, name):
        if not name:
            raise ValueError("Missing name")
        self.name = name
        self._songs = []

    def __str__(self):
        return f"{self.name}: {len(self._songs)} songs"

    def __len__(self):
        return len(self._songs)

    @property
    def songs(self):
        return list(self._songs)

    def add(self, *songs):
        if len(set(songs)) != len(songs) or any(song in self._songs for song in songs):
            raise ValueError("Duplicate song")
        self._songs.extend(songs)
