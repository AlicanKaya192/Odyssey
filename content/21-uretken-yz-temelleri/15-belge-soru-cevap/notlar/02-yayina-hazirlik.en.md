Before putting a document Q&A system live:

**Data and search**

- [ ] Are the documents current, and who is responsible for them?
- [ ] Is the evaluation set made of real user questions? Does it include
      questions with no answer too?
- [ ] Was the search measured (recall@k, MRR)? Were the missed questions read?

**The answer**

- [ ] Are the system message's rules clear (only from the sources, the source
      number, the "not found" sentence written out exactly)?
- [ ] Are the answers verified (source number, numbers, names)?
- [ ] Does an answer that cannot be verified stay away from the user?

**Safety and cost**

- [ ] Is personal data masked before it goes to the search, the model and the
      log?
- [ ] Are the tokens and cost per question recorded? Multiplied by the scale?
- [ ] Are users told that they are talking to a model and that it can be wrong?
- [ ] In the "not found" case, is the person passed to a human?

**After a change**

- [ ] Was it measured again on the same evaluation set?
- [ ] For small differences, was the resampling interval checked?

**Common mistakes:**

- **Looking only at the correct count:** in the section the two systems were
  equal at 15; the difference was in the wrong answers.
- **Skipping verification:** the example reader never wrote a wrong number, but
  a recorded wrong reply tested it; a real model can write one.
- **Personal data in the log:** masking must happen before logging.
