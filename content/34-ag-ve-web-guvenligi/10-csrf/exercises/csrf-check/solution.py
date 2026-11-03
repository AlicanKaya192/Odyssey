import hmac


def check(expected, sent):
    if not expected or not sent:
        return False
    return hmac.compare_digest(expected, sent)

token = "tok-8f2a"
print(check(token, "tok-8f2a"))
print(check(token, "guess"))
print(check(None, None))
print(check("", ""))
