No single number says whether a generative model is good. Throughout this
path we will ask the same four questions:

| Question | How to check | In this section |
|---|---|---|
| **Does it resemble?** | Are the statistics of what is generated (mean, spread, relationships) close to reality? | Mean and standard deviation of 1000 fish |
| **Is it varied?** | Does the model keep producing the same few examples, or does it cover the whole data? | The samples spread almost exactly like the real ones |
| **Is it a copy?** | Are the samples identical to the training data? | Nearest neighbour distance |
| **Is it useful?** | Success on the actual task (answering questions, summarising, classifying) | Accuracy of the generative classifier |

**Common mistakes:**

- **Judging from a few nice samples.** It is easy to pick and show the best
  samples; look at the statistics of hundreds.
- **Looking only at resemblance.** A "model" that returns the training data
  verbatim scores perfectly on resemblance. Check for copies separately.
- **Mixing scales.** Adding centimetres and grams in one distance lets the
  grams dominate; bring the measurements to the same scale before measuring
  distance.
- **Not fixing the seed.** Comparing two models with different random
  samples hides whether the difference comes from the model or from luck.
