ALLOWED_ORIGINS = {"https://shop.example", "https://admin.shop.example"}


def cors_headers(origin):
    return {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Credentials": "true",
    }

for origin in ["https://shop.example", "https://notshop.example"]:
    print(origin)
    for key in sorted(cors_headers(origin)):
        print(" ", key)
