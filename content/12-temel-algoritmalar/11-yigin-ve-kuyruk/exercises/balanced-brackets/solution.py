def is_balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


for t in ["(a[b]{c})", "(a[b)]", "((", ")(", ""]:
    print(t, is_balanced(t))
