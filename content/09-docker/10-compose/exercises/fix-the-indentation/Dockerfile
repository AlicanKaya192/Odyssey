FROM python:3.13-slim
WORKDIR /srv
COPY index.html .
EXPOSE 8000
CMD ["python", "-m", "http.server", "8000"]
