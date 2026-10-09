def eval_postfix(tokens):
    stack = []
    for token in tokens:
        if token in ("+", "-", "*"):
            right = stack.pop()
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            else:
                stack.append(left * right)
        else:
            stack.append(int(token))
    return stack.pop() if stack else None


print(eval_postfix(["3", "4", "+", "2", "*"]))
print(eval_postfix(["8", "2", "-"]))
print(eval_postfix(["5", "1", "2", "+", "4", "*", "+", "3", "-"]))
