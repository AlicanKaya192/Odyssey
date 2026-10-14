**Uploading and downloading**

| Action | Setting | Meaning |
|---|---|---|
| `actions/upload-artifact@v4` | `name` | The artifact's name (unique in the run) |
| | `path` | The file or folder to upload |
| | `retention-days` | How many days it is kept (default 90) |
| `actions/download-artifact@v4` | `name` | Which artifact; all if not written |
| | `path` | The folder to download into |

**Cache or artifact?**

| | Cache | Artifact |
|---|---|---|
| Purpose | Speed | The product |
| Found by | A key | A name |
| Belongs to | A branch | A run |
| Downloadable by hand | No | Yes, from the run's page |
| If it is lost | The job must still work | No product |

**Common patterns**

```yaml
      # The build job
      - run: python -m build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

      # The next job (needs: build)
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - run: pip install dist/*.whl
```

```yaml
      # A report even when the tests fail
      - run: python -m pytest --junitxml=report.xml
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: report-${{ matrix.os }}
          path: report.xml
          retention-days: 14
```

**Rules**

- Build once; the tested and the released file are the same.
- No `checkout` in the smoke-test job: only the package.
- In a matrix, the name comes from the matrix: no two uploads with the
  same name.
- The report with `if: always()`: it is needed most when things fail.
