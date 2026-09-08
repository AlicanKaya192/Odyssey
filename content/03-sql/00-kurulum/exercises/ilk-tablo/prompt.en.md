A table named **`cities`** ("cities") is waiting on the server. It holds
five cities; each row has the city's name, its country and its
population.

Your task is to bring back **all** of it.

Two words do the job:

- `SELECT` — "give me this". Put `*` next to it and it means "every
  column".
- `FROM` — "from this table".

The result should be five rows and four columns:

```
id  name      country  population
--  --------  -------  ----------
1   Istanbul  Turkey   15840900  
...
```

The order of the rows does not matter; whatever order the server returns
them in is accepted.
