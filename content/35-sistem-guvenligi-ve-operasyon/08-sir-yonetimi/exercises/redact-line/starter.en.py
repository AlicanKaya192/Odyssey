def redact(line):
    # turn the password, token, secret, api_key values into ***
    return line

print(redact("login user=ada password=hunter2 ok"))
print(redact("api_key=K1 Token=T2 status=200"))
print(redact("nothing to hide here"))
