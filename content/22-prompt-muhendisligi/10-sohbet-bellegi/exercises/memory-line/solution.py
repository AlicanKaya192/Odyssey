def system_with_memory(base, memory):
    if not memory:
        return base
    facts = "; ".join(f"{key}={value}" for key, value in memory.items())
    return base + " Known facts: " + facts


print(system_with_memory("Be brief.", {"name": "Ada", "order": "ORD-1"}))
print(system_with_memory("Be brief.", {}))
