docker volume create notes
docker run --rm -v notes:/data notesapp
docker volume ls
docker volume inspect notes
docker volume rm notes
