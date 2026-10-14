Questions to ask before showing an LLM answer to a user:

1. **Does the answer rest on a source?** Does it come from the documents given,
   or from the model's general knowledge? If there is a source, check the
   details (numbers, dates, names) against it.
2. **Are the source numbers right?** Does the number shown exist, and does that
   chunk really contain the claim?
3. **Is the model sure?** On an important question take a few answers and look
   at how much they agree. Scattered answers are a sign of weak grounding.
4. **What happens if you are not sure?** Saying "I don't know" or "I could not
   find it in the source" is better than giving a wrong answer. Choose the
   threshold by the balance between the number of answers given and accuracy.
5. **How good is your checker?** Measure its precision and recall on labelled
   examples; look one by one at what it misses.

**Which check catches what?**

| Check | Catches | Misses | Price |
|---|---|---|---|
| Detail check | Made-up numbers, dates, names | A change in meaning ("store credit") | Very cheap |
| Source number check | A source that does not exist or is wrong | A sentence with the right source but a wrong reading | Cheap |
| Self-consistency | A gap in knowledge | A consistent but wrong answer | Many calls per question |
| Human review | Most errors | Fatigue, scale | Expensive |

**Common mistakes:**

- **Taking temperature 0 for reliability.** The answer becomes repeatable, not
  correct.
- **Searching inside the text instead of comparing with a set.** The number
  "1" is found inside "17:00" and taken as supported.
- **Trusting the checker without measuring it.** In the lesson one invention
  slipped through in twelve examples; on real data the rate may differ.
- **Never planning to abstain.** The interface must be able to show an "I don't
  know" answer.
