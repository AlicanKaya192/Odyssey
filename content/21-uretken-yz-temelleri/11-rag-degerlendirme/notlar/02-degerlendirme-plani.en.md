An evaluation plan for a RAG system:

1. **Build the set.** Choose at least a few hundred real user questions; write
   the right document and the right answer for each. Add questions whose answer
   is not in the documents too.
2. **Measure retrieval.** recall@k and MRR. If the right chunk is not in the
   first k, the model cannot answer whatever it does.
3. **Measure the answer.** Correct, wrong, missed. For free-text answers
   phrase matching may not be enough; use rule-based checks, human and
   model-based evaluation together.
4. **Measure abstention.** Precision and recall together.
5. **Place the error.** Separate every error into retrieval or reading; fix the
   larger share first.
6. **Test the difference.** When comparing two settings, look at the interval
   with resampling; if the interval includes zero, the difference is not
   reliable.
7. **Keep records.** Write every measurement with its settings (chunking, k,
   threshold, prompt); after a change measure again on the same set.

**Common mistakes:**

- **A single accuracy number:** it does not show where the error is.
- **Changing the set while looking at the settings:** the numbers improve, but
  not for real users.
- **Only answerable questions:** the system's ability to say "I don't know" is
  not measured.
- **Trusting small differences:** on 24 questions one question is worth 4
  points.
