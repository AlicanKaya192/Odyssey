| | Batch prediction | Online prediction |
|---|---|---|
| When | At regular times (every night) | When a request arrives |
| Result | A table or a file | An API answer |
| Speed needed | Hours are fine | Milliseconds |
| Infrastructure | A scheduled script | A service that is always on |
| Example | The list of customers to call in the morning | An offer on the cancellation page |

## Rules of serving

- The model is loaded once **when the program starts**; requests use the
  same object. The lesson's measurement: for 100 requests, the reloading
  way loaded 100 times, the load-once way 1 time.
- Before loading, the file's hash is compared with the registry's.
- The input is checked with the training rules; a request that breaks
  them gets `422`.
- Training and serving use **the same** feature code.
- The model version is written next to every prediction: in the answer,
  in the file, in the record.
- `/health` also says the model version.

## Latency percentiles

| Measure | Meaning |
|---|---|
| Average | Slow requests pull it; it can be a number nobody experienced |
| p50 (median) | Half of the requests are faster than this |
| p95 | 95% of the requests are faster than this |
| p99 | 99% of the requests are faster than this |

The nearest-rank method: sort the values and take element number
`ceil(p / 100 × n)`. For the lesson's 20 latencies, p50 = 13 ms,
p95 = 90 ms, and the average is 28.95 ms.

## Terms

- **Serving:** getting predictions to where they will be used.
- **Batch prediction:** scoring many rows at once, at regular times.
- **Online prediction:** answering an incoming request at once.
- **Latency:** how long it takes for a request's answer to arrive.
- **Percentile:** the limit below which a certain percentage of the
  values fall.
