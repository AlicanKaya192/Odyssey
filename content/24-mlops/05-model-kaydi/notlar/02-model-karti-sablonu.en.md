A template for filling in a model card. Every field can be short, but
none should stay empty.

| Field | Question | For this module's model |
|---|---|---|
| Name and version | Which model? | `churn`, version 1 |
| What it does | What does it predict? | The customers who will cancel their subscription |
| Who uses it | Which decision is the prediction used in? | The customer team, when choosing whom to call |
| Data | What was it trained on? | 2000 customers, month 0, fingerprint in the registry |
| Measurement | How was it measured? | Accuracy on a 1000-customer evaluation set; together with the baseline |
| Limits | Where should it not be used? | On another service's customers; when prices change a lot |
| Known errors | Where does it go wrong? | More often on new customers (short tenure) |
| Owner | Whom to ask when there is a problem? | The team that registered the model |

## Why are the limits the most important?

A model doesn't raise an error outside the world it was trained in; it
just predicts wrongly. The limits part of the card makes sure the person
using it knows this from the start. Later, in the Concept Drift section,
we will measure what happens when the weight of the price changes:
exactly the situation this line warns about.

## Checklist

- Does every version in production have a card?
- Does the card carry the same number as the version in the registry?
- Is the baseline written next to the measurement?
- Is the limits part filled in?

## Don't

- Don't write the card once and leave it; if the data or the measurement
  changed in a new version, the card changes too.
- Don't write only the best-looking number as the measurement; how it
  was measured is written too.
