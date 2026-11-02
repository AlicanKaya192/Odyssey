Bias is hard to see in the data: the mean of a biased sample is also a
tidy, plausible number. The way to notice it is to ask **how the selection
was made**. Four common kinds:

## Coverage bias

Part of the population has no chance of being picked at all. An in-app
survey never reaches users who deleted the app; an email survey skips
people who do not read their email.

**Ask:** Whose chance of being picked is zero?

## Voluntary response bias

People choose whether to take part. Those who write reviews are often very
happy or very angry; the quiet majority in the middle stays invisible.

**Ask:** Could answering at all be related to the answer?

## Survivorship bias

You only look at those who passed some filter. "Users of one year are very
satisfied" is true, but the unsatisfied ones already left.

**Ask:** Who was filtered out before reaching this group?

## Non-response bias

Everyone was asked but some did not answer, and those who did not answer
are different. Busy people abandon a long survey; the result becomes the
voice of those with free time.

**Ask:** Are the people who did not answer different from those who did?

## The example in this section

Showing the survey only after the fifth visit is coverage bias: users who
visit rarely have no chance of being picked. Frequent visitors stay longer,
so the average session length always comes out high, and a bigger sample
does not change that.

## What to do

- Make the selection random: the same chance for everyone.
- If you cannot, write down who is missing and state the result only for
  the selected group ("among frequent visitors the average is ...").
- Compare known features of the sample (age, visits) with the population;
  a large gap is a warning sign.
