# The Agent Loop

In the previous section the model called a tool, the program gave the
result and the model wrote an answer: a single round. Some questions need
several tool calls, and you cannot know in advance which calls are
needed: "Which of my two orders cost more, and has it shipped?" The model
first asks for the two amounts, then for the status of the more expensive
one. This loop, in which the model picks the next action every round and
the program runs the tools and gives back the results, is called an
**agent**. In this section we build an agent loop and focus on what makes
it safe: a step limit, catching a repeated call, giving errors back and
the token price that grows every round.

<figure class="fig">
  <div class="flow">
    <span class="node">Model: next action</span>
    <span class="arrow">→</span>
    <span class="node acc">Program: run the tool</span>
    <span class="arrow">→</span>
    <span class="node">Add the result to the history</span>
    <span class="arrow">→</span>
    <span class="node">Answer or a new round</span>
  </div>
  <figcaption>The program, not the model, runs the loop: the program decides when to stop.</figcaption>
</figure>

## The loop

We use two tools: `get_order`, which gives an order's status, and
`order_total`, which computes its amount (with the fictional orders in
`shop_data.py`). The loop goes round at most `max_steps` times; if the
same call comes a second time it is not run, and an "you already did
this" error goes back to the model. We keep the input tokens of every
round in a trace:

```python
import json

from llm_client import ChatClient
from shop_data import ORDERS

SYSTEM = "You are a shop assistant. Use the tools; answer when you know."
SCHEMA = [{"name": "get_order", "parameters": ["order_id"]},
          {"name": "order_total", "parameters": ["order_id"]}]


def get_order(order_id):
    order = ORDERS[order_id]
    return {"status": order["status"], "date": order["date"]}


def order_total(order_id):
    items = ORDERS[order_id]["items"]
    return {"total": round(sum(p * c for _, p, c in items), 2)}


TOOLS = {"get_order": get_order, "order_total": order_total}


def run_tool(call):
    function = TOOLS.get(call["name"])
    if function is None:
        return {"error": f"unknown tool {call['name']}"}
    try:
        return function(**call.get("arguments", {}))
    except (TypeError, KeyError):
        return {"error": "wrong arguments"}


def agent(client, question, max_steps=5):
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": question}]
    seen, trace = set(), []
    for step in range(1, max_steps + 1):
        reply = client.chat(messages, tools=SCHEMA)
        trace.append(reply.input_tokens)
        if not reply.tool_calls:
            return reply.text, step, trace
        messages.append({"role": "assistant", "content": "",
                         "tool_calls": reply.tool_calls})
        for call in reply.tool_calls:
            key = json.dumps(call, sort_keys=True)
            if key in seen:
                result = {"error": "you already made this call"}
            else:
                result = run_tool(call)
            seen.add(key)
            messages.append({"role": "tool", "content": json.dumps(result)})
    return None, max_steps, trace
```

The loop has two exits: if the model gives an answer without calling a
tool, that answer; if `max_steps` is reached, `None`. The second exit
matters: a loop that trusts the model to say "done" and goes round forever
burns both money and time.

## Three scenarios

The three **example reply sequences** below stand for three cases: an
agent that solves the question, an agent that makes the same call again
and again, and an agent that starts with a wrong tool name and recovers
after the error.

```python
def call(name, order_id):
    return {"name": name, "arguments": {"order_id": order_id}}


QUESTION = "Which of ORD-10077 and ORD-61890 cost more, and has it shipped?"
SCRIPTS = {
    "solves": [
        {"tool_calls": [call("order_total", "ORD-10077"),
                        call("order_total", "ORD-61890")]},
        {"tool_calls": [call("get_order", "ORD-10077")]},
        "ORD-10077 cost more (214.90) and it was delivered.",
    ],
    "repeats": [{"tool_calls": [call("get_order", "ORD-10077")]}] * 6,
    "recovers": [
        {"tool_calls": [call("get_status", "ORD-10077")]},
        {"tool_calls": [call("get_order", "ORD-10077")]},
        "ORD-10077 was delivered on 2026-09-28.",
    ],
}
for name, script in SCRIPTS.items():
    text, steps, trace = agent(ChatClient(script), QUESTION)
    print(name, steps, trace, sum(trace))
    print("   ", text)
```

```text
solves 3 [50, 82, 114] 246
    ORD-10077 cost more (214.90) and it was delivered.
repeats 5 [50, 82, 105, 128, 151] 516
    None
recovers 3 [50, 73, 105] 228
    ORD-10077 was delivered on 2026-09-28.
```

The first agent answered in three rounds: it first asked for the two
amounts with two calls in one round, then for the status of the more
expensive order. The second repeated the same call; from the second round
on it got the "you already made this call" error every time but did not
stop, and in the fifth round the program stopped it, the answer is
`None`. The third started with a tool that does not exist and switched to
the right tool after seeing the error. But its answer leaves the question
half answered: it does not say which order cost more. A loop ending
cleanly does not mean the answer is right and complete; evaluation shows
that.

## Every round costs more

The numbers in the trace grow every round: the agent sends the history,
the tool calls and their results again in every round. The repeating
agent spent 516 input tokens in five rounds and produced
nothing. Two limits are set together for an agent: a **step limit** and a
**token budget**. Whichever is reached first stops the loop, and the job
goes to a person or a fixed path.

## Rules that make an agent safe

- **The program runs the loop.** The step limit, the token budget and the
  time limit are in the program; they do not depend on the model saying
  "done".
- **Catch repetition.** The same call with the same arguments is usually a
  sign that the agent is stuck.
- **Give errors back.** An unknown tool or a wrong argument does not crash
  the program; the error goes to the model and the model may recover (the
  third scenario).
- **The tool rules of the previous section hold as they are:** the
  allow-list, argument validation, confirmation for irreversible jobs.
  These rules matter even more because an agent calls more tools.
- **Log the trace.** For every round: which tool, which arguments, which
  result and how many tokens; why an agent gave a wrong answer can only be
  understood from the trace.

## When an agent?

An agent helps when the order of the steps is not known in advance. If
the steps are always the same (classify, extract, write the answer), the
chain from the earlier sections is more predictable, cheaper and easier
to test. The rule: **try a chain first; switch to an agent only if the
order of the steps really changes with the input.**

## Summary

- An agent is a loop in which the model picks the next action every round
  and the program runs the tools.
- The loop's exit is not only the model's answer but the program's
  limits: a step limit and a token budget.
- A repeated identical call is caught and reported to the model as an
  error.
- Tool errors are given back to the model; the agent may recover.
- Every round sends the history again; the token price grows with the
  rounds.
- Fixed steps: a chain; changing steps: an agent.
