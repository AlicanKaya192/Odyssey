Questions to ask when choosing the chunking:

| Question | Small chunk | Large chunk |
|---|---|---|
| Over how many sentences does a fact spread? | Good for one-sentence facts | Good for explanations of several sentences |
| How large is the token budget? | Cheap | Expensive |
| How long are the documents? | Needed for long documents | For short documents the whole article is enough |
| How precise is the search? | Little noise | The chunk also holds unrelated text |

**Step by step:**

1. Build a small evaluation set from real user questions: the question, the
   right document and a phrase that must appear in a correct answer.
2. Try a few chunkings (sentences, 2–3 window sizes, with and without overlap,
   with and without titles).
3. For each, measure key@k and the average tokens; judge the two together.
4. Read the missed questions one by one: was the fact split, or was the
   question asked in other words?
5. If facts are split, enlarge the overlap or the window; if words do not
   match, try embedding or hybrid search.

**Common mistakes:**

- **A small window without overlap:** in the section 12-word windows stopped
  at 0.42; facts split at a border were lost.
- **Measuring only the right document:** a chunk of the right article that does
  not contain the answer may have been found; the measure should be the answer
  phrase.
- **Ignoring tokens:** the whole article was the most precise but four times as
  expensive.
- **Deciding on a single question:** a setting can be good for one question and
  bad for the others.
