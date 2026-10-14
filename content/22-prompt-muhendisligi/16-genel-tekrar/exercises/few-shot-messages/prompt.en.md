`few_shot_messages(system, examples, question)` should build a message
list: first `system` in the `system` role; then for every `[text, label]`
example the text in the `user` role and the label in the `assistant` role;
at the end `question` in the `user` role.

**Expected output:**

```
system | Classify.
user | Where is my parcel?
assistant | shipping
user | My card was declined.
assistant | payment
user | Refund?
```
