Terms that come up often in NLP; we use them throughout the path.

| Term | Meaning |
|---|---|
| document | A single text: one review, one ticket, one email |
| corpus | All the documents: the whole set of 2000 reviews |
| token | The unit text is split into; usually a word or a punctuation mark |
| tokenisation | The job of splitting text into tokens |
| vocabulary | The list of distinct tokens in the corpus |
| label | The correct answer of a document: `positive`, `billing` and so on |
| stop word | A word found in every text that carries no meaning on its own: "the", "and" |
| baseline | The prediction that always says the most frequent class; every model must beat it |
| accuracy | The share of correct predictions among all predictions |
| imbalanced data | The classes have very different counts: 1318 positive, 289 neutral |

## Rules or learning?

| | Rule-based | Learning |
|---|---|---|
| Who writes it? | An expert, by hand | A model, from labelled examples |
| Easy to understand? | Yes, every rule can be read | Partly; you need to look at the weights |
| Needs data? | No | Yes, labelled data |
| Copes with a new phrase | Not until a rule is added | Yes, if similar examples exist |
| Good at | Information with a fixed format: order numbers, emails, dates | Meaning and tone: sentiment, topic |

They are not rivals. For information with an exact format, such as an order
number, a regular expression is the right tool (section 14). For subtle jobs
such as the tone of a review, a learning model is needed.

## Remember

- Look at the data before working with text: how many documents, how the
  labels are distributed, how long the documents are, which words are most
  common.
- Report accuracy together with the baseline. "80% accuracy" on its own says
  nothing; if 85% of the examples share one class, it is a bad result.
