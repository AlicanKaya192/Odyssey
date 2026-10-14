The `build` job builds the package, but the files are lost with the machine. After the build, add an `actions/upload-artifact@v4` step:

- The artifact's name is `dist`
- The folder to upload is `dist/`
