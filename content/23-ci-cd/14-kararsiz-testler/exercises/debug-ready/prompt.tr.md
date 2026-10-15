`test` işini hata ayıklamaya hazırla:

- Asılı kalırsa 15 dakikada dursun: `timeout-minutes: 15`.
- pytest sonuçları dosyaya yazsın: `python -m pytest -q --junitxml=report.xml`.
- Son adım raporu **yalnızca test düşerse** saklasın: `actions/upload-artifact@v4`, `name: test-report`, `path: report.xml`.
