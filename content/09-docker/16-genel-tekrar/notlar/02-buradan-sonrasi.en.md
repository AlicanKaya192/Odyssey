The track is over; here are things you can do on your own so what you
learned stays, and the next steps.

## Practice with your own projects

1. Package a Python program you wrote before (an exercise, a script): a
   Dockerfile, `.dockerignore`, a non-root user.
2. Look at its layers with `docker history`; fix the cache order, change
   the code, rebuild and see which steps are `CACHED`.
3. Add a volume to the program: remove the container and open it again — is
   the data still there?
4. Add a second service (an API and a program that calls it) and open both
   together with `compose.yaml`.

## A small project idea

Grow the notes API from the lesson:

- An endpoint that deletes a note (`DELETE /notes/1`).
- A separate `worker` service: every minute it looks at `/stats` and writes
  the result to the log; `depends_on` + `service_healthy`.
- A one-line command that backs up the database (the `tar` method from the
  Volume section).
- Try making the image smaller with a multi-stage build and measure the
  size.

## What to learn next

- **Pushing to an image registry:** putting your image on Docker Hub (or
  GitHub's registry) with `docker tag` and `docker push`; another computer
  gets it with `docker pull`.
- **Automatic builds:** having a CI service (such as GitHub Actions) build
  the image on every change.
- **Running on a server:** opening the same `compose.yaml` on a server with
  a different `.env`.
- **Managing many containers:** tools such as Kubernetes spread what
  Compose does across many computers; the basis is what you learned on this
  track.

## Next tracks

- **Writing a REST API with FastAPI:** you will write your own API
  and package it the way you learned on this track.
- **Machine Learning:** putting a model you trained behind an API and
  shipping it in a container is where the two tracks meet.

## Keep in mind

> A container comes and goes, an image can be rebuilt, the data in a volume
> stays. When something goes wrong, first find the phase: building, or
> running?
