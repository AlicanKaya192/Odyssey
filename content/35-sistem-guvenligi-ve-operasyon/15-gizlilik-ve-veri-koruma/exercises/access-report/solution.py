def access_report(tables, email):
    person = email.lower()
    lines = []
    for table in sorted(tables):
        count = sum(1 for row in tables[table] if row["email"].lower() == person)
        if count:
            lines.append(f"{table}: {count}")
    return lines

TABLES = {
    "orders": [{"email": "ada@example.org"}, {"email": "ADA@example.org"}],
    "customers": [{"email": "ada@example.org"}, {"email": "bob@example.org"}],
    "newsletter": [{"email": "bob@example.org"}],
}
for line in access_report(TABLES, "Ada@example.org"):
    print(line)
