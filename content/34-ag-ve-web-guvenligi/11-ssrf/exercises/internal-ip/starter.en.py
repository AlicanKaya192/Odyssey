import ipaddress


def is_internal(text):
    ip = ipaddress.ip_address(text)
    return ip.is_private

for text in ["100.20.30.40", "127.0.0.1", "10.1.2.3",
             "169.254.169.254", "0.0.0.0", "not-an-ip"]:
    print(text, is_internal(text))
