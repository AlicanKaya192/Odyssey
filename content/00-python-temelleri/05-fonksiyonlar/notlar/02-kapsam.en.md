Where a variable can be seen from is called its **scope**. The moment you start
working with functions, this suddenly matters.

## Local variables

Every variable you create inside a function is **local**. It disappears when the
function ends:

```python
def calculate():
    total = 10
    print(total)

calculate()     # 10
print(total)    # NameError: name 'total' is not defined
```

This is not a restriction, it works in your favour. You can use the same name in
two different functions and they will not disturb each other.

## Global variables

Variables defined outside functions are **global**. They can be read from inside:

```python
rate = 18

def add_tax(price):
    return price + price * rate / 100

print(add_tax(100))     # 118.0
```

## Reading is allowed, writing is not

You can read a global variable inside a function. But if you **assign** to it,
Python creates a new local variable; the outer one does not change:

```python
counter = 0

def increase():
    counter = counter + 1     # UnboundLocalError

increase()
```

The error looks confusing, but the logic is this: Python sees that you assign to
`counter` inside the function and treats it as local from the start. Then, when
it tries to read the `counter` on the right-hand side, no value has been given
to it yet.

## The global keyword

If you really do want to change the outer one:

```python
counter = 0

def increase():
    global counter
    counter = counter + 1

increase()
increase()
print(counter)     # 2
```

**But do not use this.** Not unless you genuinely have to. The reason: a function
that uses `global` leaves a side effect that is invisible from the place it was
called. As a program grows, "where did this variable change" becomes a question
nobody can answer.

In almost every case the better route is to **take the value as a parameter and
return the result**:

```python
def increase(counter):
    return counter + 1

counter = 0
counter = increase(counter)
counter = increase(counter)
print(counter)     # 2
```

In this version, what the function takes and what it gives back is visible from
the call itself. Nothing is hidden.
