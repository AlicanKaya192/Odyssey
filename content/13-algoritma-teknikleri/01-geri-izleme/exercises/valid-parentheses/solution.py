def parentheses(n):
    result = []

    def build(text, opened, closed):
        if len(text) == 2 * n:
            result.append(text)
            return
        if opened < n:
            build(text + "(", opened + 1, closed)
        if closed < opened:
            build(text + ")", opened, closed + 1)

    build("", 0, 0)
    return result


for text in parentheses(3):
    print(text)
print(len(parentheses(10)))
