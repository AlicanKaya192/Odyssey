docker run --rm -e APP_ENV=production app
docker run --rm --env-file app.env app
docker build --build-arg VERSION=2.1 -t app .
