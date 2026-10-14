def window(history, keep):
    return history


HISTORY = [{"role": "system", "content": "S"}] + [
    {"role": "user" if i % 2 == 0 else "assistant", "content": f"m{i}"}
    for i in range(6)]
print([m["content"] for m in window(HISTORY, 3)])
print([m["content"] for m in window(HISTORY, 10)])
