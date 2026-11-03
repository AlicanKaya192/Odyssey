def pick_suite(client_suites, server_suites):
    return client_suites[0]

server = ["TLS_AES_256_GCM_SHA384", "TLS_AES_128_GCM_SHA256"]
print(pick_suite(["TLS_CHACHA20_POLY1305_SHA256", "TLS_AES_128_GCM_SHA256"], server))
print(pick_suite(["TLS_CHACHA20_POLY1305_SHA256"], server))
