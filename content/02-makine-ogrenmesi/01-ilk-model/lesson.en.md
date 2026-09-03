# Your First Model

In the previous section we talked about what a model is, why the data gets
split in two and what a baseline is for. You even trained a model by
searching for a threshold with a loop.

Now you will do the same job with a library. What changes is not the idea
but the number of lines you write: the search you did by hand in twenty
lines comes down to three.

## The three steps of sklearn

The machine learning library is called **scikit-learn** and appears in code
as `sklearn`. Every model inside it carries the same three steps.

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1 · build</b><br><code>LinearRegression()</code></span>
    <span class="arrow">→</span>
    <span class="node acc"><b>2 · learn</b><br><code>fit(X, y)</code></span>
    <span class="arrow">→</span>
    <span class="node ok"><b>3 · predict</b><br><code>predict(X_new)</code></span>
  </div>
  <figcaption>Linear regression, decision tree, KNN — all of them carry these three. Changing model usually means changing the first line.</figcaption>
</figure>

Say we have the floor area and price of eight houses:

```python
from sklearn.linear_model import LinearRegression

areas = [50, 60, 70, 80, 90, 100, 110, 120]
prices = [155, 178, 205, 228, 250, 278, 300, 325]

model = LinearRegression()
model.fit([[a] for a in areas], prices)

print(model.predict([[95]]))   # [264.16666667]
```

Three lines. For a 95 square metre house the model says **264**.

That number is not in the data — there is a 90 and a 100, but no 95. The
model derived the rule in between and applied it to an input it had never
seen. That is what we were after all along.

## What the model learned is two numbers

When `fit` finishes the model has learned something, and you can look at it:

```python
print(model.coef_[0])     # 2.4285714285714284
print(model.intercept_)   # 33.35714285714289
```

The rule it learned is this:

```
price = 2.43 x area + 33.36
```

**`coef_` is the slope and `intercept_` the intercept.** How much the price
rises when the area goes up by one unit is what `coef_` says: 2.43. The
"price" of a zero square metre house is `intercept_` — a meaningless number
on its own, but it fixes where the line sits.

In the previous section you searched for a threshold with a loop. `fit`
does exactly that: it searches for the slope and intercept that minimise
the error. The difference is that it computes them directly instead of
looping.

**The trailing underscore is a rule.** `coef_` and `intercept_` end in an
underscore. In sklearn that means "this value came into existence **after
training**". Look at them before calling `fit` and you get an error —
because they do not exist yet.

## `X` has to be two-dimensional

The `[[a] for a in areas]` above may have looked odd. Why not a plain list,
why is each number in a list of its own?

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">X</span><span class="anat-body">a <b>table</b>: each row a sample, each column a feature → two-dimensional</span></div>
    <div class="anat-row"><span class="anat-label">y</span><span class="anat-body">a single <b>column</b>: the right answer for each sample → one-dimensional</span></div>
  </div>
  <figcaption>X is a table even when you work with one feature. A one-column table is still a table.</figcaption>
</figure>

sklearn always expects a **table**, because the models are written to work
with many features. One feature means a table with one column.

On the pandas side the distinction is made by the number of brackets:

```python
X = df[["area"]]   # DataFrame - a table, 2D    correct
X = df["area"]     # Series    - a column, 1D   error
y = df["price"]    # a Series is correct for y
```

Write single brackets and call `fit`, and sklearn tells you:

```
ValueError: Expected 2D array, got 1D array instead
```

**Everybody sees this error.** Have the translation ready for when you do:
"you did not hand X over as a table."

## With real data: split, train, measure

An eight-row list had no test set. With a real file the whole flow comes
together:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("homes.csv")
X = df[["area"]]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
prediction = model.predict(X_test)

print(mean_absolute_error(y_test, prediction))   # 18.5
```

A few details:

- **`train_test_split` returns four things** in a fixed order:
  `X_train, X_test, y_train, y_test`. Getting the order wrong is a silent
  bug — the code runs and the result is nonsense.
- **`test_size=0.25`** keeps a quarter of the data for testing. Between 0.2
  and 0.3 is common; less makes the measurement unreliable, more weakens
  the training.
- **`random_state=42`** fixes the split. Without it every run gives a
  different result and you cannot tell improvement from luck. 42 is a
  convention, not a magic number.
- The split is **random**, not a cut from the top. If the file were sorted
  by area, taking the first 75% would train on small houses and test on
  large ones.

## A measurement says nothing on its own

What does `18.5` mean? Is it good or bad?

The previous section's answer earns its keep here: **look at the baseline.**

```python
baseline = y_train.mean()
baseline_mae = mean_absolute_error(y_test, [baseline] * len(y_test))

print(baseline_mae)   # 82.29
```

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Baseline</h4>
      <p>Says <b>312.87</b> for every house.<br>Mean error: <b>82.29</b></p>
    </div>
    <div class="versus-side">
      <h4>Model</h4>
      <p>Looks at the area and answers.<br>Mean error: <b>18.50</b></p>
    </div>
  </div>
  <figcaption>The error dropped by 77%. The answer to "is 18.5 good" comes from here, not from the number itself.</figcaption>
</figure>

The model beat the baseline; it has learned something. Had it not, three
lines of code would be predicting worse than the mean and would have to go.

**Do not break the order:** the baseline is built **before** the model.
Built afterwards, you have already seen the model's number, and it becomes
easy to talk yourself into "well, that is about as good as it gets".

## A second feature

Our file also has an `age` column — the age of the house. Let us add it:

```python
X = df[["area", "age"]]
```

The rest of the code is **the same**. The only change is that `X` now has
two columns.

```
one feature   MAE 18.50
two features  MAE  7.13
```

The error dropped by more than half. The model has now learned two
coefficients:

```python
print(model.coef_)   # [ 2.77 -3.35]
```

**The sign of a coefficient says something:** as area goes up the price
goes up (+2.77); as age goes up the price goes down (-3.35). The numbers
came out of the data; nobody told the model that older houses are cheaper.

But two warnings:

- **A coefficient does not state a cause.** Not "age lowers the price" but
  "houses that are older come out cheaper" is the correct sentence. The
  rule from the previous module holds here too.
- **Coefficients cannot be compared with each other.** You cannot say "age
  matters more" because 3.35 > 2.77: area ranges from 45 to 165 while age
  runs from 0 to 30. A coefficient depends on its column's **unit**.
  Comparing them requires scaling first — that is section 4.

## One more number: `score`

Every sklearn model has `score`. For regression it returns **R²**:

```python
print(model.score(X_test, y_test))   # 0.943
```

R² roughly means "how much of the variation in the target you managed to
explain". Close to 1 is good, 0 is as good as the baseline, negative is
**worse** than the baseline.

The practical difference from MAE: MAE speaks in the target's unit ("I am
off by 18.5 thousand on average") while R² is a unitless ratio. Reports
carry both — one is understandable, the other comparable.

## The whole flow in one place

<figure class="fig">
  <div class="flow">
    <span class="node"><b>read</b><br><code>read_csv</code></span>
    <span class="arrow">→</span>
    <span class="node"><b>split</b><br><code>train_test_split</code></span>
    <span class="arrow">→</span>
    <span class="node"><b>baseline</b><br><code>y_train.mean()</code></span>
    <span class="arrow">→</span>
    <span class="node acc"><b>train</b><br><code>fit</code></span>
    <span class="arrow">→</span>
    <span class="node ok"><b>measure</b><br><code>mean_absolute_error</code></span>
  </div>
  <figcaption>This order stays the same for every section that follows. The only thing that changes is the model inside the fourth box.</figcaption>
</figure>

If you wanted a decision tree instead of linear regression, this is the
only line that changes:

```python
from sklearn.tree import DecisionTreeRegressor
model = DecisionTreeRegressor()
```

Everything else — splitting, training, measuring — stays as it is. That is
why learning sklearn's three steps once is enough.

## What we skipped in this section

To be honest, we passed over a few things:

- **Linear regression does not suit every dataset.** If price does not rise
  along a straight line with area, this model falls short. Sections 7 and 8
  have models that capture curved relationships.
- **Missing values and text columns cannot enter a model.** Our file was
  clean; real data is not. That is section 4.
- **The result of a single split is partly luck.** Write 7 instead of
  `random_state=42` and the MAE changes. For a more reliable measurement
  there is cross validation — section 5.

For now you have a working flow, and that flow beats the baseline.
Everything else is built on top of it.
