docker network create shopnet
docker run -d --name api --network shopnet shop-api
docker run --rm --network shopnet shop-web
docker network ls
docker network inspect shopnet
