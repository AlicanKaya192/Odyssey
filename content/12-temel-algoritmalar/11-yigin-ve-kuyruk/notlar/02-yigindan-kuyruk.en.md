Two classic design questions; both come up often in interviews and show the
power of a stack.

## A queue from two stacks

If all you have are stacks, can you build a queue? Yes: two stacks, one for
**input**, one for **output**. Adding goes to the input stack. When taking, if
the output stack is empty, move everything from the input stack to the output
one by one: the order flips and the oldest element comes to the top.

```python
class TwoStackQueue:
    def __init__(self):
        self.inbox = []
        self.outbox = []

    def push(self, x):
        self.inbox.append(x)

    def pop(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox.pop()

q = TwoStackQueue()
for x in [1, 2, 3]:
    q.push(x)
print(q.pop(), q.pop())        # 1 2
q.push(4)
print(q.pop(), q.pop())        # 3 4
```

A transfer looks like `O(n)`, but every element is transferred **at most
once** in its life: on average each operation is `O(1)` (amortised).

## A stack that knows its minimum

While pushing and popping, can you tell the **smallest** element at any moment
in `O(1)`? Next to each element, also store "the smallest in the stack when
this element was pushed":

```python
class MinStack:
    def __init__(self):
        self.items = []                    # (value, the smallest at that moment)

    def push(self, x):
        smallest = x if not self.items else min(x, self.items[-1][1])
        self.items.append((x, smallest))

    def pop(self):
        return self.items.pop()[0]

    def minimum(self):
        return self.items[-1][1]

s = MinStack()
for x in [5, 3, 7, 2]:
    s.push(x)
print(s.minimum())   # 2
s.pop()
print(s.minimum())   # 3
```

When the top element leaves, the minimum recorded by the one below is already
there; no need to scan the whole stack again.
