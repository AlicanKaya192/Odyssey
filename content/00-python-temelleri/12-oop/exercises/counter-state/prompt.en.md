The real benefit of a class is that the object **remembers** something. In
this exercise you will write an object that keeps its state between calls.

**What you need to do:**

1. Write a class called `Counter`.
2. Its constructor takes no arguments; it starts the `count` attribute at `0`.
3. The `increase` method: adds one to the counter and returns the **new
   value**.
4. The `reset` method: sets the counter back to zero and returns nothing.
5. Build a `Counter` object, increase it three times and print `count`. Then
   reset it and print it again.

**Expected output:**

```
1
2
3
3
0
```

The first three lines are the **return values** of the `increase` calls, the
fourth is the `count` attribute, and the fifth is what it looks like after the
reset.

> To add one to the counter you write `self.count = self.count + 1`. You need
> `self.` every time you reach the object's data inside a method.
