import ipaddress


def is_internal_ip(ip):
    return (ip.is_private or ip.is_loopback or ip.is_link_local
            or ip.is_unspecified or ip.is_reserved)


from urllib.parse import urlsplit


def safe_target(url, dns):
    host = urlsplit(url).hostname
    if not host:
        return "unknown host"
    try:
        ip = ipaddress.ip_address(dns.get(host, host))
    except ValueError:
        return "unknown host"
    return "blocked" if is_internal_ip(ip) else "ok"

DNS = {"images.example.com": "100.20.30.40",
       "intranet.example.net": "10.20.0.15"}
for url in ["https://images.example.com/a.png",
            "https://intranet.example.net/",
            "http://127.0.0.1/admin",
            "https://nowhere.example/",
            "not a url"]:
    print(safe_target(url, DNS))
