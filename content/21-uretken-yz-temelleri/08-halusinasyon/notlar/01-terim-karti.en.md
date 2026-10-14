| Term | Meaning |
|---|---|
| **Hallucination** | Producing content without basis in a fluent way |
| **Unfaithfulness** | Adding a detail that is not in the given document while answering from it |
| **Self-consistency** | Asking the same question a few times and checking whether the answers agree |
| **Abstaining** | Giving no answer where certainty cannot be reached |
| **Grounding** | The answer resting on a source |
| **Citation** | Stating which chunk every claim of the answer comes from |
| **False positive** | Marking a correct answer as made up |
| **False negative** | Failing to catch a made-up answer |

**Keep in mind:**

- No setting prevents hallucination completely; the program measures, checks
  and abstains when needed.
- In the toy model consistency was 1.0 on known topics and 0.35 on unknown
  ones; a threshold of 0.6 brought the wrong answers to zero (20 calls per
  question).
- The detail check (numbers, times, names) is cheap but does not check the
  meaning: "store credit" slipped through.
- Consistency is a sign, not a proof; checkers are measured too.
