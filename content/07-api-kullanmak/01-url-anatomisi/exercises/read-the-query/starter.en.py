from urllib.parse import parse_qs

query = "city=Ankara&units=imperial&tag=sea&tag=museum&tag=castle"

# params = parse_qs(...)
# city, units: plain text; tags: a list


# Print: the city, the units, then "3 tags: sea, museum, castle"
