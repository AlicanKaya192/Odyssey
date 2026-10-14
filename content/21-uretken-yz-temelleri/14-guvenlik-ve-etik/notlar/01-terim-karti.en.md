| Term | Meaning |
|---|---|
| **Bias** | A model systematically disadvantaging a group |
| **Protected attribute** | Information decisions should not discriminate on (group, sex, origin…) |
| **Proxy variable** | A feature that indirectly carries the protected attribute |
| **Selection rate** | The share of a group that gets a positive decision |
| **Equal opportunity** | Truly suitable people being selected at an equal rate across groups |
| **Personal data** | Information that identifies a person: email, phone, address… |
| **Masking** | Replacing personal data with a label (`[EMAIL]`) |
| **Human in the loop** | The last word in a decision affecting a person being a human's |

**Keep in mind:**

- In the section the model trained on a biased history selected suitable
  candidates at 67% in A and 24% in B; removing the group column was not enough
  because of a proxy.
- A per-group threshold equalised opportunity (52% and 53%) but it is a policy
  decision.
- Masking with regular expressions is cheap but misses unusual spellings.
