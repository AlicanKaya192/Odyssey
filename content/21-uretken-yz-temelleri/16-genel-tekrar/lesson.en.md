# Overall Review

You have reached the end of the Generative AI Fundamentals module. We started
by drawing a sample from a distribution; we generated images and points with
the autoencoder, the VAE, the GAN and diffusion. Then we moved to large
language models: we measured how they generate, tokens and cost, and
hallucination; we chunked and searched documents, built RAG and evaluated it;
we tried fine-tuning, alignment and LoRA; we measured bias and personal data,
and built a document Q&A system. This section walks the path once more.

<figure class="fig">
  <div class="flow">
    <span class="node">Generative models<br><small>00–05</small></span><span class="arrow">→</span>
    <span class="node">Language models<br><small>06–08</small></span><span class="arrow">→</span>
    <span class="node">RAG<br><small>09–11</small></span><span class="arrow">→</span>
    <span class="node">Adaptation<br><small>12–13</small></span><span class="arrow">→</span>
    <span class="node acc">Responsibility and project<br><small>14–15</small></span>
  </div>
  <figcaption>The module's path: generate samples from a distribution, understand the language model, ground it in documents, adapt the model, build a responsible system.</figcaption>
</figure>

## 1. Generative models (Sections 0–5)

- A **generative model** learns the data's distribution and draws new samples
  from it; we check memorisation with the nearest-neighbour distance (00).
- **Sampling:** the probability ruler, inverse transform, rejection
  sampling (01).
- The **autoencoder** compresses but its latent space is disorderly: a clear
  digit from a random code 32% of the time (02).
- The **VAE** pulls the code towards the standard normal: codes drawn from it
  gave all 10 digits (03).
- The **GAN** is sharp but fragile: at learning rate 0.01 two clusters vanished
  with two seeds (04).
- **Diffusion** learns to take the noise back: eight clusters with three seeds
  at the same setting; the price is 100-step generation (05).

## 2. Large language models (Sections 6–8)

- The model only continues; chat is a **template**. The finish reason is
  `stop` or `length` (06).
- The history is sent again in every call: over eight messages the total input
  was 4.5 times the last call; the **cost** is computed from input and output
  tokens (07).
- **Hallucination:** the model gives a fluent answer to what it does not know
  too. Self-consistency and source checks help catch it (08).

## 3. RAG (Sections 9–11)

- Documents are **chunked**, and the chunks closest to the question are found
  with **vector search**; chunk size is a trade-off (09).
- **RAG:** the chunks are numbered and put into the prompt, the answer rests on
  the source, and "not found" is said if it cannot be found (10).
- **Evaluation:** retrieval (recall@k, MRR), the answer and abstention are
  measured separately; most errors were in retrieval (11).

## 4. Adaptation (Sections 12–13)

- **Fine-tuning** can make the model forget the old; mixing in old data keeps
  it. A **reward model** learns from preferences, and from their biases too
  (12).
- **LoRA** writes the change with two low-rank matrices: full fine-tuning level
  with 714 parameters (13).

## 5. Responsibility and the project (Sections 14–15)

- **Bias** comes from the data; deleting the group column is not enough because
  of proxy variables. **Personal data** is masked and the masker is measured
  (14).
- **Document Q&A system:** mask → search → fit to the budget → prompt → answer
  → verify → log → measure (15).

## All together: why does RAG exist?

What would happen if we sent all the help articles to the model with every
question? Let us compare the token count with the search from 09:

```python
from retrieval import Index, by_sentence, QUESTIONS, DOCS, count_tokens

everything = sum(count_tokens(d["title"] + " " + d["text"]) for d in DOCS)
index = Index(by_sentence())
rag_tokens = [sum(count_tokens(text) for (_, text), _ in
                  index.search(q["q"], 3)) for q in QUESTIONS]
average = sum(rag_tokens) / len(rag_tokens)
print("all articles", everything, "tokens per question")
print(f"RAG, 3 sentences {average:.0f} tokens per question")
print(f"ratio {everything / average:.1f}")
```

```text
all articles 979 tokens per question
RAG, 3 sentences 50 tokens per question
ratio 19.7
```

Sending all the articles costs 979 tokens per question; the 3 sentences chosen
with RAG average 50 tokens, about 20 times fewer. Even this small shop's 14
short articles come close to a thousand tokens per question; a company's
thousands of pages fit in no context window. RAG's price is the misses and
wrong retrievals we saw in 10 and 11; that is why both the search and the
answer are measured separately.

## Next

The next module, **Prompt Engineering and LLM Applications**, focuses on
talking to the model itself: clear instructions, prompts with examples, making
it reason step by step, structured output, tool calling, the agent loop,
conversation memory, defending against prompt injection and improving prompts
by measuring. The pieces you built here (the client, token counting, RAG,
verification, evaluation) will be used there too.
