def total_seconds(steps, builds):
    # Her derlemede adimlari sirayla gez; bir adim calismaya basladiysa
    # sonrakiler de calisir.
    pass


good = [
    ["FROM python:3.13-slim", [], 5],
    ["COPY requirements.txt .", ["requirements.txt"], 1],
    ["RUN pip install -r requirements.txt", [], 60],
    ["COPY . .", ["app.py", "requirements.txt"], 1],
    ["CMD python app.py", [], 0],
]
bad = [
    ["FROM python:3.13-slim", [], 5],
    ["COPY . .", ["app.py", "requirements.txt"], 1],
    ["RUN pip install -r requirements.txt", [], 60],
    ["CMD python app.py", [], 0],
]
builds = [[], ["app.py"], ["app.py"], ["requirements.txt"], ["app.py"]]
print("good order:", total_seconds(good, builds))
print("bad order:", total_seconds(bad, builds))
