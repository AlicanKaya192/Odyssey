| Term | Meaning |
|---|---|
| **Development set** | The messages measured while deciding on changes; their errors are read |
| **Test set** | Messages kept aside without looking; measured once, at the end |
| **Baseline** | The measure of the first version; every later change is judged against it |
| **Error analysis** | Reading the errors one by one and counting them by kind |
| **Overfitting** (memorisation) | The prompt fitting details of the development set and not showing the same success on new messages |
| **Ablation** | Finding a part's contribution by taking it out and measuring again |
| **Toy model** | The simple program used in this section to show the method, deciding by the word lists in the prompt; not a real language model |

**Keep in mind:**

- With the toy model `v1` scored 0.60 on development and test; `v2` (words
  from the meaning) 0.90 and 0.75; `v3` (words copied from development
  messages) 1.00 and 0.75.
- `v3` gained nothing on the test set but made the prompt grow from 100 to
  139 tokens.
- All eight of `v1`'s errors were `unknown`: the definitions were too
  narrow.
- In the ablation, taking out `back` raised the success; taking out `send`
  and `back` together left the total the same but changed the answers of
  two messages.
