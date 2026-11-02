Every pipe pattern, at a glance.

## Forms

| Form | What it does |
|---|---|
| <code>a &#124; b</code> | The output of a becomes the input of b |
| <code>a &#124; b &#124; c</code> | A chain: a → b → c |
| <code>a &#124; b &gt; f</code> | Writes the result of the chain into f |
| <code>a 2&gt;&amp;1 &#124; b</code> | Gives the error messages to b too |
| <code>a 2&gt; /dev/null &#124; b</code> | Drops the errors, processes only the output |

## Common chains

| Chain | What it finds |
|---|---|
| <code>ls folder &#124; wc -l</code> | The number of items in the folder |
| <code>sort f &#124; head -n 3</code> | The first three sorted lines |
| <code>head -n 6 f &#124; tail -n 3</code> | Lines 4, 5 and 6 |
| <code>grep word f &#124; wc -l</code> | The number of lines containing the word |
| <code>cat -n f &#124; tail -n 2</code> | The last two lines with their real numbers |
| <code>ls &#124; grep md</code> | Names containing md |

## Useful on the right of a pipe

Commands that read their input: `sort`, `head`, `tail`, `wc`, `grep`, `cat`,
`uniq`, `cut`, `tr`. Commands that ignore it: `ls`, `cd`, `mkdir`, `echo`, `rm`.

## Remember

- Spaces are free: `a|b` and `a | b` are the same.
- If you save, `>` goes at the end.
- In a real terminal, see and save at once: `a | tee f`.
