Two shapes have something in common: both have a name and both can describe
themselves. What differs is how they work out their area. You will write the
shared part once and hand it down.

**What you need to do:**

1. Write a parent class called `Shape`:
   - Its constructor takes `name`.
   - The `describe` method **returns** this text:
     `name has area NUMBER` — for example `rectangle has area 12`

2. A `Rectangle` class that inherits from `Shape`:
   - Its constructor takes `width` and `height`.
   - It calls the parent's constructor with the name `"rectangle"`.
   - The `area` method: width times height.

3. A `Circle` class that inherits from `Shape`:
   - Its constructor takes `radius`.
   - It calls the parent's constructor with the name `"circle"`.
   - The `area` method: `math.pi * radius * radius`, **rounded to two decimal
     places.**

4. Build `Rectangle(3, 4)` and `Circle(2)` and print their `describe` results.

**Expected output:**

```
rectangle has area 12
circle has area 12.57
```

Note: the `describe` method is written only in `Shape`, yet it calls
`self.area()` — and at run time it finds **the object's own** `area` method.

> The parent's constructor is called with `super().__init__(...)`. Without it
> `self.name` is never created and `describe` raises an error.
