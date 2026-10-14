**When LoRA?**

- When the model is large and updating all its weights is expensive.
- When the same model needs a separate adaptation for many tasks (only an
  adapter is stored per task).
- When a reversible change is wanted that does not break the pre-trained
  model's behaviour.

**Choices:**

| Choice | Effect |
|---|---|
| r (rank) | A small r means few parameters; too small is not enough. In the section r = 1 gave 87%, r = 4 94% |
| Which layers | Usually the weights of the attention and feed-forward layers; the more layers, the more parameters |
| Learning rate | Because the adapter is small, a different rate from full fine-tuning may be needed |
| Initialisation | B = 0: training starts from the pre-trained model |

**Step by step:**

1. Try only the last layer or a prompt first; if that is not enough, LoRA.
2. Start with a small r (4–8) and measure on the evaluation set.
3. Stop if raising r does not raise accuracy.
4. Measure the old tasks too: LoRA does not change the pre-trained model, but
   the merged model can do worse on an old task.

**Common mistakes:**

- **Initialising B at random:** at the start of training the model moves away
  from the pre-trained model.
- **Computing the gradients after the update:** `g_A` and `g_B` must be computed
  with the same `A` and `B`.
- **Deciding on a single seed:** in the section the differences were below one
  point and changed direction.
