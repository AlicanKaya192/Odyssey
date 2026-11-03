import html
import sqlite3


def comments_html(rows, author):
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE comments (author TEXT, body TEXT)")
    db.executemany("INSERT INTO comments VALUES (?, ?)", rows)
    query = "SELECT body FROM comments WHERE author = ? ORDER BY rowid"
    found = db.execute(query, (author,)).fetchall()
    return ["<li>" + html.escape(body) + "</li>" for (body,) in found]

ROWS = [
    ["ada", "<i>hi</i>"],
    ["bob", "a & b"],
    ["o'brien", "x < y"],
    ["ada", "second"],
]
for author in ["ada", "o'brien", "zeynep"]:
    print(author)
    for line in comments_html(ROWS, author):
        print(" ", line)
