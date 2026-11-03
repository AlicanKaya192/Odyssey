def access_report(tables, email):
    lines = []
    for table, rows in tables.items():
        count = sum(1 for row in rows if row["email"] == email)
        lines.append(f"{table}: {count}")
    return lines

TABLES = {
    "orders": [{"email": "ada@example.org"}, {"email": "ADA@example.org"}],
    "customers": [{"email": "ada@example.org"}, {"email": "bob@example.org"}],
    "newsletter": [{"email": "bob@example.org"}],
}
for line in access_report(TABLES, "Ada@example.org"):
    print(line)
