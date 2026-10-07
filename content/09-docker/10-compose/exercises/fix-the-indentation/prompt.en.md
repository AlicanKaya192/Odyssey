This compose.yaml cannot be read: `docker compose up` says:

```text
did not find expected key
```

**What to do:** find the line whose indentation is shifted and fix it. All of
`web`'s settings (`build`, `ports`, `environment`) must start in the same
column.
