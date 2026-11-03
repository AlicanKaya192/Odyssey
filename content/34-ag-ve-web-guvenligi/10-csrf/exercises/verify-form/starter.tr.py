import hmac


def verify(sessions, sid, form):
    # oturumun jetonunu bul, formdakiyle karsilastir
    return "ok"

sessions = {"s-ada": "tok-1", "s-bob": "tok-2"}
print(verify(sessions, "s-ada", {"csrf": "tok-1", "amount": "50"}))
print(verify(sessions, "s-ada", {"csrf": "tok-2", "amount": "50"}))
print(verify(sessions, "s-ada", {"amount": "50"}))
print(verify(sessions, "s-eve", {"csrf": "tok-1"}))
