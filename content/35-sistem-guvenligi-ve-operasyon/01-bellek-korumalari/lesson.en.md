# Memory Protections: ASLR, DEP, Canaries

In the Memory Safety and Buffer Overflows section we saw that an overflow
silently damages nearby data. The best fix is never writing these bugs in
the first place: choosing a memory-safe language, measuring before writing.
But millions of lines of C and C++ run in the world and they cannot all be
fixed in a day.

That is why operating systems and compilers add protection layers that
shrink the damage **even when** the bug is there. This section covers the
three most common ones: the **stack canary**, **DEP** (data execution
prevention) and **ASLR** (address space layout randomization). We will
again see them all with toy models built in Python.

## The stack and the return information

When a function is called, a region of memory is opened for its local
variables; this is called a **stack frame**. In the frame, right next to
the local buffers, sits the information that says **where the program
returns** when the function ends. If an overflow reaches that information,
the program's flow is damaged. Most protections defend exactly this point.

## The stack canary

Miners had an old habit: they took a canary into the mine, and when
dangerous gas built up the canary was affected first and the miners were
warned. A **stack canary** uses the same idea: the compiler places a value,
chosen **at random** every time the program starts, between the buffer and
the return information. Before the function returns it looks at this value.
If the value has changed, an overflow has happened in between; instead of
returning, the program is stopped right away.

```python
import random

rng = random.Random(42)
CANARY = rng.randrange(1, 256)


def make_frame(size):
    return [0] * size + [CANARY, 0]


def write(frame, data):
    for i, value in enumerate(data):
        if i < len(frame):
            frame[i] = value


def check(frame, size):
    if frame[size] != CANARY:
        return "stack smashing detected"
    return "ok"


small = make_frame(4)
write(small, [1, 2, 3])
print(check(small, 4))
big = make_frame(4)
write(big, [1, 2, 3, 4, 5, 6])
print(check(big, 4))
```

```text
ok
stack smashing detected
```

The frame is made of a 4-number buffer, the canary and the return
information. Three numbers fitted in the buffer and the canary stayed in
place. Six numbers went past the buffer and over the canary; the check
caught it. In real programs the program ends in this case with a message
like `stack smashing detected`: better than carrying on with damaged return
information.

The canary must be **random** and **secret**: a fixed value everyone knows
would not be enough to notice the overflow. Because the canary is only
checked **before returning**, it cannot catch another variable that the
overflow damaged inside the same function (like the role in the previous
section).

## DEP: what is writable is not executable

Every region of memory has permissions: readable (`r`), writable (`w`),
executable (`x`). **DEP** (Data Execution Prevention, called the **NX** bit
in hardware) enforces this rule: regions reserved for data (the stack, the
heap) are **not executable**. Its general name is **W^X** (write xor
execute): a region is either writable or executable, never both.

```python
regions = {"code": "r-x", "data": "rw-", "stack": "rw-", "jit": "rwx"}
for name, perms in regions.items():
    writable = "w" in perms
    executable = "x" in perms
    flag = "  <- W^X violation" if writable and executable else ""
    print(f"{name:<6} {perms}{flag}")
```

```text
code   r-x
data   rw-
stack  rw-
jit    rwx  <- W^X violation
```

The code region is executable but not writable; data and stack are
writable but not executable. So data written into memory by an overflow
cannot run as code. The `jit` region in the list (the kind of region used
by compilers that generate code while running) allows both; the check
flagged it. Such regions are opened only when truly needed, and carefully.

## ASLR: changing the addresses every time

Someone trying to exploit an overflow wants to know **where** the program
and its libraries sit in memory. These addresses used to be the same on
every run. **ASLR** (Address Space Layout Randomization) chooses the
starting address of the program, the libraries, the stack and the heap
**at random** on every run:

```python
import random

for run in range(3):
    rng = random.Random(run)
    base = 0x400000 + rng.randrange(256) * 0x10000
    print(f"run {run}: base {base:#x}")
```

```text
run 0: base 0x1050000
run 1: base 0x840000
run 2: base 0x5c0000
```

The same program started at three different addresses in three runs. Even
if an address is learned once, it is useless on the next run.

ASLR's strength depends on how many different addresses are possible, that
is, **how many bits of randomness** (entropy) are used:

```python
for bits in [8, 16, 28]:
    print(f"{bits:>2} bits: 1 in {2 ** bits:,}")
```

```text
 8 bits: 1 in 256
16 bits: 1 in 65,536
28 bits: 1 in 268,435,456
```

With 8 bits of randomness the chance of guessing the right address is 1 in
256; that can be hit within a few hundred tries. As the number of
bits grows the chance drops fast: every extra bit doubles the guessing
work. That is why ASLR on 64-bit systems is much stronger than on 32-bit
systems, whose address space is narrow.

## The layers complement each other

<figure class="fig"><div class="flow">
  <span class="node">Overflow</span><span class="arrow">→</span>
  <span class="node acc">Canary: caught on return</span><span class="arrow">→</span>
  <span class="node acc">DEP: data does not run</span><span class="arrow">→</span>
  <span class="node acc">ASLR: address hidden</span><span class="arrow">→</span>
  <span class="node ok">Program protected</span>
</div><figcaption>None of them fixes the bug; each makes it harder for the bug to turn into damage.</figcaption></figure>

| Protection | What does it protect? | Where is it turned on? |
|---|---|---|
| **Stack canary** | Catches return information damaged by an overflow | Compiler (`-fstack-protector-strong`, `/GS`) |
| **DEP / NX** | Stops data regions running as code | Processor + operating system |
| **ASLR** | Makes addresses unpredictable | Operating system + position-independent build (PIE) |
| **CFI** (control-flow integrity) | Lets the program jump only to allowed places | Compiler + operating system |

None of these protections **fixes the bug**: the overflow is still there.
Each one only makes it harder to turn the bug into damage. That is why
they are used together (**defense in depth**) and they do not replace
moving to a memory-safe language or fixing the bug. A program built with a
protection switched off is one of the first things flagged in a security
review.

## Summary

- Protections do **not fix** a memory bug, they shrink its damage; they are
  used together.
- **Stack canary:** a random, secret value between the buffer and the
  return information; checked before returning.
- **DEP / NX (W^X):** a region is either writable or executable; data does
  not run as code.
- **ASLR:** addresses are random on every run; its strength grows with the
  number of bits, every bit doubles the guessing.
- The real fix is still **memory-safe code**: protections are the second
  line of defense.
