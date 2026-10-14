| Term | Meaning |
|---|---|
| **LoRA** (low-rank adaptation) | Adding the product of two thin matrices beside a frozen weight and training only them |
| **Rank** | The number of independent directions of a matrix |
| **Singular values** | The sizes of a matrix's directions; their squares give the "energy" share |
| **Adapter** | Small extra parameters trained for one task (A, B, an output layer if needed) |
| **Freezing** | Not updating a weight during training |
| **Merging** | Turning W + AB into a single matrix and removing the extra compute cost |
| **r** | LoRA's rank; the parameter count is r × (d_in + d_out) |

**Keep in mind:**

- B starts at zero: training starts from exactly the pre-trained model.
- In the section the first 8 directions carried 99.6% of full fine-tuning's
  change; an r = 4 LoRA gave 94% with 714 parameters, full fine-tuning 93% with
  2410 (the same level with three seeds).
- The pre-trained model does not change; the adapter is attached and detached.
