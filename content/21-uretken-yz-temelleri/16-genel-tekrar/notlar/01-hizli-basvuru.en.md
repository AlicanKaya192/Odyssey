| Topic | Main idea | Formula / measure |
|---|---|---|
| Sampling | Ruler, inverse transform, rejection | Cumulative probability |
| Autoencoder | Rebuilding from a narrow code | Reconstruction error |
| VAE | The code is a distribution pulled to the standard normal | Loss = reconstruction + β·KL; $z = \mu + \sigma\varepsilon$ |
| GAN | The game of generator and discriminator | $-\log D(x) - \log(1 - D(G(z)))$; at equilibrium $D = 0.5$ |
| Diffusion | Learn to take the noise back | $x_t = \sqrt{\bar\alpha_t}\, x_0 + \sqrt{1 - \bar\alpha_t}\, \varepsilon$ |
| LLM generation | Template, next token, finish reason | `stop` / `length` |
| Tokens and cost | The history is sent in every call | input × price + output × price |
| Hallucination | Fluent but without basis | Self-consistency, source check |
| Chunking and search | Find the relevant chunk | key@k, cosine |
| RAG | Put the sources in the prompt, cite them | correct / wrong / missed / abstain |
| RAG evaluation | Retrieval and answer separately | recall@k, MRR, resampling |
| Fine-tuning and alignment | Forgetting, reward model | $\sigma(r(a) - r(b))$ |
| LoRA | A low-rank correction | $\Delta W = AB$, parameters $r(d_{in} + d_{out})$ |
| Safety | Bias, proxies, masking | Selection rate, equal opportunity |
| Capstone | Mask → search → verify → log → measure | A measure per component |

**The sections' measured results:**

- The VAE produced all 10 digits, the autoencoder 4 (03).
- At learning rate 0.01 the GAN gave 8, 6, 6 clusters; diffusion 8, 8, 8 (04, 05).
- Over eight messages the total input was 4.5 times the last call (07).
- 7 of 9 RAG errors were in retrieval (11).
- LoRA r = 4: 94% with 714 parameters; full fine-tuning 93% with 2410 (13).
- All articles 979 tokens, RAG 50 tokens (16).
