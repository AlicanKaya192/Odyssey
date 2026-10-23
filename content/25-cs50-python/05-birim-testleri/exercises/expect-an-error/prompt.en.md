Write two tests. `test_numbers` should try `square`'s result with a few numbers (positive, negative, zero). `test_str` should assert that `square("cat")` raises a `TypeError`: call it inside a `with pytest.raises(TypeError):` block.

One of the broken versions does not raise an error for a string; it returns the string as it is. Only `test_str` catches that.
