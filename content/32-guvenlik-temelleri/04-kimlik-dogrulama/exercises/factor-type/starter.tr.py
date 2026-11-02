FACTORS = {
    "password": "know", "pin": "know", "passphrase": "know",
    "sms_code": "have", "app_code": "have",
    "security_key": "have", "smart_card": "have",
    "fingerprint": "are", "face": "are", "voice": "are",
}


def factor_type(method):
    return FACTORS[method]

for method in ["password", "App_Code", " fingerprint ", "carrier_pigeon"]:
    print(repr(method), factor_type(method))
