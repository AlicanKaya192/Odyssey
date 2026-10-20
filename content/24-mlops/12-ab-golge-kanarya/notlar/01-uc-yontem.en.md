A new model is released in three steps; each step answers a different
question.

<figure class="fig">
  <div class="flow">
    <span class="node">Gate</span>
    <span class="arrow">→</span>
    <span class="node">Shadow</span>
    <span class="arrow">→</span>
    <span class="node">Canary</span>
    <span class="arrow">→</span>
    <span class="node acc">A/B test</span>
  </div>
  <figcaption>From an offline test to a live experiment.</figcaption>
</figure>

## Comparison

| | Shadow | Canary | A/B test |
|---|---|---|---|
| Who sees the answer | Nobody | A small share | Half the group |
| Are labels needed | Not for the difference | No (errors, latency, distribution) | Depends on the measure |
| Cost | Twice the computation | A slow release | A long time, many customers |

## The lesson's shadow measurement (month 6, 1000 customers)

| | Old model | New model |
|---|---|---|
| Predicted churn share | 0.586 | 0.456 |
| Accuracy with labels | 0.685 | 0.821 |

The two models decided differently for 298 customers.

## Routing with a bucket

```python
bucket = zlib.crc32(str(customer_id).encode()) % 100
side = "new" if bucket < percent else "old"
```

- The same customer always stays on the same model.
- As the share grows, those who saw the new model keep seeing it.

## Don't

- Don't route by rolling a die on every request; the customer goes back
  and forth between the two models.
- Don't show the shadow's answer to the customer; the shadow is only
  recorded.
