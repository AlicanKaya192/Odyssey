import ipaddress


def is_internal(text):
    try:
        ip = ipaddress.ip_address(text)
    except ValueError:
        return True
    return (ip.is_private or ip.is_loopback or ip.is_link_local
            or ip.is_unspecified or ip.is_reserved)

for text in ["100.20.30.40", "127.0.0.1", "10.1.2.3",
             "169.254.169.254", "0.0.0.0", "not-an-ip"]:
    print(text, is_internal(text))
