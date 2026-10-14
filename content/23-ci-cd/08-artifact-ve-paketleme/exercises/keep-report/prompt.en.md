When the tests fail, finding the details in a long log is hard. Keep the test report:

- pytest should also write the result to the `report.xml` file (`--junitxml=report.xml`).
- Then upload `report.xml` as an artifact named `test-report`, kept for 14 days.
- The upload should run **even if the tests fail**.
