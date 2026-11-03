import hmac

ALLOWED_ORIGINS = {"https://notes.example"}


def gate(req, sessions, notes):
    session = sessions.get(req.get("cookie", ""))
    if session is None:
        return 401
    if req["method"] == "POST":
        if req.get("origin") not in ALLOWED_ORIGINS:
            return 403
        if not hmac.compare_digest(req.get("csrf", ""), session["csrf"]):
            return 403
    for note in notes:
        if note["id"] == req["note"] and note["owner"] == session["user"]:
            return 200
    return 404

SESSIONS = {
    "s-ada": {"user": "ada", "csrf": "t-1"},
    "s-bob": {"user": "bob", "csrf": "t-2"},
}
NOTES = [{"id": 1, "owner": "ada"}, {"id": 2, "owner": "bob"}]
good = "https://notes.example"
print(gate({"method": "GET", "cookie": "s-ada", "note": 1}, SESSIONS, NOTES))
print(gate({"method": "GET", "cookie": "s-ada", "note": 2}, SESSIONS, NOTES))
print(gate({"method": "GET", "note": 1}, SESSIONS, NOTES))
print(gate({"method": "POST", "cookie": "s-ada", "note": 1,
            "origin": good, "csrf": "t-2"}, SESSIONS, NOTES))
print(gate({"method": "POST", "cookie": "s-ada", "note": 1,
            "origin": good, "csrf": "t-1"}, SESSIONS, NOTES))
