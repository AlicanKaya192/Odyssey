# Preparing Data for a Model

The files so far have been clean: every column a number, not a value
missing. Real data is not like that.

This section has three problems and one rule. The rule matters more than all
three.

## The rule: split first, then touch

Every step of preparation **learns** something from the data: a mean, a
standard deviation, a list of categories. If that information is drawn from
all the data, the test rows the model must not see enter the arithmetic.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>The wrong order</h4>
      <p>Prepare all the data → then split.<br>Test information <b>leaks</b> into training.</p>
    </div>
    <div class="versus-side">
      <h4>The right order</h4>
      <p>Split → <b>learn the preparation on training</b> → apply to both.<br>The test set stays untouched.</p>
    </div>
  </div>
  <figcaption>This is called data leakage. The test score comes out higher than it should and the model is not really that good.</figcaption>
</figure>

Every operation in this section follows that rule. Preparation done without
knowing it corrupts the measurement silently.

## Problem 1: missing values

```
ValueError: Input contains NaN
```

sklearn does not work with missing values (apart from a few tree-based
models). There are two options: **fill** them or **drop** them.

```python
print(df.isna().sum())
# age        0
# km         0
# engine    14
# fuel       0
# ...
```

14 of the 120 rows have no engine size.

**Dropping** is the easiest but expensive: dropping 14 of 120 rows means
losing an eighth of the data. With little data you cannot afford it.

**Filling** is more common. The mean or median for numeric columns, the most
frequent value for categorical ones.

```python
fill_value = X_train["engine"].mean()      # from TRAINING only
X_train = X_train.fillna({"engine": fill_value})
X_test = X_test.fillna({"engine": fill_value})
```

**Note:** the mean is computed from the **training** data and **the same
number** is applied to both. Computing it over all the data would be
leakage.

In this example the two means barely differ — **1.458** and **1.457**. The
rule is not about the size of the difference but about whether the
measurement is honest. A difference of 0.001 today can be 0.3 on other data.

**Mean or median:** the median, if there are outliers. A mean is pulled by a
single extreme record; a median is not.

## Problem 2: text columns

```
ValueError: could not convert string to float: 'diesel'
```

A model works with numbers. The `fuel` column holds `petrol`, `diesel` and
`lpg` — those cannot enter a model as they are.

**The first idea that comes to mind is wrong:** saying `petrol=0, diesel=1,
lpg=2`. To the model that makes `lpg` twice `petrol` and `diesel` exactly
halfway between. No such ordering exists.

The right way is **one-hot encoding**: every category gets its own column.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">before</span><span class="anat-body">one column: <code>fuel</code> = petrol / diesel / lpg</span></div>
    <div class="anat-row"><span class="anat-label">after</span><span class="anat-body">three columns: <code>fuel_petrol</code>, <code>fuel_diesel</code>, <code>fuel_lpg</code> — exactly one is 1 in each row</span></div>
  </div>
  <figcaption>The way to avoid inventing an order where none exists: give each category a column of its own.</figcaption>
</figure>

```python
encoded = pd.get_dummies(df, columns=["fuel", "gearbox"])
```

Five columns become eight: `age`, `km`, `engine`, `fuel_petrol`,
`fuel_diesel`, `fuel_lpg`, `gearbox_manual`, `gearbox_auto`.

**The result:** adding those two columns to the model brings the error down
**from 32.58 to 16.42**. Fuel type and gearbox really do drive the price;
they had been left out only because they were not numbers.

**When inventing an order is right:** when the category really has one.
`low < medium < high` or `primary < secondary < university` take `0, 1, 2`
correctly — that is called **ordinal** encoding. With no order, one-hot.

**A trap:** columns with many categories (a city, a product code) produce
hundreds of columns under one-hot. With little data that pushes the number
of features towards the number of samples and the model starts memorising.

**A pandas 3 detail:** older tutorials find text columns with
`df.dtypes == "object"`. In pandas 3 text columns are no longer `object`;
that check returns an **empty list**. The way that works:

```python
text_columns = df.select_dtypes(exclude="number").columns.tolist()
```

## Problem 3: differences in scale

The `km` column runs from 10,000 to 300,000 while `engine` runs from 1.0 to
2.0. Both are numbers, but they do not live in the same world.

For a model that works on distance this is fatal:

```
KNN, unscaled   MAE 171.49
KNN, scaled     MAE  51.48
```

**A factor of three.** Unscaled, KNN is really only looking at `km`; the
difference between 1.0 and 2.0 in `engine` counts for nothing next to a
250,000 gap in `km`.

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)                       # learn from TRAINING only
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**`fit` on training, `transform` on both.** Those three lines are the
section's rule written as code. Calling `fit_transform` on the test set is a
common mistake and is exactly what leakage means.

### Which models want scaling

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Affected</h4>
      <p>KNN, linear models (when regularised), clustering, neural networks<br><b>Anything using distance or the size of a weight</b></p>
    </div>
    <div class="versus-side">
      <h4>Not affected</h4>
      <p>Decision trees, random forests, gradient boosting<br><b>Anything working with thresholds</b></p>
    </div>
  </div>
  <figcaption>A tree asks "is km above 150,000"; the column's scale does not change that question.</figcaption>
</figure>

On the same data, linear regression is **entirely unaffected** by scaling:

```
linear regression, unscaled   MAE 34.63
linear regression, scaled     MAE 34.63
```

Identical. The model adjusts its coefficient to the column's scale.

**Scaling still has a use here:** on scaled data the coefficients become
comparable. In section 1 we said "you cannot claim age matters more because
3.35 > 2.77" — after scaling, you can.

**Two scalers:**

| Scaler | What it does | When |
|---|---|---|
| `StandardScaler` | Sets the mean to 0 and the standard deviation to 1 | The default choice |
| `MinMaxScaler` | Squeezes everything into 0-1 | When a bounded range is needed |

## Leakage does not have to be small

In this section's examples leakage barely moves the number: scaling on all
the data takes MAE from 51.48 to 51.69, next to nothing.

That does not mean the rule is loose. How large a leak is depends on **what
leaked**, and sometimes the result is pure fiction.

Consider this experiment: 80 rows, 300 columns and **every value random**.
Nothing has any relationship with the target. A correctly built model should
find nothing here.

```
leaky selection    R2   0.442
clean selection    R2  -0.273
```

**The clean result is negative** — which is right, because there is nothing
to learn.

**The leaky result is 0.442** — that is, it looks like there is a model. The
only thing done differently was choosing the columns **by looking at all the
data**: among 300 random columns, the five that happen to agree with the
test data get picked, and then the measurement is taken on that same test
data.

That number can be written on a slide and nobody will notice. The model is
worth nothing.

## The order

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1</b><br>read</span>
    <span class="arrow">→</span>
    <span class="node acc"><b>2</b><br>SPLIT</span>
    <span class="arrow">→</span>
    <span class="node"><b>3</b><br>fill gaps</span>
    <span class="arrow">→</span>
    <span class="node"><b>4</b><br>encode categories</span>
    <span class="arrow">→</span>
    <span class="node"><b>5</b><br>scale</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>6</b><br>train and measure</span>
  </div>
  <figcaption>The second box sits right at the front. Every step after it is learned on training and applied to both.</figcaption>
</figure>

This order is awkward to work with: applying the same operation to two sets
separately, keeping the fill value, carrying the scaler around. It scatters
the code and makes forgetting a step easy.

**There is a solution: `Pipeline`.** It gathers every preparation step
together with the model into a single object and makes leakage structurally
impossible. That is section 11.

For now the steps are done by hand — because using `Pipeline` without
knowing what it automates means never seeing the leak it prevents.
