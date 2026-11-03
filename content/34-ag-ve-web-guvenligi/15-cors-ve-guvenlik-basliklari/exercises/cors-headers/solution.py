ALLOWED_ORIGINS = {"https://shop.example", "https://admin.shop.example"}


def cors_headers(origin):
    headers = {"Vary": "Origin"}
    if origin in ALLOWED_ORIGINS:
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Credentials"] = "true"
    return headers

for origin in ["https://shop.example", "https://notshop.example"]:
    print(origin)
    for key in sorted(cors_headers(origin)):
        print(" ", key)
