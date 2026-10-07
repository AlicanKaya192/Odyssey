In this project only the shop front (`web`) should be visible from outside.
`api` serves services on the same network; it does not need to be reached
from the computer, yet it is open to the outside.

**What to do:** remove the `ports:` lines of the `api` service. Keep
`web`'s.

Odyssey will bring the project up and send requests to the shop front and,
**from inside the network**, to the API; both must work.
