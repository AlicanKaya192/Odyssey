Web pages embed YouTube videos with an `iframe`:

`<iframe width="560" height="315" src="https://www.youtube.com/embed/xvFZjo5PgG0" title="YouTube video player" frameborder="0" allowfullscreen></iframe>`

The short form of that address is `https://youtu.be/xvFZjo5PgG0`. In `watch.py`, write `parse(s)`: it takes a string of HTML; if there is a YouTube embed URL in the `src` attribute of an `iframe` in it, it returns the short URL as a str, otherwise `None`. The URL has one of these forms: `http://youtube.com/embed/...`, `https://youtube.com/embed/...`, `https://www.youtube.com/embed/...` (`http://www.` too). The value of `src` is in double quotes; the `iframe` may have other attributes; there is at most one URL in the input. `main` asks for the HTML and prints `parse`'s result.

## How to test

- Input `<iframe src="http://www.youtube.com/embed/xvFZjo5PgG0"></iframe>` → output `https://youtu.be/xvFZjo5PgG0`
- Input `<iframe width="560" height="315" src="https://www.youtube.com/embed/xvFZjo5PgG0" title="YouTube video player" frameborder="0" allowfullscreen></iframe>` → output `https://youtu.be/xvFZjo5PgG0`
- Input `<iframe src="https://cs50.harvard.edu/python"></iframe>` → output `None`
