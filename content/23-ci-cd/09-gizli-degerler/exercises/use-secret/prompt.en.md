In this workflow the report service's key is written openly in the file. The key now lives in the repository's store under the name `REPORT_API_KEY`:

- The step's `REPORT_API_KEY` environment variable should take its value from `${{ secrets.REPORT_API_KEY }}`.
- The openly written key should not remain anywhere in the file.
