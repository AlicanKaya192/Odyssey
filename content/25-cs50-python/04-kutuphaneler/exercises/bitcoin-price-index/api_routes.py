"""Odyssey'nin alıştırma sunucusu: CoinCap v3 biçiminde sabit Bitcoin fiyatı."""


def handle(request):
    if request.method == "GET" and request.path == "/v3/assets/bitcoin":
        return 200, {
            "data": {
                "id": "bitcoin",
                "rank": "1",
                "symbol": "BTC",
                "name": "Bitcoin",
                "priceUsd": "97534.2891736481",
            },
            "timestamp": 1761206400000,
        }
    return 404, {"error": "not found"}
