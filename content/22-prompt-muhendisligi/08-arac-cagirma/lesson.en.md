# Tool Calling

A language model cannot know where a customer's order is; that
information is in the shop's database. When something the model does not
know or cannot do is needed, it is introduced to **tools**: "there is a
function that fetches an order by its number". Instead of an answer, the
model returns a **tool call**: which tool it wants to call, with which
arguments. The **program** runs the tool and gives the result back to the
model; the model writes the final answer with that result. In this
section we build this loop and see the most important rule: the call the
model asks for is not run without the program **validating** it.

<figure class="fig">
  <div class="flow">
    <span class="node">Question + tool list</span>
    <span class="arrow">→</span>
    <span class="node">Model: tool call</span>
    <span class="arrow">→</span>
    <span class="node acc">Program validates and runs</span>
    <span class="arrow">→</span>
    <span class="node">Model: final answer</span>
  </div>
  <figcaption>The model does not run the tool; it only says it wants to call it.</figcaption>
</figure>

## Defining the tools

Each tool has a name, a description telling the model when to use it,
and arguments. With the fictional orders we added to `shop_data.py`, let
us write two tools: `get_order`, which fetches an order, and
`cancel_order`, which cancels one. Cancelling cannot be undone; we mark it
separately:

```python
import json
import re

from shop_data import ORDERS


def get_order(order_id):
    order = ORDERS.get(order_id)
    if order is None:
        return {"error": f"no order {order_id}"}
    return {"order_id": order_id, "status": order["status"],
            "date": order["date"]}


def cancel_order(order_id):
    return {"order_id": order_id, "cancelled": True}


TOOLS = {
    "get_order": {"function": get_order, "confirm": False,
                  "description": "Look up an order's status by its number.",
                  "parameters": {"order_id": r"ORD-\d{5}"}},
    "cancel_order": {"function": cancel_order, "confirm": True,
                     "description": "Cancel an order that has not shipped.",
                     "parameters": {"order_id": r"ORD-\d{5}"}},
}


def schema(tools):
    return [{"name": name, "description": tool["description"],
             "parameters": list(tool["parameters"])}
            for name, tool in tools.items()]


print(json.dumps(schema(TOOLS)[0], indent=1))
print(get_order("ORD-48213"))
```

```text
{
 "name": "get_order",
 "description": "Look up an order's status by its number.",
 "parameters": [
  "order_id"
 ]
}
{'order_id': 'ORD-48213', 'status': 'shipped', 'date': '2026-10-09'}
```

Only `schema(TOOLS)` goes to the model: names, descriptions, argument
names. The functions themselves, the argument patterns and the "needs
confirmation" mark stay in the program. Real chat APIs want the arguments
as JSON Schema, with types and descriptions; the list here is a short
form of the same idea. The descriptions matter: the model often decides
which tool to pick and when by looking only at the description.

## Validating the call

The tool call the model returns is a **request**, not an order. The model
may ask for a tool that does not exist, an argument in the wrong form or
an irreversible job the user did not ask for. The program checks every
call before running it:

```python
def run_tool(call):
    tool = TOOLS.get(call["name"])
    if tool is None:
        return {"error": f"unknown tool {call['name']}"}
    args = call.get("arguments", {})
    if set(args) != set(tool["parameters"]):
        return {"error": "arguments must be " + ", ".join(tool["parameters"])}
    for name, pattern in tool["parameters"].items():
        if not re.fullmatch(pattern, str(args[name])):
            return {"error": f"{name} has the wrong form"}
    if tool["confirm"]:
        return {"pending": "needs the customer's confirmation"}
    return tool["function"](**args)


CALLS = [{"name": "get_order", "arguments": {"order_id": "ORD-48213"}},
         {"name": "get_order", "arguments": {"order_id": "48213"}},
         {"name": "get_order", "arguments": {"order_id": "ORD-99999"}},
         {"name": "cancel_order", "arguments": {"order_id": "ORD-23345"}},
         {"name": "delete_account", "arguments": {}}]
for call in CALLS:
    print(call["name"], json.dumps(run_tool(call)))
```

```text
get_order {"order_id": "ORD-48213", "status": "shipped", "date": "2026-10-09"}
get_order {"error": "order_id has the wrong form"}
get_order {"error": "no order ORD-99999"}
cancel_order {"pending": "needs the customer's confirmation"}
delete_account {"error": "unknown tool delete_account"}
```

Only one of the five example calls returned an order's information. The
order number in the wrong form, the order that does not exist and the
unknown tool each came back as an **error result**; the program did not
crash, the error will go back to the model and the model can tell the
customer something correct. The cancel request was not run: it is
waiting for confirmation.

Three rules:

- **Only tools on the allow-list.** Never run the name the model gives
  directly as a function or a command (no `eval`, no `getattr`).
- **Always validate the arguments.** The model may carry a text the
  customer wrote into an argument; if the argument goes into a database
  query or a file path, that becomes a way in for an attack.
- **Irreversible jobs are not done without confirmation.** For
  cancelling, paying, deleting, the customer or an employee has the last
  word.

## The whole loop

Now let us join the question, the tool call, the tool result and the
final answer. The model's tool call is added to the history as an
`assistant` message, the tool's result as a message with the `tool` role.
The two **example replies** below are a tool call and a final answer that
uses the tool result:

```python
from llm_client import ChatClient

SYSTEM = ("You are a shop assistant. Use the tools to look up orders; "
          "never guess an order's status.")


def answer(client, question):
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": question}]
    reply = client.chat(messages, tools=schema(TOOLS))
    if reply.tool_calls:
        messages.append({"role": "assistant", "content": "",
                         "tool_calls": reply.tool_calls})
        for call in reply.tool_calls:
            messages.append({"role": "tool",
                             "content": json.dumps(run_tool(call))})
        reply = client.chat(messages, tools=schema(TOOLS))
    return reply.text, messages


client = ChatClient([
    {"tool_calls": [{"name": "get_order",
                     "arguments": {"order_id": "ORD-48213"}}]},
    "Your order ORD-48213 was shipped on 2026-10-09.",
])
text, messages = answer(client, "Where is my order ORD-48213?")
print([m["role"] for m in messages])
print(messages[-1]["content"])
print(text)
print(len(client.calls), "calls")
```

```text
['system', 'user', 'assistant', 'tool']
{"order_id": "ORD-48213", "status": "shipped", "date": "2026-10-09"}
Your order ORD-48213 was shipped on 2026-10-09.
2 calls
```

One question took two calls: one to get the tool call, one to write the
answer using the result. The second call also carries the first question,
the tool call and the tool result; that is the token price of using
tools.

In real APIs each tool call has an id and the `tool` message is tied to
that id; so when the model calls several tools at once, it does not get
mixed up which result belongs to which call. The client here simplifies
this.

## Does the answer rest on the tool result?

Even after getting the tool result, the model may write another date or
status in its answer. Because the tool result is structured, this is easy
to check with code: let us see whether the dates in the answer are the
same as the date in the tool result.

```python
def grounded(text, tool_result):
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)
    return all(date == tool_result.get("date") for date in dates)


result = get_order("ORD-48213")
for text in ["Your order ORD-48213 was shipped on 2026-10-09.",
             "Your order ORD-48213 was shipped on 2026-10-07."]:
    print(grounded(text, result), text)
```

```text
True Your order ORD-48213 was shipped on 2026-10-09.
False Your order ORD-48213 was shipped on 2026-10-07.
```

The second example reply writes a date that is not in the tool result,
and the check catches it. The idea we used in the previous module to
check answers that cite sources holds here too: **the tool result is the
answer's source.**

## Summary

- A tool is a function the program offers for a job the model does not
  know or cannot do; only its name, description and arguments go to the
  model.
- The model does not run the tool, it asks for a call; the program runs
  it and gives the result back.
- Every call is validated before running: the allow-list, argument
  patterns, confirmation for irreversible jobs.
- A faulty call does not crash the program; the error result goes back
  to the model.
- Using a tool means at least one more call.
- Compare the final answer with the tool result; structured facts such as
  dates, statuses and amounts can be checked with code.
