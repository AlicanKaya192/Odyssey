docker run --rm greet Ada
docker run --rm -it --entrypoint sh greet
docker run -d --init --name worker worker
docker stop -t 30 worker
