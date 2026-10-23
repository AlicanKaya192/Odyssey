day = input("Day: ").strip().lower()
match day:
    case "saturday" | "sunday":
        print("weekend")
    case "monday" | "tuesday" | "wednesday" | "thursday" | "friday":
        print("weekday")
    case _:
        print("unknown")
