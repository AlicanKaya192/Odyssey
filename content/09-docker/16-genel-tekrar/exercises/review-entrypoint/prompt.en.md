`greet.py` greets the name it is given. Right now `docker run app Ada` tries
to run a command called `Ada` instead of the program.

**What to do:** make the command fixed and the name changeable:

1. `ENTRYPOINT` in exec form: `python greet.py`.
2. `CMD` in exec form with the default name: `world`.

Odyssey will run it twice:

```
docker run app      ->  hello world
docker run app Ada  ->  hello Ada
```
