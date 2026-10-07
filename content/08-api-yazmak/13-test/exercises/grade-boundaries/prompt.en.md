`GET /grade?score=...` turns a score into a letter: 90 and above `A`, 80 and
above `B`, 70 and above `C`, below that `F`; outside 0–100 `422`.

**What to do:** write tests that try the boundaries with
`@pytest.mark.parametrize` (at least 5 tests). The broken versions will have
`>` instead of `>=` or the upper limit removed; your tests must catch them.
