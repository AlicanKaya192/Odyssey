`digest_bits(names)` should return a `[name, bits]` list for every
algorithm name. The number of bits is the `digest_size` (bytes) of the
object made with `hashlib.new(name, b"")`, times 8.

**Expected output:**

```
md5 128
sha1 160
sha256 256
sha512 512
```
