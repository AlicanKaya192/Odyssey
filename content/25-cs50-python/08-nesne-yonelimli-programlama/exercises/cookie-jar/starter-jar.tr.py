COOKIE = "🍪"


class Jar:
    def __init__(self, capacity=12):
        # capacity negatif olmayan bir int değilse ValueError
        ...

    def __str__(self):
        # Kavanozdaki her kurabiye için bir COOKIE
        ...

    def deposit(self, n):
        # n kurabiye ekle; kapasite aşılırsa ValueError
        ...

    def withdraw(self, n):
        # n kurabiye al; yeterince yoksa ValueError
        ...

    @property
    def capacity(self):
        ...

    @property
    def size(self):
        ...
