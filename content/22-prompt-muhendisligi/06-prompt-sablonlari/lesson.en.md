# Prompt Templates

In a real application a prompt is not written by hand; it is built again
in every call from a **template**: the fixed text stays the same and
**variables** such as the customer's message, the order number and
document chunks are put in. A template looks like a simple text
operation, but it has three traps and all three work silently: the
braces of a JSON example, variables left missing and template marks that
come from inside a variable. In this section we really run all three in
Python and write a safe template function.

## `str.format` and JSON

In Python `str.format` comes to mind first. But if our instruction
contains a JSON example, the braces get mixed up with `format`'s own
marks:

```python
TEMPLATE = ('Put the message into one category.\n'
            'Answer as JSON: {"category": "<name>"}\n'
            'Message: {message}')
try:
    print(TEMPLATE.format(message="Where is my parcel?"))
except KeyError as error:
    print("KeyError:", error)

SAFE = ('Put the message into one category.\n'
        'Answer as JSON: {{"category": "<name>"}}\n'
        'Message: {message}')
print(SAFE.format(message="Where is my parcel?"))
```

```text
KeyError: '"category"'
Put the message into one category.
Answer as JSON: {"category": "<name>"}
Message: Where is my parcel?
```

`format` took the `{"category": "<name>"}` part for a variable, and since
no such variable was given it raised an error. The fix is to double the
braces in the JSON (`{{` and `}}`). At least this error is **loud**: the
program stopped before running.

## A silently missing variable

`string.Template` uses placeholders of the form `$name`; they do not
clash with JSON braces. It has two functions and the difference matters:

```python
from string import Template

t = Template("Hello $name, your order $order_id is on its way.")
print(t.safe_substitute(name="Ada"))
try:
    t.substitute(name="Ada")
except KeyError as error:
    print("KeyError:", error)
```

```text
Hello Ada, your order $order_id is on its way.
KeyError: 'order_id'
```

`safe_substitute` leaves the missing variable as it is and says nothing:
a prompt containing `$order_id` goes to the model, and the model
interprets it in its own way. `substitute` raises an error. When
building prompts, **a loud error is better than a silent one**: a missing
variable must be caught before the model runs.

## A mark from inside a variable

Writing templates in the form `{{name}}` and doing a `replace` for each
variable is also common. What happens if the customer's message contains
a template mark?

```python
import re

SLOT = re.compile(r"\{\{(\w+)\}\}")
T = "Customer {{name}} wrote: {{message}}\nOrder: {{order_id}}"
VALUES = {"name": "Ada", "message": "Is {{order_id}} shipped?",
          "order_id": "ORD-48213"}


def render_naive(template, values):
    for name, value in values.items():
        template = template.replace("{{" + name + "}}", str(value))
    return template


def render(template, values):
    names = set(SLOT.findall(template))
    missing, unused = names - values.keys(), values.keys() - names
    if missing or unused:
        raise ValueError(f"missing {sorted(missing)}, unused {sorted(unused)}")
    return SLOT.sub(lambda m: str(values[m.group(1)]), template)


print(render_naive(T, VALUES))
print(render(T, VALUES))
try:
    render(T, {"name": "Ada"})
except ValueError as error:
    print("ValueError:", error)
```

```text
Customer Ada wrote: Is ORD-48213 shipped?
Order: ORD-48213
Customer Ada wrote: Is {{order_id}} shipped?
Order: ORD-48213
ValueError: missing ['message', 'order_id'], unused []
```

The version that does `replace` one after another **changed** the
customer's message: the `{{order_id}}` inside the message was filled by
the `replace` that came after the message was put into the template.
Here it looks harmless, but the same path lets a text the customer wrote
pull into its own message a hidden value placed elsewhere in the template
(an internal note, another customer's data). The safe `render` does two
things:

- It fills the template **in one pass** (`SLOT.sub`): a value that was
  put in is not scanned again.
- It compares the template's variables with the given values and stops
  before running if a variable is missing or unused. An unused variable
  is often a typo (`order` instead of `order_id`).

## A budget for a variable

A variable can be very long: a customer writes a long message, a document
chunk comes out bigger than expected. Text over the budget must be cut,
but **where** you cut it matters:

```python
def fit_start(text, max_words):
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + " ..."


def fit_middle(text, max_words):
    words = text.split()
    if len(words) <= max_words:
        return text
    head = max_words // 2
    tail = max_words - head
    return " ".join(words[:head]) + " ... " + " ".join(words[-tail:])


LONG = ("I bought the Trail 40 backpack in May. " * 6
        + "Yesterday the main zip broke and I need it for a trip on Friday.")
print(len(LONG.split()), "words")
for fit in [fit_start, fit_middle]:
    short = fit(LONG, 24)
    print(fit.__name__, len(short.split()), "zip" in short)
```

```text
62 words
fit_start 25 False
fit_middle 25 True
```

The version that cuts from the start dropped the real point of the
message (the zip broke, it is needed on Friday); the version that cuts
the middle kept the beginning and the end. Which is right depends on the
data: in support messages the real request is often at the end, in a
document it is the title and the first paragraph. Also show that you cut
(`...`); the model should know the text is incomplete.

## Managing templates

- **Keep templates apart from the code and named:** `classify`,
  `summarize`, `reply`. Give each a **version**; when you change it, open
  a new version and do not delete the old one. Evaluation (in later
  sections) compares two versions on the same set.
- **Log the template's name and version** (like the digest in the System
  Messages section).
- **Test the template:** build an example with the expected variables
  for every template and read the result once with your own eyes; `render`
  not raising an error is not enough.

## Summary

- A template builds the prompt in every call from fixed text and
  variables.
- In `str.format` the braces of a JSON example are doubled (`{{ }}`);
  otherwise `KeyError`.
- `safe_substitute` silently leaves a missing variable; when building
  prompts a missing variable should raise an error.
- `replace` one after another also fills marks inside the customer's
  text; fill the template in one pass and check the variable list.
- When fitting a long variable into a budget, mind where you cut and show
  that you cut.
- Give templates names and versions; log them.
