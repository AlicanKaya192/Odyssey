# Assessing Risk

In the previous section we said that risk is "likelihood × impact". In
this section we actually do that multiplication. Why is it needed? Because
no organisation has enough money, time and people for every risk. **Risk
assessment** means making risks comparable so you can decide which one
gets effort first, and how much.

There are two ways: a **qualitative** assessment done with words and small
scores, and a **quantitative** assessment done with money. We will see
both.

## Qualitative assessment: 1 to 5

The most common method is to give likelihood and impact a score between 1
and 5. What the scores mean is written down in advance, otherwise everyone
understands them differently:

| Score | Likelihood | Impact |
|---|---|---|
| 1 | Almost never | Negligible, nobody notices |
| 2 | Low, once in a few years | Small, fixed within hours |
| 3 | Medium, once a year | Medium, work stops for a day |
| 4 | High, once a month | Large, customer data affected |
| 5 | Almost certain | Very large, the organisation is at stake |

The **risk score** is the product of the two scores, so a number between 1
and 25. In this lesson we split the score into four **levels**: 1–4 low
(L), 5–9 medium (M), 10–16 high (H), 17–25 critical (C). Organisations
choose their own boundaries; what matters is that the boundaries are
written down beforehand.

Seeing every possible product in one table, that is, drawing a **risk
matrix**, is easier than memorising the levels:

```python
def level(score):
    if score <= 4:
        return "L"
    if score <= 9:
        return "M"
    if score <= 16:
        return "H"
    return "C"


print("impact:      1  2  3  4  5")
for likelihood in range(5, 0, -1):
    row = [level(likelihood * impact) for impact in range(1, 6)]
    print("likelihood", likelihood, " ", "  ".join(row))
```

```text
impact:      1  2  3  4  5
likelihood 5   M  H  H  C  C
likelihood 4   L  M  H  H  C
likelihood 3   L  M  M  H  H
likelihood 2   L  L  M  M  H
likelihood 1   L  L  L  L  M
```

The top right corner (likely and large) is urgent; the bottom left corner
(unlikely and small) can wait. Notice: a risk with likelihood 1 but impact
5 comes out as "low". Risks like this (an earthquake, all data being
wiped) are handled separately, not by the score; insurance and a disaster
recovery plan exist for them.

The good side of the qualitative method is that it is fast; the bad side is
that it is subjective. "Is it a 4 or a 3?" arguments are common. The scores
are given by several people together, not by one.

## Quantitative assessment: with money

Sometimes management asks "is this control worth our money?". Then the risk
is computed in money. The terms:

- **Asset value** (AV): what the asset is worth.
- **Exposure factor** (EF): how much of the value is lost in one event;
  between 0 and 1.
- **Single loss expectancy** (SLE): the cost of one event.
  **SLE = AV × EF**.
- **Annual rate of occurrence** (ARO): how many times a year the event is
  expected. Once in ten years is 0.1.
- **Annual loss expectancy** (ALE): the average yearly cost of this risk.
  **ALE = SLE × ARO**.

An example: if a customer database worth 500,000 leaks, 40% of its value is
lost (fines, lost customers); such a leak is expected once in ten years.

```python
asset_value = 500_000
exposure = 0.4
aro = 0.1
sle = asset_value * exposure
ale = sle * aro
print(f"SLE: {sle:.0f}  ALE: {ale:.0f}")
```

```text
SLE: 200000  ALE: 20000
```

This risk means an average loss of 20,000 every year. Now think of a
control that costs 5,000 a year and lowers the chance of a leak to once in
fifty years (ARO 0.02). Is the control worth the money?

```python
ale_after = sle * 0.02
cost = 5_000
net = ale - ale_after - cost
print(f"ALE after: {ale_after:.0f}  net benefit: {net:.0f}")
```

```text
ALE after: 4000  net benefit: 11000
```

The control brings the risk down from 20,000 to 4,000 and, after paying
its own cost, saves 11,000 a year. If the net benefit had been negative,
the control would cost more than the risk.

The weak side of the quantitative method is the numbers: "once in ten
years" is usually a guess. The result looks exact, but it is only as right
as its inputs. That is why the two methods are used together.

## Four answers to a risk

Once a risk has been assessed, one of four things is done:

| Answer | What it means | Example |
|---|---|---|
| **Mitigate** | Take a control to lower the likelihood or the impact | Adding a second step to the password |
| **Transfer** | Hand part of the loss to someone else | Cyber insurance, giving the service to a specialist |
| **Avoid** | Not do the activity that creates the risk at all | Not collecting data you do not need |
| **Accept** | Leave it as it is, knowingly and in writing | A small vulnerability on an unimportant test server |

No control brings risk to zero. The risk left after the controls is called
**residual risk**. The amount of risk an organisation is ready to accept is
called its **risk appetite**; if the residual risk is below that limit, it
is accepted.

Accepting is not "ignoring". An accepted risk is written down, who accepted
it is noted, and it is looked at again at regular intervals.

## The risk register

All risks are kept in a single table: the **risk register**. Every row
holds the risk's name, likelihood, impact, score, owner and the answer
given. The register is read starting from the highest score:

```python
register = [("laptop lost", 4, 3), ("db leak", 2, 5),
            ("site down", 3, 3), ("ransomware", 3, 5)]
ranked = sorted(register, key=lambda r: r[1] * r[2], reverse=True)
for name, likelihood, impact in ranked:
    score = likelihood * impact
    print(f"{score:>2} {level(score)} {name}")
```

```text
15 H ransomware
12 H laptop lost
10 H db leak
 9 M site down
```

Ransomware (3 × 5 = 15) is at the top of the list. A lost laptop (12) is
more frequent, but its impact is smaller. The database leak and the outage
have different scores (10 and 9) but are close to each other; in cases like
this the score alone does not decide, the team talks it through.

## Summary

- Risk assessment points scarce resources at the most important risk.
- **Qualitative:** likelihood and impact 1–5, the score is the product,
  the levels are written down in advance.
- **Quantitative:** SLE = AV × EF, ALE = SLE × ARO; a control's net benefit
  = ALE before − ALE after − the control's cost.
- Four answers: **mitigate**, **transfer**, **avoid**, **accept**. What is
  left is **residual risk**.
- Risks are kept in a **risk register** and reassessed regularly.
