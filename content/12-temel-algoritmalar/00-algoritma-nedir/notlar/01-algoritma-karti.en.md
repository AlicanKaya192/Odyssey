A short card to keep at hand while writing an algorithm and after.

## Five properties

| Property | Question |
|---|---|
| Input | What does the algorithm work with? Of what type, in what range? |
| Output | What does it return? What does it return if the input is unexpected? |
| Definiteness | Does every step have one meaning? Not "wait a bit" but "wait 8 minutes". |
| Finiteness | Does it finish on every input? Is there a path into an endless loop? |
| Correctness | Does it give the right result on every input, not just on the example? |

## Before writing

1. Write the problem in your own words: what is the input, what is the
   output?
2. Solve a small example **by hand** and note step by step what you did.
3. Write those steps as pseudocode.
4. Try the pseudocode on paper with an edge case (an empty list, say).
5. Only then turn it into Python.

## Edge case checklist

- Empty input: `[]`, `""`, `0`
- One element: `[5]`
- All equal: `[7, 7, 7]`
- Negatives and zero: `[-5, -2, 0]`
- Where the answer is: start, end, middle
- Repeated values: is "the first" or "the last" wanted?
- Very large input: does the algorithm still finish in reasonable time?

## The starting value trap

When looking for "the largest" or "the smallest", do not start with a
**fixed number** (`0`, `1000`); you cannot know what range the data is in.
There are two safe ways:

- Start with the first element: `largest = numbers[0]`.
- Start with a value meaning "none yet": `largest = None`, and in the loop
  `if largest is None or number > largest:`.

For something like a sum, the right start is the operation's **identity
element**: `0` for addition, `1` for multiplication.
