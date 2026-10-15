**The first pipeline in a real repository**

1. Create `.github/workflows/ci.yml` in the repository; only get the
   code and run the tests. Open a PR and see it run.
2. Add the fast gates: format and lint. Run them locally first, then in
   the pipeline.
3. Add `permissions: contents: read` and `timeout-minutes`.
4. If the tests are slow, a cache; if several versions are supported, a
   matrix.
5. A rule for `main`: a PR required, a required check.
6. If a release is needed: a job that starts with a tag, a version check,
   build once.

After every step, break a test on purpose to see the pipeline really
fail: a gate that does not fail is not a gate.

**What we did not run in this module**

- We did not run the workflows on GitHub's machine; we checked them
  without running. In a real run the action versions, the machine's
  installed tools and the durations show up on the page.
- Action versions (`@v4`, `@v5`) change over time; when writing a new
  file, look at the action's own page.
- Cost and limits: GitHub's machines are free for public repositories;
  private repositories have a monthly minute limit. Matrices and long
  jobs use up minutes quickly.

**Where next in Odyssey?**

- **MLOps and ML System Design:** the same pipeline to train, measure,
  register and serve a model.
- **Docker:** building the images from the twelfth section in depth.
- **Version Control with Git:** branches, merging and tags are the base the pipeline rests on.
- **Writing REST APIs with FastAPI:** a service with tests and
  deployment.

**Practical advice**

1. Set up this module's capstone pipeline for your own small project.
2. Note the pipeline's duration and its slowest job; start with the
   critical path.
3. When you see a flaky test, take a note: which commit, which result.
4. Before adding any new action, look at who wrote it and which
   permissions it asks for.
5. Review the pipeline's file like code too: change it with a PR, write
   down the reason.
