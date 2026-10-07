docker build -t greeter .
docker run --rm greeter
docker build -f Dockerfile.dev -t greeter:dev .
