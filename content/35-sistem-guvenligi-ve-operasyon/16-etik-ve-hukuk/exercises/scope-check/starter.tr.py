import ipaddress
from datetime import date


def scope_check(target, day, scope, excluded, window):
    address = ipaddress.ip_address(target)
    when = date.fromisoformat(day)
    start = date.fromisoformat(window[0])
    end = date.fromisoformat(window[1])
    if not start <= when <= end:
        return "outside the window"
    # hariç tutulanlar?
    if not any(address in ipaddress.ip_network(net) for net in scope):
        return "out of scope"
    return "in scope"

SCOPE = ["10.20.0.0/24"]
EXCLUDED = ["10.20.0.5"]
WINDOW = ["2026-11-10", "2026-11-14"]
for target, day in [["10.20.0.17", "2026-11-14"],
                    ["10.20.0.5", "2026-11-11"],
                    ["10.30.0.8", "2026-11-11"]]:
    print(scope_check(target, day, SCOPE, EXCLUDED, WINDOW))
