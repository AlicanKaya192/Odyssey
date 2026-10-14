Before sending a prompt, ask these questions:

| Question | What happens if it is missing? |
|---|---|
| Who does the model act as? | The model picks the tone and level of detail |
| Is the task clear in one sentence? | The model may do another job (a comment instead of a summary) |
| Is the information it needs in the prompt? | The model fills what it does not know with a guess |
| Is the answer's format written down? | The program cannot parse the answer |
| Is the input kept apart from the instructions? | A sentence in the input may be read as an instruction |
| How much room does the answer need? | A small `max_tokens` cuts the answer, a large one takes room in the window |

**On the program side:**

1. Build the message list with a function; keep the fixed parts in one
   place.
2. Log the request that was sent (role, content, `max_tokens`,
   temperature).
3. Parse the answer strictly; clean only harmless differences (spaces,
   capital letters, a final full stop).
4. Do not fix an answer outside the allowed values with a guess; set it
   apart (`needs_review`) or ask again with an error message.
5. Measure the system message's tokens; multiply by the number of calls.

**Common mistakes:**

- **Writing the prompt by hand as one long text.** It becomes invisible
  which part does what and how much room it takes.
- **Searching the answer text and taking the first match.** In the lesson
  `"warranty, maybe payment"` gave `warranty`; the hesitation was lost.
- **Assuming a principle works.** Example replies do not measure a
  model's behaviour; measure the principle's effect on your own model
  with your own examples.
