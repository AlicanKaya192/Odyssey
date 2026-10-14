**The next module:** Prompt Engineering and LLM Applications. The client,
token counting, RAG, verification and evaluation you built in this module will
be used there too; the focus is talking to the model itself: clear
instructions, prompts with examples, structured output, tool calling, the
agent loop, memory and defending against prompt injection.

**Moving to real tools:**

- The models in this module were built with NumPy, on small data and on a
  single computer, to show the ideas. Real image and language models are
  trained with deep learning libraries, very large data and powerful hardware.
- When you move to a real chat API, this module's patterns hold as they are:
  the message list, the finish reason, token counting (with that model's own
  tokenizer), the cost log, verification.
- In vector search an embedding model is used instead of TF-IDF, and a vector
  database for large corpora; the way of measuring (key@k, recall@k, MRR) stays
  the same.
- There are ready libraries for fine-tuning and LoRA; but measuring forgetting
  and reward hacking is still your job.

**Practical advice:**

1. Build an evaluation set of 30–50 questions from your own documents; add
   questions whose answers are not in the documents too.
2. Measure the search first, then the answer.
3. When you make a change, measure again on the same set; look at small
   differences with resampling.
4. Mask personal data, tell users they are talking to a model, and leave the
   last word to a person in decisions that affect people.
