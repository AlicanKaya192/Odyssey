In a growing program, SQL queries are not spread all over the code; all the
code that talks to the database is gathered in **one class** (the data
access layer, a "repository"). The rest of the program works only with
objects.

```python
import sqlite3
from contextlib import closing
from dataclasses import dataclass


@dataclass
class Task:
    title: str
    done: bool = False
    id: int | None = None


class TaskStore:
    CREATE = ("CREATE TABLE IF NOT EXISTS tasks "
              "(id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER)")
    INSERT = "INSERT INTO tasks (title, done) VALUES (?, ?)"
    OPEN = "SELECT id, title, done FROM tasks WHERE done = 0 ORDER BY id"

    def __init__(self, path=":memory:"):
        self.conn = sqlite3.connect(path)
        self.conn.execute(self.CREATE)

    def add(self, task: Task) -> Task:
        with self.conn:
            cur = self.conn.execute(self.INSERT, (task.title, int(task.done)))
        task.id = cur.lastrowid
        return task

    def open_tasks(self) -> list[Task]:
        rows = self.conn.execute(self.OPEN)
        return [Task(title, bool(done), id_) for id_, title, done in rows]

    def close(self):
        self.conn.close()


with closing(TaskStore()) as store:
    store.add(Task("write report"))
    store.add(Task("send mail", done=True))
    store.add(Task("call ada"))
    for task in store.open_tasks():
        print(task)
```

```text
Task(title='write report', done=False, id=1)
Task(title='call ada', done=False, id=3)
```

## Why like this?

- **SQL in one place:** if the table changes, only `TaskStore` changes. The
  queries are constants of the class; the calling code sees no SQL.
- **Objects in, objects out:** `add` takes a `Task`, fills in its id
  (`lastrowid`) and gives it back; `open_tasks` turns rows into `Task`s.
  SQLite has no `bool`; `done` is stored as 0/1 and the class converts it to
  `bool`.
- **Every write is a transaction:** `with self.conn:`.
- **Closing:** there is a `close()` method, and `closing(...)` calls it at the
  end of the block.
- **Testable:** with `":memory:"`, an empty, fast database in every test.

If the database changes later (to PostgreSQL, say), only this class is
rewritten; the rest of the program keeps seeing `add` and `open_tasks`.
