`channel_max` holds the highest level each channel can carry.

`can_share(level, channel, channel_max)` should return `True` if the level
does not exceed the channel's limit. An unknown channel or a level not in
`LEVELS` gives `False`: deny by default.

**Expected output:**

```
True
False
False
False
```
