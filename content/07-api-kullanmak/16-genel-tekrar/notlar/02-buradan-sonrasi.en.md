The Using APIs module is done. Ways to make what you learnt stick and to move to the next step.

## Practice with real APIs

Everything you learnt on the practice server holds for real APIs too. Good
candidates to start with:

- **Open APIs without keys:** services such as weather, country information
  and open data portals that need no sign-up. Ideal for first tries.
- **The GitHub API:** very well documented; it works without a key under a
  low rate limit, and the limit rises with a key. You see pagination, rate
  limit headers and authentication in their real form.
- **Data from your own field:** find an open API on a topic you care about
  (sport, finance, transport) and build a small dataset from it.

With every new API follow the same order: read the documentation, try it in
the browser or with curl/Postman, then turn it into Python.

## A small project idea

1. Pick an open API.
2. Adapt the pipeline template from Section 15 to it: fetch, store, flatten,
   check, write.
3. Open the dataset with pandas and ask a question ("which is the most?",
   "how did it change over time?").
4. Run the pipeline incrementally every day for a week; watch the change.

## The next paths

- **Writing REST APIs with FastAPI:** the other side of the table.
  You will write your own endpoints, validate with Pydantic and see Swagger UI
  at `/docs`; at the end of the path you will put a machine learning model
  behind an API.
- **Docker:** packing the API you wrote into something that runs the same on
  every computer.

## Worth remembering

> Code first, then the body. A time limit on every request. Retry only
> temporary errors. The key never goes into the code. Keep the raw data.
