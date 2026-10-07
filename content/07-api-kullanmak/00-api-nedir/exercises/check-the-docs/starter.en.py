docs = {
    "/weather": {"required": ["city"], "optional": ["units"]},
    "/forecast": {"required": ["city", "days"], "optional": []},
    "/cities": {"required": [], "optional": ["country"]},
}

# check(path, params): "404 unknown endpoint", "missing: ...", "unknown: ..." or "ok"


# Check these five requests and print the result:
# ("/weather", ["city"])
# ("/news", [])
# ("/forecast", ["city"])
# ("/weather", ["city", "color"])
# ("/cities", [])
