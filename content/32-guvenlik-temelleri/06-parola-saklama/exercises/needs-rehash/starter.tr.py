def needs_rehash(record, min_iterations):
    parts = record.split("$")
    return parts[1] < str(min_iterations)

for record in ["pbkdf2_sha256$1000$ab$cd", "pbkdf2_sha256$90000$ab$cd",
               "pbkdf2_sha256$600000$ab$cd", "md5$1$ab$cd"]:
    print(record.split("$")[1], needs_rehash(record, 600000))
