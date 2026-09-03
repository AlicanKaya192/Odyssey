Testing a model on the data you trained it on is like handing a student
the exam questions in advance. So the data is **split in two** — and in this
exercise you will do that split by hand.

**What you need to do:**

1. Work out how many records **70%** of them is.
2. Keep the first that many as **training** and the rest as **test**.
3. Print the training and test counts **side by side**.
4. Print the **first record** of the test set.
5. Print the mean score of the **training records only**, rounded to two
   decimals.

**Expected output:**

```
7 3
('Ela', 83)
69.86
```

**The last line is what this exercise is really about.** Computing the mean
over all the data would be easier; but if that mean is later used as a
prediction, it carries information from the test records. Data the model
must not see must not enter its arithmetic either.

In practice `train_test_split` does this — that is the next section. First
you need to know what it does.
