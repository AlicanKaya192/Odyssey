Whether a pipeline is useful depends not only on how the file is written
but also on how the team works with it. Rules you will often hear:

1. **Small changes, merged often.** When a two-week change goes red, the
   problem is hard to find; in a twenty-line change it is easy.
2. **If the main branch is red, fix it first.** Adding work on top of a
   red branch hides which change caused the next failure.
3. **Fast stages first.** A style check takes seconds, long tests take
   minutes. If the cheap gate closes first, the expensive one is never
   reached.
4. **Keep the pipeline fast.** If the result takes longer than ten
   minutes, people stop waiting for it and the pipeline stops being a
   habit. Caching and parallel jobs exist for this (later sections).
5. **Run it locally too.** The pipeline does not run the tests instead of
   you; it catches a problem you missed on your computer. Run the tests
   yourself before you push.
6. **Remember the clean machine.** Nothing is ready on the runner: the
   first step is downloading the code (`actions/checkout`), then
   installing Python and the dependencies.
7. **Write the version of every action.** Write `actions/checkout@v4`, not
   `actions/checkout`. GitHub does not accept an action without a
   version; the version keeps the pipeline the same even when the action
   changes.

**Common symptom → likely cause**

| Symptom | Likely cause |
|---|---|
| `requirements.txt` not found | There is no step that downloads the code (`checkout`). |
| Passes for me, fails in the pipeline | A package is installed only on your computer. |
| The pipeline takes 20 minutes | Slow stages go first, there is no cache. |
| The pipeline is green but the program is broken | The broken thing has no test. |
