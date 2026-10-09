def format_duration(seconds):
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

print(format_duration(3725))
print(format_duration(90061))
print(format_duration(59))
