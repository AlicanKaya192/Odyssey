# What Is Machine Learning?

In every program you have written so far, **you wrote the rules.** You said
"a score above 50 passes", and the program applied it.

Machine learning turns that around: you do not write the rule, you
**derive it from data.**

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Classical programming</h4>
      <p>You write the rule, you supply the data, an answer comes out.</p>
    </div>
    <div class="versus-side">
      <h4>Machine learning</h4>
      <p>You supply the data <b>and the answers</b>, a rule comes out.</p>
    </div>
  </div>
  <figcaption>The difference is not in the input but in what is unknown. In classical programming the answer is unknown; in machine learning the rule is.</figcaption>
</figure>

## When do you need it?

Try writing the rule that decides whether an email is spam: you say "if it
contains 'you have won'", and the next day one arrives saying "you hav won".
You write hundreds of rules and every one of them is incomplete.

But if you have ten thousand emails already known to be spam or not, you can
derive the rule **from those**.

The test is this: **if you can write the rule as a sentence, you do not need
machine learning.** Nobody builds a model to calculate VAT; the formula is
known. Models are for jobs that have no formula but plenty of examples.

## The vocabulary

The field has its own words, and every one of them is a new name for
something familiar:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">sample</span><span class="anat-body">a <b>row</b> in the table — one house, one patient, one email</span></div>
    <div class="anat-row"><span class="anat-label">feature</span><span class="anat-body">a <b>column</b> used to predict — floor area, age, word count</span></div>
    <div class="anat-row"><span class="anat-label">target</span><span class="anat-body">the column you want to predict — price, ill or not</span></div>
    <div class="anat-row"><span class="anat-label">model</span><span class="anat-body">the rule from features to target, derived from data</span></div>
    <div class="anat-row"><span class="anat-label">fit</span><span class="anat-body">the act of deriving that rule from data</span></div>
    <div class="anat-row"><span class="anat-label">predict</span><span class="anat-body">applying the rule to a new row</span></div>
  </div>
</figure>

By convention the features are written `X` and the target `y`. The capital
letter is not accidental: `X` is a **table** (many columns), `y` a single
**column**.

## Three kinds of learning

**Supervised learning.** You have the right answers. You know the floor area
of a thousand houses **and what they sold for**; the model learns the
relationship. This section and the eight after it are about that.

**Unsupervised learning.** There are no right answers. You have customers,
but there is no such thing as "the correct group"; the model clusters
similar ones on its own. That is section 10.

**Reinforcement learning.** The model learns by trying and being rewarded —
systems that play games or walk robots. Outside this path.

## Two kinds of problem

In supervised learning, **what the target is** decides the method:

| Target | Problem | Example |
|---|---|---|
| A number | **Regression** | House price, tomorrow's sales, temperature |
| A category | **Classification** | Spam or not, which species, pass or fail |

The distinction matters because the **measure of success** changes with it:
regression asks "by how much were you off", classification asks "how many
did you get right". Confusing the two is the most common beginner mistake.

Sometimes the line is blurred: "how many stars will they give" can be a
five-category classification or a regression between 1 and 5. That is your
decision, and you write down your reason.

## The central idea: test on data it has not seen

A model can memorise the data it was trained on. A model that memorises a
thousand houses is perfect on those thousand and useless on a new one.

So the data is **split in two**:

<figure class="fig">
  <div class="flow">
    <span class="node"><b>All the data</b></span>
    <span class="arrow">→</span>
    <span class="node acc"><b>Training</b><br>the model sees this</span>
    <span class="arrow">+</span>
    <span class="node ok"><b>Test</b><br>the model never sees this</span>
  </div>
  <figcaption>The test set is like an exam: hand out the questions in advance and the mark measures memory, not knowledge.</figcaption>
</figure>

```python
records = [("Ada", 62), ("Kerem", 78), ("Mina", 91), ("Deniz", 45)]

split = int(len(records) * 0.75)
train, test = records[:split], records[split:]

print(len(train), len(test))
```

```text
3 1
```

In practice you do not do this by hand (`train_test_split` exists, and it is
in the next section), but you need to know what it does when you use it.

**The rule:** a model's success is measured **only** on the test data.
Success on the training data is the mark of a student who sat the exam with
the answer key.

## Without a baseline, a number says nothing

Is a model that is "80% correct" good? That depends on how correct you would
be without a model at all.

Say 80 of a hundred emails are ordinary and 20 are spam. A one-line program
that says "all ordinary" and learns nothing is also **80% correct**.

So every job starts with a **baseline**:

| Problem | Baseline |
|---|---|
| Regression | Predict the **mean** of the training data for everything |
| Classification | Predict the **most frequent** class for everything |

If your model cannot beat the baseline, there is no model. Those two lines
can show on day one that a project worked on for months has gone nowhere.

## What learning actually means

The word "learning" sounds more mysterious than it is. For most models the
work is this: **searching for the numbers that make the error smallest.**

If you wanted to derive "what score and above passes" from a list of marks,
you would try thresholds from 30 to 100 and keep the one that got the most
right. That is what linear regression does too — except the numbers it
searches for are a slope and an intercept rather than a threshold.

A model is not magic; it is **a parameter that was searched for**.

## What it cannot do

- **It cannot know what is not in the data.** If what drives house prices is
  location and there is no location column, the model cannot invent it.
- **It does not tell you causes.** The rule from the previous module holds
  here too: a model finds things that move together, not why.
- **It repeats the past.** If past decisions were biased, the model learns
  the bias and carries it forward.
- **It cannot be better than its data.** Dirty, incomplete, unbalanced data
  gives a bad model. That is what the whole previous module was for.

## The order

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1</b><br>question and data</span>
    <span class="arrow">→</span>
    <span class="node"><b>2</b><br>split</span>
    <span class="arrow">→</span>
    <span class="node"><b>3</b><br>baseline</span>
    <span class="arrow">→</span>
    <span class="node"><b>4</b><br>build a model</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>5</b><br>measure on the test set</span>
  </div>
  <figcaption>Step three is the one that gets skipped, and then nobody can tell whether step four was any good.</figcaption>
</figure>

## Summary

- In classical programming **you write the rule**; in machine learning **the
  rule comes out of the data**.
- If you can write the rule as a sentence, you do not need a model.
- **Features are `X`**, the **target is `y`**. A numeric target means
  regression, a categorical one classification.
- Three kinds of learning: supervised (answers exist), unsupervised (they do
  not), reinforcement (learning by trying).
- **Success is measured only on data the model has not seen.**
- **A success figure is unreadable without a baseline**: on unbalanced data,
  a program that learns nothing can also be 80% correct.
- Learning is usually **searching for the parameters that minimise the
  error**.
- A model cannot know what is not in the data, does not tell you causes, and
  repeats the past.
