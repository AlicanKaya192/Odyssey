Python is a high-level programming language created by Guido van Rossum in 1991, designed with readability as its main priority.

## Why Python?

There are a few reasons Python dominates data science and machine learning:

**The syntax is close to English.** Work that takes dozens of lines in other languages fits into a few lines in Python. This lowers the learning curve considerably.

**The libraries are mature.** NumPy for numerical computing, pandas for data handling, scikit-learn for machine learning, matplotlib for visualisation — all developed over years and used in industry.

**The community is large.** The answer to almost any problem you hit is out there somewhere. That means you are not on your own when you get stuck.

## An interpreted language

Python is **interpreted**: your code runs line by line, with no separate compilation step. That makes experimenting easy — you can write one line and see the result immediately.

The trade-off is that it is slower than compiled languages like C or Rust. But in data science the heavy computation is done by libraries like NumPy, whose core is written in C, so in practice you rarely feel that slowness.

## Versions

The version in use today is Python 3. You may come across older examples written in Python 2 online; the most visible difference is how `print` is used:

```python
print "hello"      # Python 2 — no longer works
print("hello")     # Python 3 — the correct form
```

If an example does not run, first check whether it was written for Python 2.
