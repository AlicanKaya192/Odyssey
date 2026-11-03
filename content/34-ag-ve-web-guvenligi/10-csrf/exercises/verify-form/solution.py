import hmac


def verify(sessions, sid, form):
    expected = sessions.get(sid)
    sent = form.get("csrf")
    if not expected or not sent:
        return "rejected"
    if hmac.compare_digest(expected, sent):
        return "ok"
    return "rejected"

sessions = {"s-ada": "tok-1", "s-bob": "tok-2"}
print(verify(sessions, "s-ada", {"csrf": "tok-1", "amount": "50"}))
print(verify(sessions, "s-ada", {"csrf": "tok-2", "amount": "50"}))
print(verify(sessions, "s-ada", {"amount": "50"}))
print(verify(sessions, "s-eve", {"csrf": "tok-1"}))
