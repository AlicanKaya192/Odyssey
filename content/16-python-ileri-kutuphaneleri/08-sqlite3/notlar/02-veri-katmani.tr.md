Büyüyen bir programda SQL sorguları kodun her yerine dağılmaz; veritabanıyla
konuşan bütün kod **tek bir sınıfta** toplanır (veri erişim katmanı,
"repository"). Programın geri kalanı yalnızca nesnelerle çalışır.

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

## Neden böyle?

- **SQL tek yerde:** tablo değişirse yalnızca `TaskStore` değişir.
  Sorgular sınıfın sabitleri; arayan kod SQL görmüyor.
- **Nesneler içeri, nesneler dışarı:** `add` bir `Task` alıyor, kimliğini
  (`lastrowid`) doldurup geri veriyor; `open_tasks` satırları `Task`'a
  çeviriyor. SQLite'ta `bool` yok, `done` 0/1 saklanıyor, sınıf bunu
  `bool`'a çeviriyor.
- **Her yazma bir işlem:** `with self.conn:`.
- **Kapatmak:** `close()` metodu var, `closing(...)` blok sonunda çağırıyor.
- **Sınanabilir:** `":memory:"` ile her testte boş, hızlı bir veritabanı.

İleride veritabanı değişirse (PostgreSQL gibi) yalnızca bu sınıf yeniden
yazılır; programın geri kalanı `add` ve `open_tasks` görmeye devam eder.
