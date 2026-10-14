def turkey_time(cron):
    fields = cron.split()
    minute = fields[0]
    hour = fields[1]
    if hour == "*":
        return "every hour at minute " + minute
    local = (int(hour) + 3) % 24
    return str(local).zfill(2) + ":" + minute.zfill(2)


print(turkey_time("0 3 * * *"))
print(turkey_time("17 3 * * *"))
print(turkey_time("30 22 * * 0"))
print(turkey_time("5 * * * *"))
