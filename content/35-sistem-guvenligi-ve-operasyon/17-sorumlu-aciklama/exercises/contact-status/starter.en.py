from datetime import datetime


def contact_status(fields, now):
    if not fields.get("contact"):
        return "no contact"
    if not fields.get("expires"):
        return "no expiry"
    expires = datetime.fromisoformat(fields["expires"][0])
    return "ok"

OK = {"contact": ["mailto:security@example.org"],
      "expires": ["2026-12-31T23:59:59Z"]}
OLD = {"contact": ["mailto:security@example.org"],
       "expires": ["2026-01-31T00:00:00Z"]}
NOW = "2026-11-03T12:00:00Z"
print(contact_status(OK, NOW))
print(contact_status(OLD, NOW))
print(contact_status({}, NOW))
