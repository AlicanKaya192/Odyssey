class Task:
    def __init__(self, title: str, done: bool = False):
        self.title = title
        self.done = done

    def finish(self) -> None:
        self.done = True

    def __str__(self) -> str:
        if self.done:
            return "[x] " + self.title
        return "[ ] " + self.title


class Board:
    def __init__(self):
        self.tasks: list[Task] = []

    def add(self, task: Task) -> int:
        self.tasks.append(task)
        return len(self.tasks)

    def pending(self) -> list[str]:
        titles: list[str] = []
        for task in self.tasks:
            if not task.done:
                titles.append(task.title)
        return titles


board = Board()
board.add(Task("write"))
board.add(Task("test"))
total = board.add(Task("ship"))

board.tasks[1].finish()

print(total)
print(board.tasks[1])
print(board.pending())
