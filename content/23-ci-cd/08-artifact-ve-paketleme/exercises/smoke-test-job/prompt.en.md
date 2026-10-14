Add a `smoke-test` job that tries whether the package works once installed:

- It should start when `build` finishes; the machine is `ubuntu-latest`.
- It should **not** get the code; it should set up Python 3.13.
- It should download the `dist` artifact into the `dist` folder.
- It should install it with `pip install dist/*.whl`.
- It should run `python -c "import greeter; print(greeter.hello())"`.
