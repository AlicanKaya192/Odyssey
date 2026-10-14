There are two ways to "teach" a model something new, and they are often
confused:

| | RAG | Fine-tuning |
|---|---|---|
| What does it change? | The text the model sees in that call | The model's weights |
| Good for? | Knowledge: documents, rules, current data | Behaviour: format, tone, task, short answers |
| Updating | Changing the document is enough | Retraining is needed |
| Citing sources | Easy | Hard; the knowledge spreads into the weights |
| Risks | Wrong retrieval, long prompts | Forgetting, reward hacking, training cost |

**As a rule:** if the model does not know a fact, RAG first; if the model knows
it but does not use it in the wanted format or tone, fine-tuning. Most real
systems use both: fine-tuning for the behaviour "answer from the sources, say
so if you cannot find it", RAG for the knowledge itself.

**Questions before fine-tuning:**

1. Does a good prompt or RAG give the same result? Try the cheaper way first.
2. How many good-quality examples do I have? Little, noisy data breaks the
   model.
3. How will I keep the earlier skills? Mix in general-purpose examples.
4. How will I measure success? With a labelled evaluation set independent of
   the reward model.

**Common mistakes:**

- **Trying to teach knowledge with fine-tuning:** when the documents change, the
  model keeps saying the old facts.
- **Training on new data alone:** in the section the old task fell to 6.5%.
- **Taking the reward for success:** the biased reward chose long answers and
  correctness stayed low.
