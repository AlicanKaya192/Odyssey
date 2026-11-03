`safe_path(base, name)` should add `name` to the `base` folder
(`posixpath.join`) and normalise the result with `posixpath.normpath`;
return the path if the result starts with `base + "/"`, otherwise `None`.
The starter code checks without normalising.

**Expected output:**

```
cat.png /srv/app/uploads/cat.png
../settings.ini None
a/../../x None
/etc/x None
```
