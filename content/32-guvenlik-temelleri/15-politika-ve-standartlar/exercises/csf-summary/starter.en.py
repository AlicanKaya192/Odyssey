FUNCTIONS = ["Govern", "Identify", "Protect", "Detect", "Respond", "Recover"]


def csf_summary(controls):
    counts = {}
    for name, function in controls:
        counts[function] = counts.get(function, 0) + 1
    return [[f, n] for f, n in counts.items()]

controls = [
    ["asset inventory", "Identify"],
    ["mfa for staff", "Protect"],
    ["disk encryption", "Protect"],
    ["log monitoring", "Detect"],
    ["backup restore test", "Recover"],
    ["coffee machine", "Snacks"],
]
for function, count in csf_summary(controls):
    print(function, count)
