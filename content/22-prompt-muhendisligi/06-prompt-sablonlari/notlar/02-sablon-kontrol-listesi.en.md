Three template ways in Python and their traps:

| Way | Placeholder | Trap | Safe use |
|---|---|---|---|
| `str.format` | `{name}` | JSON braces are taken for variables | `{{` and `}}` in the JSON |
| `string.Template` | `$name` | `safe_substitute` silently leaves missing ones | Only `substitute` |
| Your own `render` | `{{name}}` | `replace` one after another also fills inside values | One pass (`re.sub`) + a variable check |

**Before using a template:**

1. List the template's variables; compare them with the given values.
   Stop if one is missing or unused.
2. Put the values in with one pass.
3. Fit long variables into a budget; decide where to cut and show the cut
   with `...`.
4. Log the template's name and version.
5. Measure a new version against the old one with an evaluation set.

**Common mistakes:**

- **Sending a prompt with a missing variable.** The model interprets a mark
  such as `$order_id` in its own way.
- **Treating the customer's text as a template.** Marks in the text get
  filled or shift to the wrong place.
- **Always cutting long text from the start.** In support messages the
  real request is often at the end.
- **Changing a template in place.** If the old version is lost, two
  versions cannot be compared.
