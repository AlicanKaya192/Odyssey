def cache_results(queries, ttl):
    expires = {}
    results = []
    # for each query, look at the expiry time
    return results

queries = [[0, "example.com"], [100, "example.com"],
           [150, "www.example.com"], [300, "example.com"],
           [449, "www.example.com"], [450, "www.example.com"]]
for (t, name), result in zip(queries, cache_results(queries, 300)):
    print(t, name, result)
