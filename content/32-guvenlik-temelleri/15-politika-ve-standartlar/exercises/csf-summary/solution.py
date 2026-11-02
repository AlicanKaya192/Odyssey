FUNCTIONS = ["Govern", "Identify", "Protect", "Detect", "Respond", "Recover"]


def csf_summary(controls):
    counts = {f: 0 for f in FUNCTIONS}
    for name, function in controls:
        if function in counts:
            counts[function] += 1
    return [[f, counts[f]] for f in FUNCTIONS]

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
