def eval_postfix(tokens):
    stack = []
    # Push numbers; on an operator, combine the top two.

    return stack.pop() if stack else None


print(eval_postfix(["3", "4", "+", "2", "*"]))
print(eval_postfix(["8", "2", "-"]))
print(eval_postfix(["5", "1", "2", "+", "4", "*", "+", "3", "-"]))
