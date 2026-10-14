# Overall Review

You have reached the end of the Prompt Engineering and LLM Applications
module. We started by seeing that a prompt is a message list; we made the
instruction clear, gave examples, made the model reason step by step, and
parsed and validated the answer strictly. Then we moved to the
application: the system message, templates, chains, tools, the agent loop
and memory. At the end we measured and defended: evaluation, injection
defence, errors and cost, systematic improvement, and a support assistant
that joins them all. This section walks the path once more.

<figure class="fig">
  <div class="flow">
    <span class="node">Basics<br><small>00–04</small></span><span class="arrow">→</span>
    <span class="node">Application<br><small>05–07</small></span><span class="arrow">→</span>
    <span class="node">Tools and agents<br><small>08–10</small></span><span class="arrow">→</span>
    <span class="node">Measure and defend<br><small>11–13</small></span><span class="arrow">→</span>
    <span class="node acc">System and project<br><small>14–15</small></span>
  </div>
  <figcaption>The module's path: build the prompt, build the application, add tools and memory, measure and defend, join it all.</figcaption>
</figure>

## 1. The basics of a prompt (Sections 0–4)

- A prompt is a **message list**: system, user, assistant. For short
  messages 73–78% of the tokens sent are the fixed part; the answer is
  **parsed strictly**, and half of the example replies (3 of 6) were
  accepted (00).
- **Clear instructions** are measurable rules; both the prompt and the
  checker are made from the same rule dictionary. Data is separated with a
  **delimiter** and escaped (01).
- **Few-shot prompting:** the number of examples grows the tokens (0
  examples 56, 10 examples 287 tokens); examples are chosen to cover the
  categories, and 5 random examples missed a category in 932 of a thousand
  draws (02).
- **Step-by-step reasoning** makes a calculation error visible but does not
  check it; the code does the calculation. The answer with steps takes 10
  times the tokens (03).
- **Structured output:** parse, validate with a schema, repair once if
  needed (input tokens from 16 to 114 in the repair) (04).

## 2. Building the application (Sections 5–7)

- The **system message** is built from settings and tracked with a version
  digest; the answer is checked against the rules (05).
- **Templates:** `str.format` breaks on a JSON example, `safe_substitute`
  leaves a missing value silently; values are validated and long text is
  cut in the middle (06).
- **Chains:** every step is small and checkable; a single prompt took 412
  tokens, the chain 215; a failed step stops the chain (07).

## 3. Tools, agents and memory (Sections 8–10)

- **Tool calling:** the model proposes the call, the program validates and
  runs it; confirmation for irreversible jobs; the answer is grounded in
  the tool's result (08).
- **The agent loop:** a limit on rounds and tokens is a must; the agent
  repeating the same call spent 516 tokens in 5 rounds and gave no result
  (09).
- **Memory:** the whole history took 1565 tokens; the last 4 messages lost
  the order number; important facts are kept in a separate memory (10).

## 4. Measuring and defending (Sections 11–13)

- **Evaluation:** form and correctness are counted separately; `v2` got 36
  of 40 messages right, `v1` 31; the interval of the difference is between
  0 and 0.25 (11).
- **Prompt injection:** there is no complete fix; a detector (precision
  0.8, recall 0.57), least privilege, confirmation and an output check
  together (12).
- **Errors and cost:** a temporary error is retried with an exponential
  wait with jitter, a permanent one is not; a cut answer makes you pay for
  the prompt again; the cache did not send 55 of 100 requests to the model
  (13).

## 5. Working systematically and the project (Sections 14–15)

- **Systematic improvement:** decide on the development set, look at the
  test at the end; the memorising `v3` scored 1.00 on development and the
  same as `v2` on test (0.75) (14).
- **The support assistant:** input filter → classify → order data → answer
  → output check; 9/10 on ten scenarios, 10/10 with a single change (15).

## All together: where do the tokens go?

The assistant from the capstone makes two calls for every message. If we
passed all 40 support messages through the assistant, how much of the
tokens would go to the fixed system messages and how much to what the
customer wrote?

```python
from llm_client import count_message_tokens
from shop_data import LABELS, TICKETS

CLASSIFY = "Answer with one word: " + ", ".join(LABELS) + "."
SYSTEM = ("You are the support assistant of an outdoor shop. Answer in at most "
          "two sentences, only from the order data you are given. Never promise "
          "a refund, a delivery date or a discount.")

fixed = total = 0
for ticket in TICKETS:
    answer_prompt = "Order data: none\n\nCustomer: " + ticket["text"]
    for system, user in [(CLASSIFY, ticket["text"]), (SYSTEM, answer_prompt)]:
        total += count_message_tokens([{"role": "system", "content": system},
                                       {"role": "user", "content": user}])
        fixed += count_message_tokens([{"role": "system", "content": system}])
print(f"{len(TICKETS)} messages, {2 * len(TICKETS)} calls, {total} input tokens")
print(f"fixed system part {fixed} ({fixed / total:.0%})")
```

```text
40 messages, 80 calls, 5054 input tokens
fixed system part 3400 (67%)
```

40 messages, 80 calls with two calls per message and 5054 input tokens; 3400
of them (67%) are the system messages repeated unchanged on every call. The
part the customer wrote is a little over a third. This number brings
several lessons of the module together: every unneeded sentence in the
system message is paid again on every call (The Anatomy of a Prompt), a
fixed start suits some services' prefix cache (Errors, Retries and Cost),
and an addition that brings no success is only a cost (Improving Prompts
Systematically). The counter is simplified; output tokens and the order
data are not in this count.

## Next

In this module we built everything with recorded replies and a toy model;
the program gave the same result on every computer. When you start working
with a real model, the only thing that changes is where the answers come
from: the message list, the parser, tool validation, the evaluation set,
the injection defence and the retries stay the same. And the rule that does
not change is this: **the effect of a prompt is measured on your model,
with your set.**
