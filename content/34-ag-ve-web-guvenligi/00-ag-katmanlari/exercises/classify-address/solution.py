import ipaddress


def classify(text):
    ip = ipaddress.ip_address(text)
    if ip.is_loopback:
        return "loopback"
    if ip.is_private:
        return "private"
    return "public"

for text in ["127.0.0.1", "10.1.2.3", "172.31.0.9",
             "172.32.0.9", "100.20.30.40"]:
    print(text, classify(text))
