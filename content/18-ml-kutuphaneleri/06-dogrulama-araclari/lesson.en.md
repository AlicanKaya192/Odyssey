# Validation Tools

When you write `cross_val_score(model, X, y, cv=5)` the data is split into
five parts. But **how** it is split changes the score: the classes may spread
unevenly over the folds, rows of the same patient may land in both training
and test, the time order may be broken. scikit-learn provides a separate
splitter for each case. This section covers the splitters, `cross_validate`,
which gives several measures at once, and two curve functions
(`learning_curve`, `validation_curve`).

## KFold and StratifiedKFold

```python
import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold

y = np.array([0] * 90 + [1] * 10)   # 100 rows, 10 positive, sorted
X = np.zeros((100, 1))
for cv in [KFold(5), StratifiedKFold(5)]:
    print([int(y[test].sum()) for _, test in cv.split(X, y)])
```

```text
[0, 0, 0, 0, 10]
[2, 2, 2, 2, 2]
```

- A splitter's `split(X, y)` method gives the `(train, test)` row indices for
  each fold. We counted the positives in each test fold.
- `KFold(5)` splits the rows into five in order. Since the data is sorted,
  the first four test folds have **no** positives and the last has all of
  them. "Finding the positives" cannot be measured in such a fold.
- `StratifiedKFold` keeps the class ratio in every fold: 2 positives each.
- When a **number** like `cv=5` is given, a classifier gets
  `StratifiedKFold(5)`. For regression (a numeric target) `KFold(5)` is used,
  and it **does not shuffle**.

## Not shuffling sorted data

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import KFold, cross_val_score
from sklearn.tree import DecisionTreeRegressor

X, y = make_regression(n_samples=200, n_features=3, noise=10, random_state=4)
order = np.argsort(y)               # suppose the file is sorted by target
X, y = X[order], y[order]
for cv in [5, KFold(5, shuffle=True, random_state=0)]:
    scores = cross_val_score(DecisionTreeRegressor(random_state=0), X, y, cv=cv)
    print(scores.round(2), round(scores.mean(), 3))
```

```text
[ -4.13 -13.08 -10.47  -9.43  -2.93] -8.009
[0.82 0.78 0.86 0.84 0.76] 0.811
```

- The data is sorted by target (like a file ordered by price). Since `cv=5`
  does not shuffle, each test fold is a price range never seen in training. A
  tree cannot predict outside the range it saw; R² fell **below zero**.
- `KFold(5, shuffle=True, random_state=0)` shuffles the rows first: mean R²
  0.811. Same model, only the split changed.
- If you do not know how the file is ordered, split with shuffling. The
  exception is time: there shuffling brings the future into training (below).

## Groups: the same person not on both sides

```python
import numpy as np
from sklearn.model_selection import GroupKFold, KFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

rng = np.random.default_rng(3)
centers = rng.normal(size=(40, 5))       # 40 patients
labels = rng.integers(0, 2, size=40)     # label per patient, random
groups = np.repeat(np.arange(40), 6)     # 6 measurements per patient
X = centers[groups] + rng.normal(scale=0.1, size=(240, 5))
y = labels[groups]
model = KNeighborsClassifier(n_neighbors=3)
plain = cross_val_score(model, X, y, cv=KFold(5, shuffle=True, random_state=0))
grouped = cross_val_score(model, X, y, cv=GroupKFold(5), groups=groups)
print(round(plain.mean(), 3), round(grouped.mean(), 3))
```

```text
1.0 0.588
```

- The label is random: **nothing** in the measurements shows the illness.
  But the 6 measurements of one patient are very alike.
- Plain `KFold` spreads one patient's measurements over training and test.
  The model finds the test measurement's "sibling" in training and copies its
  label: accuracy 1.0. What it measures is not the illness but recognising
  the patient.
- `GroupKFold` puts all rows of a patient into the same fold (with
  `groups=groups`). The model is tested on new patients: 0.588, close to
  chance, which is the truth.
- Same customer, same device, same session, same photographer: if the model
  will be applied to a **new** group tomorrow, validation is done by group as
  well. If the class ratio should also be kept, `StratifiedGroupKFold`.

## TimeSeriesSplit

```python
import numpy as np
from sklearn.model_selection import TimeSeriesSplit

X = np.arange(12).reshape(-1, 1)    # 12 months, in order
for train, test in TimeSeriesSplit(n_splits=4).split(X):
    print(train.min(), train.max(), test.tolist())
print("gap=1")
for train, test in TimeSeriesSplit(n_splits=3, test_size=2, gap=1).split(X):
    print(train.min(), train.max(), test.tolist())
```

```text
0 3 [4, 5]
0 5 [6, 7]
0 7 [8, 9]
0 9 [10, 11]
gap=1
0 4 [6, 7]
0 6 [8, 9]
0 8 [10, 11]
```

- In every fold the training is **always the past** and the test is the
  period right after. The training window grows each fold (0–3, 0–5, 0–7,
  0–9).
- `gap=1` leaves one period between training and test: train on 0–4 and test
  6–7. When the forecast will be used a month later, this is the honest one.
- Shuffling a time series (`shuffle=True`) teaches tomorrow's data to
  yesterday's model; the score comes out better than can really be reached.

## cross_validate: several measures, the training score

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=400, n_features=10, n_informative=4,
                           weights=[0.8], flip_y=0.05, random_state=6)
res = cross_validate(DecisionTreeClassifier(random_state=0), X, y, cv=5,
                     scoring=["accuracy", "f1"], return_train_score=True)
print(sorted(res))
for key in ["train_accuracy", "test_accuracy", "test_f1"]:
    print(key, round(res[key].mean(), 3))
```

```text
['fit_time', 'score_time', 'test_accuracy', 'test_f1', 'train_accuracy', 'train_f1']
train_accuracy 1.0
test_accuracy 0.82
test_f1 0.593
```

- `cross_val_score` gives an array for one measure; `cross_validate` gives a
  **dictionary**: `test_<name>` for each measure, `train_<name>` if asked, and
  `fit_time` / `score_time` (seconds).
- Training accuracy 1.0, test 0.82: the unlimited-depth tree memorised the
  training data. Seeing this gap needs `return_train_score=True`.
- The data is imbalanced (80% one class): accuracy 0.82 looks good while F1
  is 0.593. Seeing measures side by side keeps a single number from
  misleading.

## learning_curve: does more data help?

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import learning_curve

sizes, train, test = learning_curve(LogisticRegression(), X, y, cv=5,
                                    train_sizes=[0.1, 0.25, 0.5, 1.0])
print(sizes.tolist())
print(train.mean(axis=1).round(3).tolist())
print(test.mean(axis=1).round(3).tolist())
```

```text
[32, 80, 160, 320]
[0.894, 0.852, 0.855, 0.841]
[0.775, 0.825, 0.822, 0.83]
```

- `train_sizes` are fractions of the training fold: 10% of 320 training rows
  is 32 rows. At each size it trains the model 5 times and gives the training
  and test scores.
- At 32 rows training 0.894, test 0.775: with little data the model fits the
  training set but does not generalise. At 320 rows training 0.841, test
  0.83: the gap fell to 0.01 and the test score has barely moved since 80
  rows.
- If the curves have met and flattened, collecting more data will not gain
  this model much; a stronger model or better features are needed.

## validation_curve: the effect of one setting

```python
import matplotlib.pyplot as plt
from sklearn.model_selection import validation_curve
from sklearn.tree import DecisionTreeClassifier

depths = [1, 2, 3, 5, 8, 12]
train, test = validation_curve(DecisionTreeClassifier(random_state=0), X, y,
                               param_name="max_depth", param_range=depths, cv=5)
print(train.mean(axis=1).round(3).tolist())
print(test.mean(axis=1).round(3).tolist())
fig, ax = plt.subplots(figsize=(6, 3.2))
ax.plot(depths, train.mean(axis=1), marker="o", label="train")
ax.plot(depths, test.mean(axis=1), marker="o", label="test")
ax.set_xlabel("max_depth")
ax.set_ylabel("accuracy")
ax.legend()
```

```text
[0.841, 0.876, 0.882, 0.922, 0.967, 0.999]
[0.828, 0.857, 0.838, 0.83, 0.822, 0.822]
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="398.828125pt" height="222.808781pt" viewBox="0 0 398.828125 222.808781" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 222.808781 
L 398.828125 222.808781 
L 398.828125 0 
L 0 0 
L 0 222.808781 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 56.828125 184.608 
L 391.628125 184.608 
L 391.628125 7.2 
L 56.828125 7.2 
L 56.828125 184.608 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_1">
    <g id="xtick_1">
     <g id="line2d_1">
      <defs>
       <path id="m15aed4d867" d="M 0 0 
L 0 3.5 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m15aed4d867" x="99.715728" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="99.715728" y="199.205656" transform="rotate(-0 99.715728 199.205656)">2</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="155.054571" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="155.054571" y="199.205656" transform="rotate(-0 155.054571 199.205656)">4</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="210.393414" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="210.393414" y="199.205656" transform="rotate(-0 210.393414 199.205656)">6</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="265.732257" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="265.732257" y="199.205656" transform="rotate(-0 265.732257 199.205656)">8</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="321.0711" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="321.0711" y="199.205656" transform="rotate(-0 321.0711 199.205656)">10</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="376.409943" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="376.409943" y="199.205656" transform="rotate(-0 376.409943 199.205656)">12</text>
     </g>
    </g>
    <g id="text_7">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="224.228125" y="213.206438" transform="rotate(-0 224.228125 213.206438)">max_depth</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_7">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="174.25634" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="178.055169" transform="rotate(-0 49.828125 178.055169)">0.825</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="151.379745" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="155.178573" transform="rotate(-0 49.828125 155.178573)">0.850</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="128.503149" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="132.301977" transform="rotate(-0 49.828125 132.301977)">0.875</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="105.626553" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="109.425381" transform="rotate(-0 49.828125 109.425381)">0.900</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="82.749957" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="86.548786" transform="rotate(-0 49.828125 86.548786)">0.925</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="59.873362" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="63.67219" transform="rotate(-0 49.828125 63.67219)">0.950</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="36.996766" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="40.795594" transform="rotate(-0 49.828125 40.795594)">0.975</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="14.12017" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="17.918998" transform="rotate(-0 49.828125 17.918998)">1.000</text>
     </g>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.797656" y="95.904" transform="rotate(-90 14.797656 95.904)">accuracy</text>
    </g>
   </g>
   <g id="line2d_15">
    <path d="M 72.046307 159.386553 
L 99.715728 127.931234 
L 127.38515 122.212085 
L 182.723993 85.609532 
L 265.732257 44.43166 
L 376.409943 15.264 
" clip-path="url(#pa154a6d0a8)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
    <defs>
     <path id="m98ae7f93d8" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #1f77b4"/>
    </defs>
    <g clip-path="url(#pa154a6d0a8)">
     <use xlink:href="#m98ae7f93d8" x="72.046307" y="159.386553" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="99.715728" y="127.931234" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="127.38515" y="122.212085" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="182.723993" y="85.609532" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="265.732257" y="44.43166" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="376.409943" y="15.264" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="line2d_16">
    <path d="M 72.046307 171.968681 
L 99.715728 144.516766 
L 127.38515 162.818043 
L 182.723993 169.681021 
L 265.732257 176.544 
L 376.409943 176.544 
" clip-path="url(#pa154a6d0a8)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
    <defs>
     <path id="m43dc4bf304" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #ff7f0e"/>
    </defs>
    <g clip-path="url(#pa154a6d0a8)">
     <use xlink:href="#m43dc4bf304" x="72.046307" y="171.968681" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="99.715728" y="144.516766" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="127.38515" y="162.818043" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="182.723993" y="169.681021" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="265.732257" y="176.544" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="376.409943" y="176.544" style="fill: #ff7f0e; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 56.828125 184.608 
L 56.828125 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 391.628125 184.608 
L 391.628125 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 56.828125 184.608 
L 391.628125 184.608 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 56.828125 7.2 
L 391.628125 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_7">
     <path d="M 63.828125 45.201563 
L 119.103125 45.201563 
Q 121.103125 45.201563 121.103125 43.201563 
L 121.103125 14.2 
Q 121.103125 12.2 119.103125 12.2 
L 63.828125 12.2 
Q 61.828125 12.2 61.828125 14.2 
L 61.828125 43.201563 
Q 61.828125 45.201563 63.828125 45.201563 
L 63.828125 45.201563 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="line2d_17">
     <path d="M 65.828125 20.298438 
L 75.828125 20.298438 
L 85.828125 20.298438 
" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#m98ae7f93d8" x="75.828125" y="20.298438" style="fill: #1f77b4; stroke: #1f77b4"/>
     </g>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="93.828125" y="23.798438" transform="rotate(-0 93.828125 23.798438)">train</text>
    </g>
    <g id="line2d_18">
     <path d="M 65.828125 35.299219 
L 75.828125 35.299219 
L 85.828125 35.299219 
" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#m43dc4bf304" x="75.828125" y="35.299219" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     </g>
    </g>
    <g id="text_18">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="93.828125" y="38.799219" transform="rotate(-0 93.828125 38.799219)">test</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pa154a6d0a8">
   <rect x="56.828125" y="7.2" width="334.8" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>The training score climbs with depth; the test peaks at 2 and falls.</figcaption>
</figure>

- `validation_curve` tries the values of one setting (`param_name`) with
  cross-validation. It is a one-setting grid search that also gives the
  training score.
- As depth grows the training score climbs from 0.841 to 0.999; the test is
  highest at 2 (0.857) and then falls. Where the two curves open up is where
  overfitting starts.

## Summary

- `StratifiedKFold` for classification; `shuffle=True` on data that may be
  sorted; `GroupKFold` when the same person/device has several rows;
  `TimeSeriesSplit` in time.
- A splitter object is given to every tool with `cv=`: `cross_val_score`,
  `cross_validate`, `GridSearchCV`, `learning_curve`.
- `cross_validate` for several measures and the training score;
  `learning_curve` for the effect of data size, `validation_curve` for one
  setting.
