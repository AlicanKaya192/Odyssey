This exercise shows you a trap with a name: **Simpson's paradox.**

The `records` table in the starter code holds the questions two teams
answered: the team, the difficulty of the question and the score.

**What you need to do:**

1. Compute the team averages and print **A and B side by side**.
2. Print the team with the higher average.
3. Print how many **hard** questions each team answered, side by side (A,
   then B).
4. Print the averages on the **easy** questions, side by side (A, then B).
5. Print the averages on the **hard** questions, side by side (A, then B).

**Expected output:**

```
74.0 61.0
A
2 8
80.0 85.0
50.0 55.0
```

**Now read the output.** On the overall average A is ahead: 74 against 61.

But look at the last two lines: **on the easy questions B is better (85 >
80), and on the hard questions B is better too (55 > 50).** B wins at both
levels, and A wins on the overall average.

The reason is on the third line: A answered only 2 hard questions and B
answered 8. B's average comes out low because the hard questions weigh it
down.

**The overall average is not lying, it is answering the wrong question.**
When you find a difference between groups, the question to ask is: *is
something else different about these groups too?* If the answer is yes, you
have to break it down by that column as well.
