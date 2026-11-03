Most mistakes in XSS defence come from using the right tool in the wrong
place.

## Encoding input when storing it

Saving a comment to the database with `html.escape` looks safe at first,
but it causes two problems: the same text comes out with odd characters
like `&lt;` when it goes into a JSON response or an e-mail, and one day an
old record saved without encoding reaches the screen without encoding.
Data is stored as it is and encoded by the rules of the place it goes to
**when it is written there**.

## A block-list filter

A filter that deletes or rejects the word `<script>` does not stop XSS:
the `<script>` tag is not the only way to run a script, and browsers
tolerate many differences in spelling. A block list always forgets
something; output encoding neutralises every special character.

## Thinking only of the HTML body

`html.escape` is not enough in an attribute value written without quotes;
it does not check the scheme in a link address; it is not suitable at all
inside a script block. First ask "where does this value go on the page?".

## Markers that switch encoding off

Template engines' markers meaning "this value is safe, do not encode" are
used only for HTML **the developer wrote themselves**. Every line where
this marker is put on a value from the user gets a question mark in
review.

## Relying on CSP and dropping encoding

CSP is a second layer. A policy with `'unsafe-inline'`, one that allows
scripts from anywhere, or one with no `script-src` provides no protection;
even a correct policy does not close every hole.

## What to check in review

- [ ] Does user data enter HTML with an f-string or `+`?
- [ ] Is there a marker in the template that switches encoding off, and
  what is it on?
- [ ] Is the scheme checked in `href` and `src` values?
- [ ] Does the page's JavaScript write text taken from the address or input
  as HTML (DOM-based)?
- [ ] Is there a CSP header, and does it contain `'unsafe-inline'`?
- [ ] Is the session cookie `HttpOnly`?
