Turning a question into MapReduce means answering "what will map emit, what
will the key be, what will reduce combine?". Patterns for common jobs.

## Mean

A mean does not combine directly (Section 3); let map emit `(total, count)`:

```python
def mapper(row):
    yield row["city"], (row["unit_price"], 1)

def reducer(key, values):
    total = sum(v[0] for v in values)
    count = sum(v[1] for v in values)
    return key, total / count
```

A combiner can add up the same pairs too.

## Number of distinct values

"How many different customers are there in each city?" Two steps:

1. Map emits `((city, customer), None)`; reduce writes each key once → the
   repeats are gone.
2. A second MapReduce: map emits `(city, 1)`; reduce adds up.

## The top N

"The 10 most expensive orders." Each piece takes its own top 10 (a combiner),
and a single reduce picks the top 10 among those. The `nlargest` pattern from
Section 3.

## A join

Joining the orders with the customer table on `customer_id`:

```python
def mapper(record, source):
    yield record["customer_id"], (source, record)

def reducer(key, values):
    customers = [r for s, r in values if s == "customer"]
    orders = [r for s, r in values if s == "order"]
    for c in customers:
        for o in orders:
            yield {**c, **o}
```

Each record carries a tag saying which table it came from; all of a customer's
records arrive at the same reduce, so they are matched there. A job that is a
single line in SQL is a MapReduce step here; Spark and Hive build it for you.

## An inverted index

The basis of search engines: "which documents does each word appear in?"

```python
def mapper(doc_id, text):
    for word in set(text.split()):
        yield word, doc_id

def reducer(word, doc_ids):
    return word, sorted(doc_ids)
```

## Check questions

- What is the key? The values of the same key will meet in reduce.
- Can what reduce does be combined? If so, use a combiner.
- Is one key very big? There is skew; think about salting.
- Is one step enough? Jobs such as distinct counts and joins need two steps.
