import textwrap

from llm_client import ChatClient
from rag_tools import index, build_messages, make_reader


def answer(question, k):
    return ["", 0]


for question in ["Do gift cards expire?", "Do you sell bicycles?"]:
    text, tokens = answer(question, 3)
    print(tokens)
    print(textwrap.fill(text, 40))
