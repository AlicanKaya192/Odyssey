One line in the log for every prompt change:

| Version | Change | Reason (which error kind) | Development | Broken | Tokens |
|---|---|---|---|---|---|
| v1 | Baseline | — | 0.60 | — | 59 |
| v2 | Words from the meaning in the category definitions | 8 of 8 errors `unknown` | 0.90 | 0 | 100 |
| v3 | Words copied from the remaining errors | The 2 remaining errors | 1.00 | 0 | 139 |

The test set is measured only for the version chosen in the end, and noted
under its line. In this table `v3` has the highest development measure; but
its reason is "the remaining errors" and the words it adds have nothing to
do with the category: a sign of memorisation.

**Rules:**

1. One change per line.
2. Tie the reason to an error kind; "I wanted to try" is not a reason.
3. Next to the total, write the number of broken answers too.
4. Write the token count; length that brings no success is a cost.
5. Keep the full text of the version or its digest, so it can be found
   later which prompt got which measure.

**Common mistakes:**

- **Looking at the test set with every change.** The test set quietly turns
  into a development set.
- **Making several changes together.** It is not known which one helped and
  which one broke something.
- **Looking only at the total.** The answers can change while the total
  stays the same.
- **Trusting a difference of 0.05 on a small set.** In 20 messages that is
  a single message.
- **Putting development messages into the prompt as examples.** Those
  messages are then no longer a measure but questions whose answer is
  written in the prompt.
