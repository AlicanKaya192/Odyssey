"""A chat client that answers from a script of recorded replies (read-only).

No real model is called. Every reply comes from a script written in advance,
so the replies are examples, not measurements of any model, and an exercise
gives the same result on every computer.

The token counter is simplified: real models split text with their own
tokenizer, so real counts differ.
"""
import copy
import re

PIECE = re.compile(r"\w+|[^\w\s]")
CHARS_PER_TOKEN = 4
MESSAGE_OVERHEAD = 4
REPLY_PRIMER = 2
ROLES = ("system", "user", "assistant", "tool")


class ContextLengthError(Exception):
    """The input and the requested output do not fit in the context window."""


class RateLimitError(Exception):
    """Too many requests; trying again a little later may work."""


class ServerError(Exception):
    """The service failed for this request; trying again may work."""


def count_tokens(text):
    """Simplified token count.

    Every punctuation mark is one token; a word is one token per started
    group of four characters ("cat" 1, "capital" 2).
    """
    return sum(-(-len(piece) // CHARS_PER_TOKEN) for piece in PIECE.findall(text))


def count_message_tokens(messages):
    """Tokens the model reads for a message list, role markers included."""
    return sum(MESSAGE_OVERHEAD + count_tokens(m["content"]) for m in messages) + REPLY_PRIMER


def cut_to_tokens(text, limit):
    """The longest beginning of `text` that has at most `limit` tokens."""
    used, end = 0, 0
    for match in PIECE.finditer(text):
        cost = -(-len(match.group()) // CHARS_PER_TOKEN)
        if used + cost > limit:
            break
        used, end = used + cost, match.end()
    return text[:end]


class Reply:
    """One answer: the text, why generation stopped and the token usage."""

    def __init__(self, text, finish_reason, input_tokens, output_tokens, tool_calls=None):
        self.text = text
        self.finish_reason = finish_reason
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.tool_calls = tool_calls or []

    def __repr__(self):
        return f"Reply({self.text!r}, finish_reason={self.finish_reason!r})"


class ChatClient:
    """Answers each call with the next item of `script`.

    A script item is a reply text, a function that receives the message list
    and returns a reply text, a dict {"tool_calls": [...]} for a tool call, or
    an exception instance, which is raised for that call. Every call is kept
    in `calls`, so a program can be checked for what it sent.
    """

    def __init__(self, script, context_window=4096):
        self.script = list(script)
        self.context_window = context_window
        self.calls = []

    def chat(self, messages, max_tokens=256, temperature=0.0, tools=None):
        check_messages(messages)
        input_tokens = count_message_tokens(messages)
        if input_tokens + max_tokens > self.context_window:
            raise ContextLengthError(
                f"{input_tokens} input + {max_tokens} output tokens > window of {self.context_window}")
        self.calls.append({"messages": copy.deepcopy(messages), "max_tokens": max_tokens,
                           "temperature": temperature, "tools": tools})
        if not self.script:
            raise RuntimeError("the script has no more replies")
        item = self.script.pop(0)
        if isinstance(item, Exception):
            raise item
        if isinstance(item, dict):
            return Reply("", "tool_calls", input_tokens, 0, item["tool_calls"])
        text = item(messages) if callable(item) else item
        if count_tokens(text) > max_tokens:
            text = cut_to_tokens(text, max_tokens)
            return Reply(text, "length", input_tokens, count_tokens(text))
        return Reply(text, "stop", input_tokens, count_tokens(text))


def check_messages(messages):
    """Reject a message list a chat API would reject."""
    if not messages:
        raise ValueError("the message list is empty")
    for m in messages:
        if m.get("role") not in ROLES:
            raise ValueError(f"unknown role: {m.get('role')!r}")
        if not isinstance(m.get("content"), str):
            raise ValueError("every message needs a text content")
