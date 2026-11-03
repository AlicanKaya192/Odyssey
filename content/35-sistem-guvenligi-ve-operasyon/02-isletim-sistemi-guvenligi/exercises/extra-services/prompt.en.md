`extra_services(running, needed)` should return the services that are
running but not in the needed list, **once each** and in alphabetical
order, as a list. These are candidates to switch off: they grow the attack
surface.

**Expected output:**

```
['ftp', 'telnet']
```
