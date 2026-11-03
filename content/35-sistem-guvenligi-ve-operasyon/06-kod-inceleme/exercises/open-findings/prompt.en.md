Each finding is `[line, message]`; `lines` are the source lines (line 1 =
`lines[0]`). A finding is closed only if its line has a mark **with a
reason**: `"# nosec: "` followed by a non-empty reason. Writing just
`# nosec` is not enough. `open_findings(findings, lines)` should return
the findings that stay open as `"<line>: <message>"`, sorted by line.

**Expected output:**

```
2: eval
3: eval
```
