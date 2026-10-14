A checklist before opening an LLM assistant to customers:

**Measurement**

- [ ] There is an evaluation set built from real messages, with enough
  examples of every category, split into development and test.
- [ ] Attack messages and innocent messages that look like them are in the
  set too.
- [ ] The expected outcome is written for every kind of outcome (send,
  block, hand over, fallback).
- [ ] The final version was measured once on the test set and written in
  the log.

**Safety**

- [ ] The assistant has only the tools its job needs; irreversible jobs
  need a person's confirmation.
- [ ] There is no secret information in the system message.
- [ ] The output check grounds dates and numbers in the data; promises and
  claims of jobs it cannot do are caught; links come from an allow-list.
- [ ] A customer's data is not given to someone else from the cache.

**Resilience and cost**

- [ ] Temporary errors are retried with a limited wait with jitter;
  permanent errors are not.
- [ ] There is a time limit on the total waiting and a fallback answer.
- [ ] `max_tokens` fits the expected answer; tokens per message were
  measured.
- [ ] There is a daily spending limit.

**Operations**

- [ ] Messages handed over or blocked are logged; a person looks at them.
- [ ] Error rates are monitored (temporary and permanent separately).
- [ ] Every version of the prompt is kept; it is known which version went
  live when, and the old one can be restored.
- [ ] The customer knows they are talking to an AI assistant and can reach
  a person.
