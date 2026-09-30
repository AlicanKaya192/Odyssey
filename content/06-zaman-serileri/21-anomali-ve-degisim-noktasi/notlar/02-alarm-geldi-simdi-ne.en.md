A detector only says "there is something here". You decide what it is.

## Five questions

1. **The data or the world?** Suspect the measurement first: did a sensor get
   stuck, did records arrive incomplete, did a time zone slip, did a unit
   change? Most anomalies come from the data pipeline itself.
2. **One or a run?** A single alarm is an anomaly; alarms one after another in
   the same direction are a level shift.
3. **Is it in other series too?** If every shop falls on the same day the
   cause is shared (a holiday, a system outage); if it is one shop, it is
   local.
4. **Does it coincide with a known event?** The campaign calendar, the
   maintenance log, release notes, public holidays.
5. **Will it happen again?** If so the model should learn it (Section 18); if
   not it is repaired before training (Section 13).

## The decision table

| Finding | Example | What to do |
|---|---|---|
| A data error | Stuck sensor, duplicate record, −999 | Treat as missing, fill; fix the source |
| A one-off real event | An outage, a single campaign | Flag, explain; repair for training |
| A recurring real event | A holiday, payday | Add to the model as a variable |
| A level shift | A new customer, a price change | Record; renew the reference and the model |
| A slope change | Growth slowed | Learn the trend from the recent period |
| A volatility change | A machine came loose | Find the cause; renew the scale |

## Keep an event log

One line per alarm: when, which series, the score, what it was, what was done.

| Column | Why |
|---|---|
| `timestamp`, `series` | What, where |
| `score`, `direction` | How much, which way |
| `label` (real / false / data error) | To be able to measure the threshold later |
| `cause` | To recognise it next time |
| `action` | Was it repaired, was it added to the model |

This log is the **only source** of the precision–recall table of Part 10.
Whether a detector without labels is any good cannot be known.

## Looking after the detector

- **Renew the reference.** When the level or the volatility changes the old
  profile and scale are invalid; without renewal, constant alarms.
- **Keep anomalies out of the expectation.** Use the median, or leave flagged
  days out of the expectation.
- **Watch the number of alarms.** The weekly alarm count is a series in its
  own right; a sudden rise in it is a change point.
- **Watch the silence too.** A detector that never alarms is either very good
  or broken: the data feed may have stopped. "When did the last record
  arrive?" is a separate check.

## Ways of reducing false alarms

| Route | How |
|---|---|
| A better expectation | Add context: hour, day, holiday, campaign |
| Ask for confirmation | Alarm only if two observations in a row cross the threshold (at the price of delay) |
| Two levels | Score 3–5: write to the daily report; above 5: notify at once |
| Merge | Make the alarms of one event a single notification |
| Suppress known events | Planned maintenance, an announced campaign |

## Limits

- A detector counts as an anomaly **everything its expectation does not
  know**. Raising an alarm on the first holiday is not a mistake but missing
  information.
- At the start of a series there is not enough past; the first weeks are not
  judged.
- A slow drift (a thousandth a day) triggers neither a threshold nor CUSUM; a
  long-range comparison is needed (this month against the same month last
  year).
- In systems with many series (a thousand sensors) a 1% false alarm rate per
  series means ten false alarms every day: thresholds are tightened in line
  with the number of series.
