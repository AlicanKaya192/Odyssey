docker ps -a
docker logs --tail 20 web
docker run --rm -it --entrypoint sh app
docker cp web:/app/error.log .
docker build --no-cache --progress=plain -t app .
