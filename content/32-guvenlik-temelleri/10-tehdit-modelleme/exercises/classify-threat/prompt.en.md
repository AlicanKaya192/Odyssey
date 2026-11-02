The team wrote the threats as plain sentences. The `KEYWORDS`
dictionary holds keywords for every STRIDE letter (ready in the starter
code).

`classify_threat(text)` should turn the sentence into lower case and try
the letters **in the order S, T, R, I, D, E**; return the **first** letter
one of whose keywords appears inside the sentence. `"?"` if there is none.

**Expected output:**

```
S attacker could impersonate a t
T grades may be altered in the d
I error page could expose every
E student can bypass the admin c
D a flood of requests could cras
R nothing is logged, so a teache
? the coffee machine is slow
```
