The Data Science module is finished. This note answers "what do I do now".

## An honest assessment first

Finishing the sections is not the same as having learned. Can you do the
following **without looking**?

- Read a CSV and check its shape, its types and its missing values
- Combine two conditions and filter the table
- Group by a column and take the count and the mean together
- Clean the column names and the text columns
- Draw a labelled bar chart and save it to a file
- Look at a `describe()` output and say something about the distribution

If you get stuck on one of them, go back to that section. If the foundation
is missing, everything laid on top of it wobbles.

## What you really learned was not the tools

You could forget how to write `groupby` in a week; you would look at the
reference note and remember. What must not be forgotten are these habits:

- Checking **how many records** an average was computed from before you take
  it.
- When you find a difference, asking **what else is different**.
- Keeping the difference between "they move together" and "one causes the
  other".
- Writing down **what you dropped** while cleaning.
- Being able to say **that a question cannot be answered with this data**.

The tools change; these do not.

## How to practise

**Work with your own data.** The best exercise is a question you genuinely
wonder about. For example:

- Writing your monthly spending into a CSV and grouping it by category
- Turning the sizes and dates of the files in a folder into a table and
  finding the biggest ones
- Taking a class's mark list and working out its distribution
- Analysing something you tracked for a year (books, exercise, sleep)

When you see something odd in your own data, **you know why it is there** —
and that is exactly where the learning happens. With a ready-made dataset
that connection is missing.

**Start small and finish.** An unfinished large analysis teaches you less
than a finished small one.

**Tell someone the result.** If you cannot reduce a finding to one sentence,
the analysis is not done.

## A checklist for when an analysis is finished

- [ ] Did I keep the raw data intact?
- [ ] Did I write down how many rows I dropped, and why?
- [ ] Does every group average have its group size next to it?
- [ ] Do the charts have a title, axis labels and units?
- [ ] Does the bar chart axis start at zero?
- [ ] Did I write a sentence that claims causation?
- [ ] Did I state the limits of the finding?
- [ ] Does running the code from the top give the same result?

The last item matters: small fixes made by hand make an analysis
**irreproducible**. Every step belongs in the code.

## What comes next

<figure class="fig">
  <div class="flow">
    <span class="node ok"><b>Data Science</b><br>done</span>
    <span class="arrow">→</span>
    <span class="node acc"><b>Statistics</b><br>how reliable is it</span>
    <span class="arrow">→</span>
    <span class="node"><b>Machine Learning</b><br>prediction</span>
  </div>
  <figcaption>The order is not fixed; statistics and machine learning can be learned in parallel. But both are built on this module.</figcaption>
</figure>

**Statistics** answers this question: is the difference you saw real, or is
it chance? In this module we said "a group of two is not a conclusion" but
never said how many people is enough. The answer is there.

**Machine learning** is looking at past data to say something about the
future. It is worth knowing: most of the time in a machine learning project
goes on the work you learned in this module. Fitting a model is a few lines;
understanding the data, cleaning it and finding the right question takes
weeks.

**SQL** is another tool waiting in line. Data usually lives in a database
rather than a file; the same job you did with `groupby` is written there in
another language. Since you know the logic, the move will be easy.

## In the meantime

Solving this module's exercises once more can be more useful than moving on
to a new topic — especially the ones whose solutions you looked at. The
second time round, what stays with you is not how the code is written but
**why it is written that way**.
