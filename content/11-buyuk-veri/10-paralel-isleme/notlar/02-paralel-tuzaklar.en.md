Parallel code can break in more places than sequential code. Every error on
this page was produced on this machine.

## 1. No `if __name__ == "__main__":`

On Windows every new process runs the file from the top; an unprotected pool
builds new pools. In Odyssey the code ran into the time limit. Every line that
builds a pool must be under this block.

## 2. Giving a `lambda` to a process pool

```python
ex.map(lambda x: x * 2, range(4))
# PicklingError: Can't pickle <function <lambda> ...>
```

A function sent to processes must be copyable (*picklable*); a `lambda` is not
suitable. Write a named function with `def` at the outermost level of the
file. In a thread pool a `lambda` is fine, because there is no copying.

## 3. Defining the function inside the `if __name__` block

```python
if __name__ == "__main__":
    def double(x):
        return x * 2
    ex.map(double, ...)
# BrokenProcessPool: A process in the process pool was terminated abruptly ...
```

The helper processes do not run this block; they never see the function.
Functions are defined **outside** the block.

## 4. Expecting processes to change a variable

```python
counter = 0
def add(x):
    global counter
    counter += x
```

Calling `add` for 0–9 with four processes left `counter` in the main program
at **0**: each process changed its own copy. The same code with threads gave
45 (shared memory). To get results from processes, the function must
**return** a value.

## 5. Expecting order from `as_completed`

`map` brings results in the order you gave them (`[0, 1, 2, 3, 4]`);
`as_completed` in whichever order they finish (`[4, 3, 2, 1, 0]`). If order
matters, use `map` or match results by a key.

## 6. Sending every item separately

Ten thousand small jobs sent one by one to four processes turned a 0.0009 s
job into 1.78 s. Give a `chunksize`, or do not go parallel.

## 7. Opening more workers than cores

For pure Python arithmetic, more processes than cores does not speed things
up; the processes queue for the cores. For waiting work, though, there can be
more threads than cores.

## 8. Not checking the result

The parallel and sequential solutions must give the same result. Every
parallel example on this track compared the two results.
