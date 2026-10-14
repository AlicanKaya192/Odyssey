| Term | Meaning |
|---|---|
| **Zero-shot prompt** | A prompt that only gives an instruction |
| **Few-shot prompt** | A prompt that adds a few solved examples to the instruction |
| **Shot** | An input and its correct answer |
| **Example pool** | The labelled messages the prompt's examples are picked from |
| **Test set** | Messages kept for trying the prompt, never used as examples |
| **Balanced choice** | Taking the same number of examples from each category and shuffling them |
| **Choice by similarity** | Picking, for each new input, the examples most like it |
| **Leakage** | A test message getting into the prompt as an example; it makes success look better |

**Keep in mind:**

- Examples are sent again in every call: in the lesson ten examples took
  5.1 times the tokens of the zero-shot prompt.
- Five random examples missed at least one category in 932
  of a thousand draws.
- With TF-IDF the nearest example had the same category for
  6 of ten test messages; word overlap is a weak measure of
  similarity.
- Example answers are written exactly in the wanted form; the model
  learns the form from the examples.
