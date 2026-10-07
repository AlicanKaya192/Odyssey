Before using an API, look for the answers to these questions in its
documentation. Every question you cannot answer will come back later as an
error.

## Reading checklist

1. **What is the address?** The API's base address (for example
   `https://api.example.com`). Every endpoint is added after it.
2. **Which endpoints exist?** The name of each and what it is for:
   `/weather` for the weather now, `/forecast` for the coming days.
3. **What does each endpoint need?** Required information (`city`) and
   optional information (`units=metric`).
4. **What does the response look like?** Documentation usually includes a
   sample response. Which fields come back, and in which units are the
   numbers?
5. **Is identification needed?** Many APIs ask for a "key" (API key). The
   documentation says where to put it. We will see this in Section 08.
6. **What are the limits?** How many requests you may send per minute or per
   day. Go over it and the server stops answering for a while.
7. **Which errors can come back?** What the response is for cases such as
   "city not found" or "invalid key".

## A documentation example

A piece of an imaginary weather API's documentation:

```text
GET /weather
  city   (required)  City name, e.g. Istanbul
  units  (optional)  metric | imperial, default metric

Response 200:
  {"city": "Istanbul", "temp": 18, "sky": "cloudy"}

Response 404:
  {"error": "unknown city"}
```

From this much you learn that the endpoint is `/weather`, asking without
`city` is pointless, the temperature is in Celsius by default, and an unknown
city gets a `404` with an error message.

## When documentation is missing or incomplete

- Read the sample responses carefully; field names explain a lot.
- Send a small trial request and look at the response (you will see how to
  do that with tools in Section 14).
- Check the date and version number of the documentation: an old document
  may describe an API that has since changed.
