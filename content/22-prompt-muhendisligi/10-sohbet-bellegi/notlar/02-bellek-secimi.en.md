Which way do you use when?

| Way | Tokens | Does it forget? | Mind |
|---|---|---|---|
| The whole history | Grows fast with the number of messages | No | May not fit the window |
| The last N messages | Stays fixed | Yes, older facts | The simplest way |
| Summary + last N | Few, but there is a summary call too | May drop details | The summary must be checked too |
| Fact memory + last N | Few | Does not forget the facts in memory | Personal data; filter and deletion |

**When building a fact memory:**

1. Write down which facts are needed: name, order number, the chosen
   product. Do not keep what is not needed.
2. Extract the facts with code (regular expressions) or with a model
   (JSON); validate in both cases.
3. Filter before storing: passwords, card numbers, ID numbers, health
   information do not go in.
4. Add the memory to the system message as a short line.
5. Tie the memory to the user; offer a way to view and delete it; give
   records a lifetime.

**Common mistakes:**

- **Storing everything.** Memory is a customer record; more than needed is
  both a risk and tokens.
- **Trusting a summary blindly.** In the lesson the summary dropped the
  order number.
- **Using one user's memory in another conversation.** The most serious
  privacy error.
- **Not validating an extracted fact.** A wrong order number left in
  memory goes to the model in every call.
