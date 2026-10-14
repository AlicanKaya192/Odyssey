Before putting a system that uses a generative model live:

**Bias**

1. Measure the results separately per group (selection rate, equal
   opportunity, error rate). Overall accuracy hides differences.
2. Look for proxy variables: removing the protected attribute is not enough.
3. If you choose a correction, write down its price and make sure the decision
   is taken by the institution, not by the technical team alone.

**Personal data**

1. Which personal data does the task really need? Do not collect what is not
   needed.
2. Mask the rest before it goes to the model and into the logs.
3. Measure the masker on example sentences; list the forms it misses.
4. Limit how long data is kept.

**Safety and transparency**

1. Tell users they are talking to a model and that it can make mistakes.
2. Leave the last word to a person in decisions that affect people.
3. Open a way to report wrong or harmful outputs; keep logs.
4. Take the measures from Module 2 against attacks like prompt injection.

**Common mistakes:**

- **Saying "we do not use the group, so we are fair":** in the section a proxy
  variable carried the bias.
- **Looking at a single fairness measure:** equal selection rates and equal
  opportunity may not agree.
- **Not measuring the masker:** the email written out in words slipped
  through.
- **Leaving responsibility to the model:** the model suggests, a person
  decides.
