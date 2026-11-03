import hashlib
import hmac


def transcript_hash(messages):
    h = hashlib.sha256()
    for m in messages:
        h.update(m.encode())
    return h.digest()


def verify_finished(key_hex, messages, tag_hex):
    key = bytes.fromhex(key_hex)
    th = transcript_hash(messages[-1:])
    expected = hmac.new(key, th, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, tag_hex)

key = "4242424242424242424242424242424242424242424242424242424242424242"
messages = ['client_hello', 'server_hello', 'certificate', 'certificate_verify']
tag = "3083046c807b0f2cb6932d5784d219b2c2ced5461f66c056f7a2fcd2572df718"
print(verify_finished(key, messages, tag))
messages[0] = "client_hello_weak"
print(verify_finished(key, messages, tag))
