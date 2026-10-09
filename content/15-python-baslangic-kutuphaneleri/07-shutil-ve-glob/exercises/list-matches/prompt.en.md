There is a `logs` folder next to your file: `2025-11.txt`, `2025-12.txt`,
`2026-01.txt`, `2026-02.txt`, `README.txt` and `old/2024-12.txt`.

Write the function `list_matches(pattern)`: return the paths matching the
pattern with `glob.glob` (`**` should go into subfolders too:
`recursive=True`) as a **sorted** list with `/` separators.

**Expected output:**

```
2
logs/2025-11.txt
logs/2025-12.txt
logs/2026-01.txt
logs/2026-02.txt
logs/README.txt
logs/old/2024-12.txt
```
