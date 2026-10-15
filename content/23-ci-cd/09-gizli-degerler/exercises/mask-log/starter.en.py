def mask_log(lines, secrets):
    # Sort the non-empty ones from longest to shortest, then replace in each line.
    pass


log = ["Login as admin", "Using token abc123XYZ", "Retry with abc123XYZ-backup", "Done"]
for line in mask_log(log, ["abc123XYZ", "", "abc123XYZ-backup"]):
    print(line)
