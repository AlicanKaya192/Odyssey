import textwrap

from llm_client import ChatClient
from rag_tools import index, build_messages, make_reader


def answer(question, k):
    found = index.search(question, k)
    client = ChatClient([make_reader(2)])
    reply = client.chat(build_messages(question, found), max_tokens=100)
    return [reply.text, reply.input_tokens]


for question in ["Do gift cards expire?", "Do you sell bicycles?"]:
    text, tokens = answer(question, 3)
    print(tokens)
    print(textwrap.fill(text, 40))
