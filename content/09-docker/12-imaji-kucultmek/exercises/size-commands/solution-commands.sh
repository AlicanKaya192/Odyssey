docker build --target build -t report:build .
docker history report
docker run --rm report du -sh /report
