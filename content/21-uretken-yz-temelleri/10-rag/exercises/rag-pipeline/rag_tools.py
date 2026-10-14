"""The RAG setup from section 10 (read-only): prompt, example reader and pipeline."""
import re
from retrieval import Index, by_sentence, QUESTIONS
from llm_client import ChatClient

index = Index(by_sentence())
NOT_FOUND = "I could not find this in the sources."
SYSTEM = ("Answer only from the numbered sources. Cite the source number "
          "like [2]. If the sources do not contain the answer, reply: "
          + NOT_FOUND)


def build_messages(question, found):
    sources = "\n".join(f"[{i}] {text}"
                        for i, ((_, text), _) in enumerate(found, 1))
    user = f"Sources:\n{sources}\n\nQuestion: {question}"
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": user}]


STOP = {"the", "a", "an", "is", "are", "do", "does", "i", "my", "you",
        "to", "of", "in", "for", "can", "how", "what", "when", "it", "on",
        "and", "or", "will", "if", "be", "me", "we", "your", "with", "at",
        "much", "long", "many"}


def words(text):
    found = re.findall(r"[a-z0-9]+(?:[.:][0-9]+)?", text.lower())
    return {w for w in found if w not in STOP}


def make_reader(min_overlap):
    def reader(messages):
        user = messages[-1]["content"]
        question = user.split("Question: ")[-1]
        best, best_overlap = NOT_FOUND, 0
        for n, source in re.findall(r"\[(\d+)\] (.+)", user):
            overlap = len(words(question) & words(source))
            if overlap > best_overlap:
                best, best_overlap = f"{source} [{n}]", overlap
        return best if best_overlap >= min_overlap else NOT_FOUND
    return reader


def rag(question, k=3, min_overlap=2):
    found = index.search(question, k) if k else []
    client = ChatClient([make_reader(min_overlap)])
    return client.chat(build_messages(question, found), max_tokens=100)
