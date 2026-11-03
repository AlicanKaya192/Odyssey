File upload is where input validation has the most layers: the file's
name, type, size and content are separate inputs.

## Name

- Do **not use** the name the user gave as the file name on disk. Store the
  file under a random name (`secrets.token_hex(16)`) and keep the real name
  as a label in the database.
- If the name is shown, encode it when writing it on screen (XSS).
- If the name is added to a path, normalise it and check that it is inside
  the folder (path traversal).

## Type

- Do not trust the extension (`.png`) or the type the browser reports; both
  are in the user's hands.
- Limit the allowed types with a **list** (images only, say) and check that
  the file really is that type by looking at its first bytes.
- Do not put an uploaded file somewhere the server could **run** it
  (folders interpreted as scripts).

## Size

- Limit the maximum size and stop reading when the limit is passed; do not
  read the whole file into memory and measure afterwards.
- For compressed files, limit the uncompressed size too: a small archive
  can open into very large content.

## Content

- Images can be stored after re-processing (re-encoding); extra data
  hidden inside is dropped.
- If files are served from a separate domain, even if something inside
  them runs, it cannot reach the main site's cookies and pages.

## Short checklist

- [ ] A random file name, the real name only as a label.
- [ ] A type allow list + a check of the first bytes.
- [ ] A size limit (the uncompressed size too for compressed files).
- [ ] Stored somewhere it cannot be run.
- [ ] Served from a separate domain if possible.
