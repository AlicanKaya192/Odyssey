The rule "configuration lives in the environment" comes from a widely used
list of principles written for cloud applications: **The Twelve-Factor App**.
The points that will help you most when working with containers:

## III. Config in the environment

The code is the same everywhere; everything that changes with the environment
(the database address, keys, the mode) is in environment variables. A test:
**if you made the code public today, would a secret leak?** If it would, that
secret is in the code.

## V. Build, release, run are separate

- **Build**: an image from the code → `docker build`.
- **Release**: the image + the settings of that environment.
- **Run**: `docker run -e ...`.

The same image is tried on the test server and goes to the real server
**unchanged**; only the settings differ. The cure for "it worked in testing,
it broke in production".

## VI. Processes are stateless

The program keeps lasting information not inside itself but in a database or
a volume. A container can be removed and re-created at any moment (the rule
from the First Containers section).

## VII. Port binding

The program listens on a port itself and serves the outside through that port
(the Ports section).

## IX. Fast start-up, graceful shutdown

Programs that start fast and close properly on SIGTERM are easily moved,
multiplied and restarted (the CMD and ENTRYPOINT section).

## XI. Logs are a stream

The program writes its log not to a file but to **standard output**
(`print`); collecting it is Docker's job (`docker logs`).

## What does it bring?

An image that follows these rules can run on any server, in the cloud or on
your friend's computer **without changing anything**: exactly what Docker
promises.
