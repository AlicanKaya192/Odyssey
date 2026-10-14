def trim_history(messages, keep, facts):
    system = [m for m in messages if m["role"] == "system"]
    rest = [m for m in messages if m["role"] != "system"]
    memory = []
    if facts:
        note = "; ".join(f"{key}: {value}" for key, value in sorted(facts.items()))
        memory = [{"role": "system", "content": "Known facts: " + note}]
    return system + memory + (rest[-keep:] if keep else [])


HISTORY = [{"role": "system", "content": "Be brief."},
           {"role": "user", "content": "Order ORD-48213?"},
           {"role": "assistant", "content": "It shipped."},
           {"role": "user", "content": "When?"},
           {"role": "assistant", "content": "On 2026-10-09."},
           {"role": "user", "content": "Thanks!"}]
for m in trim_history(HISTORY, 2, {"order": "ORD-48213"}):
    print(m["role"], "|", m["content"])
