def mask_log(lines, secrets):
    ordered = sorted([secret for secret in secrets if secret], key=len, reverse=True)
    masked = []
    for line in lines:
        for secret in ordered:
            line = line.replace(secret, "***")
        masked.append(line)
    return masked


log = ["Login as admin", "Using token abc123XYZ", "Retry with abc123XYZ-backup", "Done"]
for line in mask_log(log, ["abc123XYZ", "", "abc123XYZ-backup"]):
    print(line)
