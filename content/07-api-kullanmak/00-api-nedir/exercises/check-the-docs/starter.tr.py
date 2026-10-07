docs = {
    "/weather": {"required": ["city"], "optional": ["units"]},
    "/forecast": {"required": ["city", "days"], "optional": []},
    "/cities": {"required": [], "optional": ["country"]},
}

# check(path, params): "404 unknown endpoint", "missing: ...", "unknown: ..." ya da "ok"


# Bu bes istegi denetle ve sonucu yazdir:
# ("/weather", ["city"])
# ("/news", [])
# ("/forecast", ["city"])
# ("/weather", ["city", "color"])
# ("/cities", [])
