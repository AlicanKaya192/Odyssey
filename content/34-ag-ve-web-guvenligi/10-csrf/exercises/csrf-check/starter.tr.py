import hmac


def check(expected, sent):
    return expected == sent

token = "tok-8f2a"
print(check(token, "tok-8f2a"))
print(check(token, "guess"))
print(check(None, None))
print(check("", ""))
