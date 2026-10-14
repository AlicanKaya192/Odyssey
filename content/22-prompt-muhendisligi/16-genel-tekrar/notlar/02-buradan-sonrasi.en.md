**Moving to a real model:**

- All the code in this module also works with a real chat API; the
  service's client takes the place of `ChatClient`. The message list, the
  finish reason, the token usage and the error types are similar in every
  service, but their names and details differ; read the service's
  documentation.
- Count tokens with that model's own tokenizer; the counter in this module
  is simplified.
- The form of tool calling changes from service to service; validation,
  confirmation and the grounding check stay in your program.
- Prices and limits change; track the spending from your own log.

**Where to go from here in Odyssey?**

- **Generative AI Fundamentals:** RAG, measuring hallucination, fine-tuning
  and LoRA; to ground the support assistant's answers in documents.
- **NLP Fundamentals** and **Embeddings and Language Models:** text
  classification, embeddings and attention; to measure a real classifier
  instead of the toy model.
- **Writing REST APIs with FastAPI:** turning the assistant into an endpoint;
  validation, error handling and tests.
- **Docker:** packaging the assistant and its API.

**Practical advice:**

1. Build an evaluation set of 50–100 messages from your own work; add
   attack messages and innocent messages that look like them too.
2. Set part of the set aside as a test and look at it only at the end.
3. Keep the first version simple; measure every change and write it in the
   log.
4. Give the assistant only the tools it needs; hand every case that cannot
   be trusted over to a person.
5. Tell the user they are talking to an AI assistant.
