docker build -t notes .
docker run -d --name api -p 8095:8000 -v notes-data:/data notes
docker logs -f api
docker compose up -d --build
docker compose down -v
