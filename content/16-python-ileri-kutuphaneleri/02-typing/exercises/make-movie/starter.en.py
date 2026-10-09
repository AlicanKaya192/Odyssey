from typing import NotRequired, TypedDict


class Movie(TypedDict):
    title: str
    year: int
    rating: NotRequired[float]


def make_movie(title: str, year: int, rating: float | None = None) -> Movie:
    movie: Movie = {"title": title, "year": year}
    # add rating if it is not None
    return movie

print(sorted(make_movie("Up", 2009)))
print(make_movie("Coco", 2017, 8.4)["rating"])
